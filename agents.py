import os
from typing import Literal
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

load_dotenv()

# Resolve data files next to this module so the CLI works from any directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize LLMs (Using Gemini). GEMINI_MODEL lets you switch models, e.g. when a free-tier quota runs out.
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
llm = ChatGoogleGenerativeAI(model=MODEL, temperature=0.7)
llm_judge = ChatGoogleGenerativeAI(model=MODEL, temperature=0.1) # Lower temp for more consistent judging

def load_knowledge_base():
    with open(os.path.join(BASE_DIR, 'knowledge_base.json'), 'r') as f:
        return f.read()

def load_prompts():
    with open(os.path.join(BASE_DIR, 'prompts.md'), 'r') as f:
        content = f.read()
    
    # Simple parser to extract sections
    sections = {}
    current_section = None
    for line in content.split('\n'):
        if line.startswith('## 1. Critic Agent'):
            current_section = 'critic'
            sections[current_section] = []
        elif line.startswith('## 2. Author Agent'):
            current_section = 'author'
            sections[current_section] = []
        elif line.startswith('## 3. Synthesizer Agent'):
            current_section = 'synthesizer'
            sections[current_section] = []
        elif line.startswith('## 4. Blind Judge Agent'):
            current_section = 'judge'
            sections[current_section] = []
        elif current_section is not None:
            sections[current_section].append(line)
            
    return {k: '\n'.join(v).strip() for k, v in sections.items()}

PROMPTS = load_prompts()
KB = load_knowledge_base()

class CritiqueOutput(BaseModel):
    critique_1: str = Field(description="First critical point")
    critique_2: str = Field(description="Second critical point")
    critique_3: str = Field(description="Third critical point")

Option = Literal["option_1", "option_2", "option_3"]

class JudgeOutput(BaseModel):
    first_choice: Option = Field(description="The option name of the 1st choice, strictly 'option_1', 'option_2', or 'option_3'")
    second_choice: Option = Field(description="The option name of the 2nd choice, strictly 'option_1', 'option_2', or 'option_3'")
    third_choice: Option = Field(description="The option name of the 3rd choice, strictly 'option_1', 'option_2', or 'option_3'")
    justification: str = Field(description="Brief justification for the 1st choice")

def critique_copy(candidate_a: str, goal: str, platform: str) -> CritiqueOutput:
    sys_msg = SystemMessage(content=f"You are operating for platform: {platform}. Here is the knowledge base:\n{KB}\n\n{PROMPTS['critic']}")
    human_msg = HumanMessage(content=f"Campaign Goal: {goal}\n\nCurrent Best Copy:\n{candidate_a}")
    
    structured_llm = llm.with_structured_output(CritiqueOutput)
    return structured_llm.invoke([sys_msg, human_msg])

def rewrite_copy(critique: CritiqueOutput, goal: str, platform: str) -> str:
    critique_str = f"1. {critique.critique_1}\n2. {critique.critique_2}\n3. {critique.critique_3}"
    sys_msg = SystemMessage(content=f"You are operating for platform: {platform}.\n\n{PROMPTS['author']}")
    human_msg = HumanMessage(content=f"Campaign Goal: {goal}\n\nCritic Feedback:\n{critique_str}")
    
    return llm.invoke([sys_msg, human_msg]).text

def synthesize_copy(candidate_a: str, candidate_b: str, goal: str, platform: str) -> str:
    sys_msg = SystemMessage(content=f"You are operating for platform: {platform}.\n\n{PROMPTS['synthesizer']}")
    human_msg = HumanMessage(content=f"Campaign Goal: {goal}\n\nDraft A:\n{candidate_a}\n\nDraft B:\n{candidate_b}")
    
    return llm.invoke([sys_msg, human_msg]).text

def judge_copies(goal: str, option_1: str, option_2: str, option_3: str, platform: str) -> JudgeOutput:
    sys_msg = SystemMessage(content=f"You are operating for platform: {platform}.\n\n{PROMPTS['judge']}")
    human_msg = HumanMessage(content=f"Campaign Goal: {goal}\n\noption_1:\n{option_1}\n\noption_2:\n{option_2}\n\noption_3:\n{option_3}")
    
    structured_llm = llm_judge.with_structured_output(JudgeOutput)
    return structured_llm.invoke([sys_msg, human_msg])
