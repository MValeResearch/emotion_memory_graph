# Phase 4: The Brain (MCP Server)

This is the nervous system. The MCP server sits between your LLM and the graph database, letting the AI query its own memory autonomously.

## Environment Variables

Before running the Brain, set your Neo4j credentials.

In your terminal:

```bash
export NEO4J_URI="neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"
```

Optional: create a `.env` file at your project root with the same three lines (without `export`). Then load it into your shell before running the server:

```bash
set -a
source .env
set +a
```

## The Script

Save this as `scripts/memory_server.py`:

```python
from mcp.server.fastmcp import FastMCP
from neo4j import GraphDatabase
import os

# Initialize the server
mcp = FastMCP("The Brain")

# Database Connection (from environment variables)
URI = os.getenv("NEO4J_URI", "neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io")
USER = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "your_password")
AUTH = (USER, PASSWORD)

def has_fulltext_index(driver, index_name: str) -> bool:
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
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
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
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        if not has_fulltext_index(driver, "contentIndex"):
            return []
        records, _, _ = driver.execute_query(
            """
            CALL db.index.fulltext.queryNodes("contentIndex", $query) YIELD node, score
            RETURN coalesce(node.content, node.text, node.title, node.name, node.path) AS content, score
            ORDER BY score DESC
            LIMIT 5
            """,
            query=query
        )
    return [r["content"] for r in records]

if __name__ == "__main__":
    mcp.run()
```

## How to Run

Run this in your terminal from the project folder:

```bash
python scripts/memory_server.py
```

The server will start listening on stdio. Keep it running, your LLM will connect to it in the next phase.

## Important

The `recall()` function uses a fulltext index called `contentIndex` that gets created in Phase 5 (Step 1.5).

If the index doesn't exist yet, `recall()` returns an empty list instead of crashing.

Move on to [Phase 5: The Telepathy](05_telepathy.md).
