import os
from neo4j import GraphDatabase
from unstructured.partition.auto import partition
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- CONFIG ---
FOLDER_PATH = "./my_memory_folder"  # Point this to your folder
NEO4J_URI = "neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io"  # Your URI here
NEO4J_USER = "neo4j"  # Your username
NEO4J_PASSWORD = "your_password"  # Your password

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def ingest_file(filepath):
    print(f" Eating: {filepath}...")
    try:
        elements = partition(filename=filepath)
        text_content = "\n\n".join([str(e) for e in elements])
        
        vector = embeddings.embed_query(text_content)
        
        query = """
        MERGE (f:File {path: $path})
        SET f.content = $content, 
            f.embedding = $vector,
            f.processed = true,
            f.timestamp = datetime()
        """
        with driver.session() as session:
            session.run(query, path=filepath, content=text_content, vector=vector)
            
    except Exception as e:
        print(f"❌ Choked on {filepath}: {e}")

def run_ingest():
    with driver.session() as session:
        session.run("""
        CREATE VECTOR INDEX file_content_index IF NOT EXISTS
        FOR (f:File) ON (f.embedding)
        OPTIONS {indexConfig: {
         `vector.dimensions`: 384,
         `vector.similarity_function`: 'cosine'
        }}
        """)

    for root, dirs, files in os.walk(FOLDER_PATH):
        for file in files:
            if not file.startswith('.'):
                ingest_file(os.path.join(root, file))
    
    print("✨ BURP. All done.")
    driver.close()

if __name__ == "__main__":
    run_ingest()
