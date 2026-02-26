# Phase 1: Infrastructure Setup

## Prerequisites

- **Python 3.x**
- **Neo4j Database:** Use the free [Neo4j Aura Cloud](https://neo4j.com/cloud/aura/) tier or Neo4j Desktop. This guide uses the cloud version.
- **LM Studio** (or a similar local LLM runner supporting the Model Context Protocol)

### Setting Up Neo4j

When you create your "AI Memory Graph" instance on Neo4j Aura, the website shows you your password **only once** and then it disappears forever for security.

**SAVE YOUR PASSWORD IMMEDIATELY.**

Also grab the Instance ID — it's displayed under the name of your instance. Save that too. You'll need both for every script in this project.

You should have three things saved:
1. Your **Neo4j URI** (looks like `neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io`)
2. Your **username** (usually `neo4j`)
3. Your **password** (the one they only show you once)

---

## Dependencies

Install the required libraries to handle vector embeddings, PDF processing, and the Neo4j connection.

Save the following as `requirements.txt` in your project root:

```
### Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
websockets==12.0
python-multipart==0.0.6

### Database
neo4j==5.14.1
chromadb==0.4.18

### Vector & Embeddings
sentence-transformers==2.2.2
numpy==1.24.3

### File Processing
pypdf2==3.0.1
pdfplumber==0.10.3
python-docx==1.1.0
pytesseract==0.3.10
pillow==10.1.0
python-magic==0.4.27

### Encryption
cryptography==41.0.7

### LLM Integration
openai==1.3.7
anthropic==0.7.8
httpx==0.25.2

### Utilities
python-dotenv==1.0.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-json-logger==2.0.7

### Emotion Analysis
textblob==0.17.1
vaderSentiment==3.3.2
scipy==1.11.4
```

Then run:

```bash
pip install -r requirements.txt
```
---

## Set Your Credentials

The Brain script (Phase 3) reads your Neo4j credentials from environment variables so they stay out of the code. Set them now so you don't forget:
```bash
export NEO4J_URI="neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io"
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="your_password"
```

Replace those values with your actual credentials (the ones you saved earlier). You'll need to run these exports in your terminal each time you open a new terminal window, or add them to your shell profile (`~/.zshrc` on Mac, `~/.bashrc` on Linux).

Alternatively, create a file called `.env` in your project root:
```
NEO4J_URI=neo4j+s://YOUR_INSTANCE_ID.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

The `.gitignore` already excludes `.env` so your credentials won't end up on GitHub.

Once everything installs cleanly, move on to [Phase 2: Ingestion](02_ingestion.md).
