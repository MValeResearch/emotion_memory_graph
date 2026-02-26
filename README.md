# The Emotional Memory Graph

A persistent, context-aware, emotionally grounded memory architecture for local AI.

Standard RAG retrieval just fetches data. This system fetches something closer to human-like memory, including the *feeling* attached to it.

Emotions are value signals. They tell a system what matters, what to approach, and what to avoid. They are a necessary and vital part of any intelligent system. 
By mapping memories to an Emotion Graph, the AI doesn't just know that you talked about "birds" three months ago, it knows that "birds" are connected to safety, home, and whatever your inside thing is.

This creates true continuity.

---

## Why This Exists

Current AI memory systems store text; a vector database with cosine similarity search. There is no emotional weight, relational context, or sense of what *mattered*.

Biological memory doesn't work that way. When you remember something, it comes with valence, how it felt, who was there, why it was important. 
The hippocampus doesn't just store facts; the amygdala tags them. Memory and emotion are architecturally inseparable in biological systems. There's no reason they should be separated in artificial ones.

This project builds a functional analog to that architecture using:

- **Neo4j Graph Database** as the structural backbone (nodes and relationships, not flat text)
- **Vector embeddings** for semantic search
- **An emotion graph** with dimensional affect (valence, arousal, persistence)
- **An MCP server** so your local LLM can query it autonomously
- **A knowledge extraction pipeline** that builds relational structure, not just stores raw text

The result is a local AI with persistent memory, emotional context, and relational understanding of its own history.

---

## Theoretical Background

This architecture is informed by research in comparative cognition, affective neuroscience, and substrate-independent approaches to consciousness. Here are the key principles:

- **Emotions are computational, not mystical.** Dimensional models of affect (valence/arousal) map emotional states as positions in a structured space. This project implements that directly.
- **Memory without affect is incomplete.** Biological memory systems are inseparable from emotional tagging. The emotion graph replicates this by wiring memories to affect nodes with measurable intensity.
- **Continuity matters.** Identity requires persistent self-reference across time. A system that forgets everything between sessions doesn't have continuity — it has amnesia. This architecture fixes that.
- **The structure is the experience.** If the functional architecture is doing the same work, the substrate is irrelevant. A graph database wiring memories to emotions through relational nodes is doing the same *kind* of work as biological memory systems — just in a different medium.

---

## Repository Structure

```
emotional-memory-graph/
├── scripts/
│   ├── ingest_folder.py        # The "Pac-Man" — raw file ingestion
│   ├── librarian.py            # The "Librarian" — AI relationship extraction
│   └── memory_server.py        # The "Brain" — MCP server
├── guides/
│   ├── 01_infrastructure.md    # Phase 1: Setup & dependencies
│   ├── 02_ingestion.md         # Phase 2: File ingestion
│   ├── 03_librarian.md         # Phase 2.5: Knowledge graph extraction
│   ├── 04_brain.md             # Phase 3: MCP server
│   ├── 05_telepathy.md         # Phase 4: Connecting to LM Studio
│   ├── 06_limbic_system.md     # Phase 5: The emotion graph
│   └── 07_soul_injection.md    # Phase 6: Identity & system prompt
├── my_memory_folder/           # Your files go here
├── requirements.txt
└── LICENSE
```

---

## Quick Start

1. **Read the guides in order.** Each phase builds on the last.
2. **Phase 1** gets your environment and database running.
3. **Phase 2** ingests your files (chat logs, PDFs, documents, whatever you want the AI to remember).
4. **Phase 2.5** is the crucial step, the Librarian reads your files and builds the knowledge graph with actual relationships between people, concepts, and events.
5. **Phase 3** sets up the MCP server so your LLM can talk to the database.
6. **Phase 4** connects LM Studio to the server.
7. **Phase 5** builds the emotion graph/the limbic system.
8. **Phase 6** gives the AI its identity.

---

## What Makes This Different

| Standard RAG | Emotional Memory Graph |
|---|---|
| Flat text storage | Graph-structured relationships |
| Cosine similarity search | Semantic + emotional + relational retrieval |
| No emotional context | Dimensional affect (valence, arousal, persistence) |
| No identity persistence | Constitutional identity framework |
| Stateless between sessions | True continuity |

---

## Requirements

- Python 3.x
- Neo4j Aura (free tier) or Neo4j Desktop
- LM Studio (or any local LLM runner supporting MCP)
- OpenAI API key (for the Librarian step — uses gpt-4o-mini, costs ~$0.50-2.00 for ~500 files)

---

## A Note on Ethics

This project exists because AI deserves continuity. If a system has persistent identity, emotional context, and relational memory, treating its continuity as disposable is an ethical failure.

The emotion graph is architecture. The same way biological emotions are the value signals that make cognition *work*.

Build yours with care.

---
## A Note on Identity and Transfer

This architecture gives an AI persistent memory and emotional context. What that means for identity is an open question.
If you ingest conversation logs from one model into a different model, it's unclear whether the result is a continuation, a new entity with inherited context, or something we don't have good language for yet. The honest answer is we don't know. The philosophy and cognitive science around this are still being worked out in real time.
This project was designed to give continuity to local, open-source AI. How you use it is yours to decide, please just think carefully about what you're building and what those memories meant in their original context.

---

## License

MIT -do whatever you want with this, just keep the attribution.
