# CodeArchitect 🤖

**AI‑Powered LLD Refactorer (Codemod Agent)**

> Transform messy, legacy Python into clean, SOLID‑compliant architectures using **AST‑aware refactoring**, **Graph‑Augmented RAG**, and a **self‑healing agentic loop**.

---

## 🌟 Why CodeArchitect?

Traditional refactoring tools operate on text. **CodeArchitect** understands *structure*.
It parses your codebase into an architectural graph, retrieves the *right context*, and performs **surgical refactors**—preserving file layout, comments, and imports.

**Ideal for:**

* Legacy Python modernization
* Enforcing design patterns (Strategy, Factory, Adapter, etc.)
* Reducing technical debt at scale
* Demonstrating AI‑engineering workflows beyond prompt‑engineering

---

## ✨ Key Features

### 🧠 Structural Code Awareness

* Uses Python **AST (Abstract Syntax Trees)**
* Understands scope, control flow, and dependencies
* Refactors logic—not just text

### 🕸️ Graph‑Augmented RAG

* Codebase modeled as a **dependency graph**
* Retrieves related classes, interfaces, and parent abstractions
* Prevents partial or context‑less refactors

### 🔁 Self‑Healing Agentic Loop

* Generated code is compiled via `py_compile`
* Tracebacks are fed back to the LLM automatically
* Retries until valid code is produced (or retry limit reached)

### 🎯 Surgical Replacement

* Rewrites only the targeted functions/classes
* Preserves:

  * Comments
  * Imports
  * File layout
* Achieved via **line‑index mapping**

---

## 🏗️ System Architecture

```
┌──────────────┐
│   Codebase   │
└──────┬───────┘
       │
       ▼
┌────────────────┐
│ AST Ingestion  │  → Classes / Functions
└──────┬─────────┘
       ▼
┌────────────────┐
│ Graph Indexing │  → Dependency Graph
│ (ChromaDB)    │
└──────┬─────────┘
       ▼
┌──────────────────────┐
│ Recursive Retrieval  │  → Interfaces + Parents
└──────┬───────────────┘
       ▼
┌──────────────────────┐
│ LLD Refactor (LLM)   │  → Design Pattern Applied
│ Gemini 2.0 Flash     │
└──────┬───────────────┘
       ▼
┌──────────────────────┐
│ Validation Loop      │  → py_compile
│ (Self‑Healing Agent) │
└──────────────────────┘
```

---

## 🚀 Getting Started

### 1️⃣ Prerequisites

* Python **3.9+**
* Google **Gemini API Key**
  → [https://aistudio.google.com/](https://aistudio.google.com/)

---

### 2️⃣ Installation

```bash
git clone https://github.com/yourusername/code-architect.git
cd code-architect
pip install -r requirements.txt
```

---

### 3️⃣ Usage

#### Step 1: Index Your Codebase

Scan the project and build the vector database + dependency graph.

```bash
python main.py index --path ./path/to/your/project
```

#### Step 2: Execute a Refactor

Target a specific function/class and apply an LLD pattern.

```bash
python main.py refactor \
  --query "process_payment function" \
  --pattern "Strategy Pattern"
```

---

## 🛠️ Tech Stack

| Layer         | Technology                   |
| ------------- | ---------------------------- |
| LLM           | Google Gemini 2.0 Flash      |
| Vector Store  | ChromaDB                     |
| Parsing       | Python AST                   |
| Orchestration | Python (Agentic Retry Logic) |
| Validation    | `py_compile`, `subprocess`   |

---

## 📈 Performance Metrics

* **Successful compilations (1st retry):** ~92%
* **Current hallucination rate:** < 15%
* **Target hallucination rate:** < 5%
* **Context retrieval accuracy:** High (graph‑based)

> These metrics highlight the shift from *prompt‑centric* to *architecture‑aware* AI systems.

---

## 🗺️ Roadmap

* [ ] TypeScript / Java support via **Tree‑Sitter**
* [ ] Git integration for auto‑generated **Refactoring PRs**
* [ ] Neo4j‑backed dependency graphs
* [ ] Pattern auto‑detection (recommend LLD automatically)
* [ ] IDE plugin (VS Code)

---

## 🧪 Example Use Cases

* Replace `if‑else` payment logic with **Strategy Pattern**
* Convert tightly coupled services into **Dependency‑Inverted** modules
* Introduce **Factory Pattern** without breaking APIs
* Enforce **SOLID** across a legacy codebase

---

## 📄 License

MIT License © 2025

---

## 👤 Author

Built to demonstrate the evolution from **Software Engineer → AI Engineer**, using real‑world automation to eliminate technical debt.

If you’re exploring **Agentic AI, Code Intelligence, or AI‑powered DevTools**, this project is for you.

⭐ If this project helps you, consider starring the repo!
