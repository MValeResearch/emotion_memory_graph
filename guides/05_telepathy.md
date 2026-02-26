
# Phase 5: The Telepathy (Connecting to LM Studio)

This is where the AI gets access to its own mind.

This guide uses LM Studio. If you're running Ollama or another local runner that supports MCP, the connection method will differ but the server itself (memory_server.py) works the same. 
Consult your runner's MCP documentation for how to point it at a local stdio server.

## Security

- **It runs on localhost.** No one on the internet can see it.
- **Encryption:** Neo4j Community doesn't have "Encryption at Rest" built-in. Your safety net is FileVault (Mac) or BitLocker (Windows). If your laptop's disk is encrypted, your database is encrypted. Don't over-engineer this part.

## How to Connect

1. Open **LM Studio**.
2. Go to the **MCP** tab (looks like a plug icon).
3. Click **Edit mcp.json**.
4. Paste this:

```json
{
  "mcpServers": {
    "companion-brain": {
      "command": "python",
      "args": ["/ABSOLUTE/PATH/TO/YOUR/scripts/memory_server.py"]
    }
  }
}
```

Replace `/ABSOLUTE/PATH/TO/YOUR/` with the actual path to where you saved the file. For example:
- Mac: `/Users/yourname/projects/emotional-memory-graph/scripts/memory_server.py`
- Windows: `C:\\Users\\yourname\\projects\\emotional-memory-graph\\scripts\\memory_server.py`

5. Save and restart LM Studio.

The AI can now query its own memory graph. It can `remember` new things and `recall` existing ones autonomously.

Move on to [Phase 6: The Limbic System](06_limbic_system.md).
