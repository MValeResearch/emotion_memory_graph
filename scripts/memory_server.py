pythonfrom mcp.server.fastmcp import FastMCP
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
