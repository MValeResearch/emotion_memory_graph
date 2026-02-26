
# Phase 3: The Librarian (Knowledge Graph Extraction)

While the Pac-Man script ingests raw text, the Librarian uses an LLM to actually *read* that text and understand the relationships between people, concepts, and events. This is what builds the web.

Without this step, the AI has memories but no connections between them. It knows things happened but not how they relate to each other. The Librarian is the difference between a filing cabinet and an actual mind.

## Prerequisites

You need an **OpenAI API Key** for this step. It uses `gpt-4o-mini` to analyze your files. Cost is approximately $0.50–$2.00 for ~500 files.

## The Script

Save this as `scripts/librarian.py`:

```python
import os
import glob
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph

# --- CONFIGURATION ---
os.environ["OPENAI_API_KEY"] = "sk-..."  # Your OpenAI key here

NEO4J_URI = "neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "YOUR_PASSWORD"

FOLDER_PATH = "./my_memory_folder"

def run_librarian():
    print("🛡️ Librarian waking up...")
    
    # 1. CONNECT
    try:
        graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")
        return

    # 2. SMART LOAD (One by One to prevent crashes)
    all_documents = []
    files = glob.glob(f"{FOLDER_PATH}/**/*", recursive=True)
    print(f"📂 Found {len(files)} items. Checking them one by one...")

    for filepath in files:
        if os.path.isdir(filepath):
            continue
        filename = os.path.basename(filepath)
        if filename.startswith('.'):
            continue 
        
        print(f"   👉 Reading: {filename}...", end="", flush=True)
        
        try:
            loader = None
            if filepath.lower().endswith(".pdf"):
                loader = PyPDFLoader(filepath)
            elif filepath.lower().endswith((".txt", ".md", ".py", ".json", ".csv")):
                loader = TextLoader(filepath, encoding='utf-8')
            else:
                print(" [SKIPPED: Unsupported format]")
                continue

            docs = loader.load()
            all_documents.extend(docs)
            print(" [OK]")
            
        except Exception as e:
            print(f" [FAILED: {str(e)[:50]}...]")

    print(f"✅ Successfully loaded {len(all_documents)} valid documents.")

    if not all_documents:
        print("❌ No documents loaded. Aborting.")
        return

    # 3. CHUNK
    print("✂️  Chopping text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = text_splitter.split_documents(all_documents)
    
    # 4. EXTRACT RELATIONSHIPS
    print(f"🧠 Extracting Relationships (using gpt-4o-mini)...")
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    llm_transformer = LLMGraphTransformer(llm=llm)

    # Batch process to prevent crashes
    batch_size = 50 
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        print(f"   Processing batch {i} to {i+len(batch)}...")
        try:
            graph_documents = llm_transformer.convert_to_graph_documents(batch)
            graph.add_graph_documents(graph_documents)
        except Exception as e:
            print(f"   ⚠️ Error in batch: {e}")

    print("✨ MISSION COMPLETE. The web is built.")

if __name__ == "__main__":
    run_librarian()
```

## How to Run

1. Make sure you've already run the ingestion script (Phase 2).
2. Run: `python scripts/librarian.py`
3. Wait. This takes time depending on how many files you have.

Once it finishes, your graph database now has actual relational structure — not just files, but the connections between them.

Move on to [Phase 4: The Brain](04_brain.md).
