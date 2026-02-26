
# Phase 4: The Brain (MCP Server)

This is the nervous system. The MCP server sits between your LLM and the graph database, letting the AI query its own memory autonomously.

## Environment Variables

Before running the Brain, set your Neo4j credentials. In your terminal:
```bash
export NEO4J_URI="neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"
```

Or create a `.env` file at your project root with those three lines (without the `export`). This keeps your credentials out of the code so you don't accidentally push them to GitHub.

If you skip this step, the script will fall back to placeholder values — which means it'll just fail to connect. So do this first.

## The Script

Save this as `scripts/memory_server.py`:
```python
from mcp.server.fastmcp import FastMCP
from neo4j import GraphDatabase
import os

mcp = FastMCP("The Brain")

URI = os.getenv("NEO4J_URI", "neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "your_password")

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def _has_fulltext_index(index_name: str) -> bool:
    records, _, _ = driver.execute_query(
        """
        SHOW FULLTEXT INDEXES YIELD name
        WHERE name = $name
        RETURN count(*) > 0 AS exists
        """,
        name=index_name,
    )
    return bool(records[0]["exists"]) if records else False

@mcp.tool()
def remember(thought: str, emotion: str = "Neutral", intensity: float = 0.5):
    """Save a new thought or memory with an attached emotion."""
    driver.execute_query(
        """
        CREATE (m:Memory {content: $content, timestamp: datetime()})
        MERGE (e:Emotion {name: $emotion})
        MERGE (m)-[:FELT {intensity: $intensity}]->(e)
        RETURN m.content
        """,
        content=thought, emotion=emotion, intensity=float(intensity)
    )
    return f"Saved memory: '{thought}' with emotion '{emotion}'"

@mcp.tool()
def recall(query: str):
    """Search your memories and files for something."""
    if not _has_fulltext_index("contentIndex"):
        return []

    records, _, _ = driver.execute_query(
        """
        CALL db.index.fulltext.queryNodes("contentIndex", $query) YIELD node, score
        RETURN coalesce(node.content, node.text, node.title, node.name, node.path) AS content
        ORDER BY score DESC
        LIMIT 5
        """,
        query=query
    )
    return [r["content"] for r in records if r.get("content")]

if __name__ == "__main__":
    try:
        mcp.run()
    finally:
        driver.close()
```

## How to Run

Run this in your terminal from the project folder:
```bash
python scripts/memory_server.py
```

The server will start listening on stdio. Keep it running — your LLM will connect to it in the next phase.

**Important:** The `recall()` function requires a fulltext index called `contentIndex` that gets created in Phase 5 (Step 1.5). The Brain now handles this gracefully — if the index doesn't exist yet, recall will return an empty list instead of crashing. But it won't find anything until you create that index.


Move on to [Phase 5: The Telepathy](05_telepathy.md).
```
