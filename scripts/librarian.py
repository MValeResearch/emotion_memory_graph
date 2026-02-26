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
    
    try:
        graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")
        return

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

    print("✂️  Chopping text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    documents = text_splitter.split_documents(all_documents)
    
    print(f"🧠 Extracting Relationships (using gpt-4o-mini)...")
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    llm_transformer = LLMGraphTransformer(llm=llm)

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
