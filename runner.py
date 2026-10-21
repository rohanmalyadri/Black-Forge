import random
import logging
from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
from agents import critique_copy, rewrite_copy, synthesize_copy, judge_copies, CritiqueOutput

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class GraphState(TypedDict):
    campaign_goal: str
    platform: str
    candidate_a: str
    critique_feedback: CritiqueOutput
    candidate_b: str
    candidate_ab: str
    survival_count: int
    round: int
    max_rounds: int
    final_output: str

def critique_node(state: GraphState) -> Dict:
    logging.info(f"--- ROUND {state['round']} : CRITIQUE PHASE ---")
    critique = critique_copy(state['candidate_a'], state['campaign_goal'], state['platform'])
    logging.info(f"Critiques: {critique.critique_1} | {critique.critique_2} | {critique.critique_3}")
    return {"critique_feedback": critique}

def rewrite_node(state: GraphState) -> Dict:
    logging.info("--- REWRITE PHASE ---")
    new_copy = rewrite_copy(state['critique_feedback'], state['campaign_goal'], state['platform'])
    return {"candidate_b": new_copy}

def synthesize_node(state: GraphState) -> Dict:
    logging.info("--- SYNTHESIZE PHASE ---")
    synth_copy = synthesize_copy(state['candidate_a'], state['candidate_b'], state['campaign_goal'], state['platform'])
    return {"candidate_ab": synth_copy}

def judgment_node(state: GraphState) -> Dict:
    logging.info("--- JUDGMENT PHASE ---")
    
    # Randomize to prevent position bias
    candidates = [
        ("A", state['candidate_a']),
        ("B", state['candidate_b']),
        ("AB", state['candidate_ab'])
    ]
    random.shuffle(candidates)
    
    option_mapping = {
        "option_1": candidates[0],
        "option_2": candidates[1],
        "option_3": candidates[2],
    }
    
    # 3 Judges
    scores = {"A": 0, "B": 0, "AB": 0}
    
    for i in range(3):
        judge_result = judge_copies(
            goal=state['campaign_goal'],
            platform=state['platform'],
            option_1=option_mapping["option_1"][1],
            option_2=option_mapping["option_2"][1],
            option_3=option_mapping["option_3"][1],
        )
        
        # Borda Count (1st = 3, 2nd = 2, 3rd = 1)
        scores[option_mapping[judge_result.first_choice][0]] += 3
        scores[option_mapping[judge_result.second_choice][0]] += 2
        scores[option_mapping[judge_result.third_choice][0]] += 1
        
        logging.info(f"Judge {i+1} favored: {option_mapping[judge_result.first_choice][0]}. Reason: {judge_result.justification}")

    logging.info(f"Final Scores: {scores}")
    
    # Determine Winner
    winner_key = max(scores, key=scores.get)
    logging.info(f"Winner of Round {state['round']} is Candidate {winner_key}")
    
    updates = {"round": state['round'] + 1}
    
    if winner_key == "A":
        updates["survival_count"] = state['survival_count'] + 1
    else:
        updates["survival_count"] = 0
        if winner_key == "B":
            updates["candidate_a"] = state['candidate_b']
        elif winner_key == "AB":
            updates["candidate_a"] = state['candidate_ab']

    return updates

def should_continue(state: GraphState) -> str:
    if state["survival_count"] >= 2:
        logging.info(f"✅ Candidate A has survived 2 rounds! Terminating.")
        return "end"
    if state["round"] >= state["max_rounds"]:
        logging.warning("🛑 Max rounds reached. Terminating early.")
        return "end"
    return "continue"

# Build Graph
builder = StateGraph(GraphState)

builder.add_node("critique", critique_node)
builder.add_node("rewrite", rewrite_node)
builder.add_node("synthesize", synthesize_node)
builder.add_node("judge", judgment_node)

builder.set_entry_point("critique")
builder.add_edge("critique", "rewrite")
builder.add_edge("rewrite", "synthesize")
builder.add_edge("synthesize", "judge")

builder.add_conditional_edges(
    "judge",
    should_continue,
    {
        "continue": "critique",
        "end": END
    }
)

graph = builder.compile()

def run_experiment(goal: str, platform: str, initial_draft: str, max_rounds: int = 5):
    initial_state = {
        "campaign_goal": goal,
        "platform": platform,
        "candidate_a": initial_draft,
        "survival_count": 0,
        "round": 1,
        "max_rounds": max_rounds
    }
    
    print("\n🚀 Starting Black Forge AutoReason Optimization...")
    print(f"Goal: {goal}")
    print(f"Platform: {platform}")
    print(f"Initial Draft:\n{initial_draft}\n")
    print("-" * 40)
    
    # Each round is 4 graph steps; leave headroom over LangGraph's default limit of 25
    final_state = graph.invoke(initial_state, config={"recursion_limit": max_rounds * 4 + 10})
    
    print("\n" + "=" * 40)
    print("🎯 OPTIMIZATION COMPLETE")
    print(f"Rounds Elapsed: {final_state['round'] - 1}")
    print("WINNING COPY:")
    print(final_state['candidate_a'])
    print("=" * 40)
    
    return final_state['candidate_a']
