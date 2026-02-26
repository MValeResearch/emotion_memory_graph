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
            MERGE (e:Emotion {name: $emotion})
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
    mcp.run()
