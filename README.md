# 🌌 Black Forge : The Personal Agent OS & Marketing Framework

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Gemini 1.5](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange.svg)](https://deepmind.google/technologies/gemini/)
[![LangGraph](https://img.shields.io/badge/Framework-LangGraph-green.svg)](https://github.com/langchain-ai/langgraph)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Black Forge** is a modular, high-fidelity Personal Agent architecture designed to bridge the gap between LLM reasoning and local system execution. It combines an adversarial **AutoReason** marketing engine with a sandboxed **Agent OS** foundation.

---

## ✨ Features

- 🧠 **Adversarial Optimization (AutoReason)**: An optimization loop that uses Critic and Judge agents to iteratively refine marketing copy until it survives blind evaluation.
- 🛡️ **Docker-Sandboxed CLI**: Safely execute shell commands and file operations within isolated Ubuntu containers.
- 📂 **MCP (Model Context Protocol)**: Ready for external tool synchronization via standard JSON-RPC.
- 💾 **Multi-Layer Memory**:
    - **Global Persona**: Core identity stored in `~/.black_forge/soul.md`.
    - **User Preferences**: Persistent settings in `~/.black_forge/user.md`.
    - **Local Discovery**: Automatic ingestion of `BLACK_FORGE.md` or `CLAUDE.md` context files.
- 🚀 **Swarm Coordination**: Logic for spawning specialized sub-agent teams for complex, multi-stage engineering tasks.

---

## 🔥 Core Capabilities

| Capability | Description |
| :--- | :--- |
| **Autonomous ReAct Loop** | Black Forge doesn't just talk; it **reasons and acts**. It iteratively uses tools, processes results, and refines its approach until the goal is met. |
| **The Hard Wall (Sandbox)** | Executes all terminal commands inside a **Docker Sandbox** (`ubuntu:latest`), protecting your host OS from accidental damage or malicious code. |
| **Context-Aware Memory** | Merges global persona (`soul.md`), user preferences (`user.md`), and local project overrides (`BLACK_FORGE.md`) into a high-fidelity system prompt. |
| **Dynamic Tool Registry** | Easily extensible tool system featuring Pydantic schemas for built-ins, Shell, and MCP-synced tools. |
| **Event-Driven Messaging** | A decoupled **MessageBus** architecture ready to bridge the engine to Slack, Telegram, or custom webhooks. |

---

## 🚀 Real-World Use Cases

- 👨‍💻 **Autonomous Software Engineering**: Ask Black Forge to read your codebase, identify bottlenecks, and write/test new modules safely within the sandbox.
- 🛡️ **Safe System Investigation**: Run complex bash scripts or audit your system files without giving an LLM direct access to your root file system.
- 📈 **Adversarial Marketing Optimization**: Use the built-in **AutoReason** framework to generate high-converting copy that survives ruthless peer-critique from other agents.
- 📂 **Standardized Project Guardrails**: Drop a `BLACK_FORGE.md` file into a repository to instantly enforce specific coding standards or library choices across all agent interactions.
- 🤖 **Cross-Platform Virtual Assistant**: Deploy the Black Forge backend and interact with your local environment via secure Slack or Discord channels.

---

## 🛠 Installation & Setup

1. **Clone & Environment** (Python 3.9+):
   ```bash
   git clone https://github.com/rohanmalyadri/Black-Forge.git
   cd Black-Forge
   python3 -m venv .black_forge-env
   source .black_forge-env/bin/activate
   pip install -r requirements.txt   # also installs the black_forge package
   ```

2. **Configure API Key**:
   ```bash
   cp .env.example .env   # then put your Gemini key in GOOGLE_API_KEY
   ```

3. **Initialize & run Black Forge**:
   ```bash
   s setup                                  # creates ~/.black_forge and checks your key
   s about                                  # what Black Forge is
   s chat "List the files in this folder"   # agent loop with tools
   ```
   Docker is optional; without it the `run_shell` tool reports that sandboxing is unavailable.

---

## 📈 Showcase: AutoReason Optimization

The **AutoReason** engine treats content generation as an optimization problem. Below is an example of the system iterating on LinkedIn hooks until they meet the brand's quality threshold.

### 📥 Example Input
```bash
python main.py --goal "Generate 5 LinkedIn hooks for Black Forge" --platform "LinkedIn" --draft "Black Forge is a personal agent on your terminal."
```

### 📤 Optimized Output
> [!TIP]
> After 3 rounds of adversarial critique, the system produced the following "Champion" variants:

| Hook Type | Refined Copy |
| :--- | :--- |
| **The Bottleneck** | "The real bottleneck to your biggest wins? It's often your tools. Stop letting tech hold you back. Black Forge isn't an app; it's an engine." |
| **Precision** | "Information overload kills clarity. While your peers drown in data, navigate every challenge with absolute precision." |
| **Revolution** | "Still managing your day like it's 2010? Outdated processes are holding you back. Step into the intelligent revolution." |

---

## 🏗 Architecture

Black Forge is built on a distributed agentic design:

```mermaid
graph TD
    User([User CLI]) --> Gateway[Session Pool / Gateway]
    Gateway --> Engine[QueryEngine / Agent Loop]
    Engine --> Memory[Soul + User + Local MD Context]
    Engine --> Tools[Registry: File I/O, MCP, Sandbox]
    Tools --> Sandbox[Docker Ubuntu Container]
    Engine --> LLM[Gemini 1.5 Flash Provider]
```

---

## 🤝 Contributing

Contributions are welcome! Whether it's adding a new **LLM Provider** or a **Built-in Tool**, please feel free to open a PR.

---

<p align="center">
  <b>Black Forge</b> · Made with love Rohan Malyadri From <b>Obscuron X Labs</b> ❤️
</p>
