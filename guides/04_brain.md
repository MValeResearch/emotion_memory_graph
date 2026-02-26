
# Phase 3: The Brain (MCP Server)

This is the nervous system. The MCP server sits between your LLM and the graph database, letting the AI query its own memory autonomously.

## The Script

Save this as `scripts/memory_server.py`:

```python
from mcp.server.fastmcp import FastMCP
from neo4j import GraphDatabase
import datetime

# Initialize the server
mcp = FastMCP("The Brain")

# Database Connection
URI = "neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io"  # Your URI
AUTH = ("neo4j", "your_password")  # Your credentials

@mcp.tool()
def remember(thought: str, emotion: str = "Neutral", intensity: float = 0.5):
    """Save a new thought or memory with an attached emotion."""
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.execute_query(
            """
            CREATE (m:Memory {content: $content, timestamp: datetime()})
            MERGE (e:Emotion {type: $emotion})
            MERGE (m)-[r:FELT {intensity: $intensity}]->(e)
            RETURN m.content
            """,
            content=thought, emotion=emotion, intensity=intensity
        )
    return f"Saved memory: '{thought}' with emotion '{emotion}'"

@mcp.tool()
def recall(query: str):
    """Search your memories and files for something."""
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        records, _, _ = driver.execute_query(
            """
            CALL db.index.fulltext.queryNodes("contentIndex", $query) YIELD node, score
            RETURN node.content as content, score
            LIMIT 5
            """,
            query=query
        )
    return [r["content"] for r in records] if records else "My mind is blank on that."

if __name__ == "__main__":
    # Runs on stdio (standard input/output) for local privacy
    mcp.run()
```

## How to Run

Run this in your terminal from the project folder:

```bash
python scripts/memory_server.py
```

The server will start listening on stdio. Keep it running — your LLM will connect to it in the next phase.

Move on to [Phase 5: The Telepathy](05_telepathy.md).
