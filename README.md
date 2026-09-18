<img width="1280" height="672" alt="image" src="https://github.com/user-attachments/assets/d894f6c4-1ba5-47b6-8d2f-2ded0cd11d46" /># RAG Study Assistant

A Retrieval-Augmented Generation (RAG) based AI Study Assistant that answers questions from educational documents using semantic retrieval, vector embeddings, and a locally hosted Large Language Model.

The system retrieves relevant document chunks from a ChromaDB vector store and uses Ollama with Llama 3.2 to generate grounded answers based only on the retrieved context.

The project provides a FastAPI backend for the RAG pipeline and a Streamlit frontend for an interactive chat-style interface.

---

## 1. Project Overview

The goal of this project is to build a complete end-to-end RAG application that can answer questions from a predefined collection of study documents.

Instead of allowing the language model to answer using only its pretrained knowledge, the system follows a retrieval-first architecture:

1. A user submits a question.
2. The question is converted into an embedding.
3. ChromaDB searches the vector store for semantically similar document chunks.
4. The most relevant chunks and their metadata are retrieved.
5. The retrieved context is provided to the local LLM.
6. The LLM generates an answer based only on the retrieved documents.
7. The backend returns the answer together with the retrieved sources.
8. The Streamlit frontend displays the answer and sources to the user.

This approach improves grounding and reduces unsupported answers.

---

## 2. Domain and Data Description

### Domain

The project focuses on educational and machine learning study materials.

The main source document used for the RAG system is:

**Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow**

The document contains educational material covering topics such as:

* Machine Learning fundamentals
* Supervised and unsupervised learning
* Classification
* Regression
* Model evaluation
* Cross-validation
* ROC curves
* Ensemble methods
* Random Forests
* Neural Networks
* Generative Adversarial Networks
* Reinforcement Learning
* Q-learning
* Bias and variance
* Model training and regularization

### Data Processing

The document was processed page by page and divided into smaller chunks suitable for semantic retrieval.

Each chunk stores metadata including:

* Source document
* Page number
* Chunk identifier

The final ChromaDB collection contains:

**2,449 document chunks**

The page-aware metadata allows the system to return not only relevant text but also the source and page where the information was found.

---

## 3. System Architecture

```text
                         User
                           |
                           v
                  Streamlit Frontend
                           |
                           | HTTP POST /query
                           v
                    FastAPI Backend
                           |
                           v
                    Query Processing
                           |
                           v
                 Sentence Transformer
                    Embedding Model
                           |
                           v
                     ChromaDB
                  Vector Retrieval
                           |
                           | Top-K Chunks
                           v
                  Retrieved Context
                           |
                           v
                      Ollama
                     Llama 3.2
                           |
                           v
                  Grounded Answer
                           |
                           v
                 Answer + Sources
                           |
                           v
                  Streamlit Frontend
```

---

## 4. RAG Pipeline

The RAG pipeline consists of the following stages.

### 4.1 Document Loading

The source document is loaded and processed page by page.

The notebook inspects the document and prepares the content for chunking.

### 4.2 Chunking

The document is divided into smaller chunks.

Chunking allows the retrieval system to search for specific pieces of information instead of processing the entire document for every question.

The chunking configuration is defined in the RAG notebook and exported as part of the project configuration.

### 4.3 Embeddings

Each document chunk is converted into a numerical vector representation using:

```text
all-MiniLM-L6-v2
```

These embeddings capture the semantic meaning of the text and allow the system to perform similarity-based retrieval.

### 4.4 Vector Store

The embeddings are stored in:

```text
ChromaDB
```

The persisted vector store contains the embedded document chunks together with their metadata.

### 4.5 Retrieval

When a user asks a question, the question is embedded and compared with the stored document embeddings.

The system retrieves the most relevant chunks using semantic similarity.

The retrieval process is page-aware and returns metadata such as:

```text
Source: Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow
Page: 60
Distance: 0.5688
```

### 4.6 Generation

The retrieved chunks are passed to the local LLM running through Ollama.

The model used is:

```text
Llama 3.2
```

The generation prompt instructs the model to answer using the provided context and avoid relying on outside information.

If the retrieved documents do not contain enough information, the system can respond:

```text
I don't have enough information in the documents to answer that.
```

This provides a grounding mechanism against unsupported answers.

---

## 5. Technologies

| Technology            | Purpose                     |
| --------------------- | --------------------------- |
| Python 3.14.5         | Main programming language   |
| FastAPI               | Backend REST API            |
| Uvicorn               | ASGI server                 |
| Pydantic              | Request/response validation |
| Pydantic Settings     | Environment configuration   |
| ChromaDB              | Vector database             |
| Sentence Transformers | Text embeddings             |
| all-MiniLM-L6-v2      | Embedding model             |
| Ollama                | Local LLM runtime           |
| Llama 3.2             | Generation model            |
| Streamlit             | Frontend interface          |
| Pytest                | Backend testing             |
| HTTPX                 | API testing                 |
| Jupyter Notebook      | RAG pipeline development    |

---

## 6. Project Structure

```text
rag-assistant-project/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       └── query.py
│   │   │
│   │   ├── core/
│   │   │   └── config.py
│   │   │
│   │   ├── schemas/
│   │   │   └── query.py
│   │   │
│   │   ├── services/
│   │   │   ├── retrieval.py
│   │   │   └── generation.py
│   │   │
│   │   ├── utils/
│   │   │   └── logging_config.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   │   └── test_query.py
│   │
│   ├── .env.example
│   ├── Dockerfile
│   └── requirements.txt
│
├── data/
│   └── generate_sample_docs.py
│
├── frontend/
│   ├── api_client.py
│   ├── app.py
│   ├── .env.example
│   └── requirements.txt
│
├── notebooks/
│   └── rag_pipeline.ipynb
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 7. Requirements

Before running the project, make sure the following are installed:

* Python 3.14.5
* Ollama
* Git

The project uses separate Python dependencies for the backend and frontend.

---

## 8. Clone the Repository

```bash
git clone https://github.com/RawanMahmoud30/rag-assistant-project.git
cd rag-assistant-project
```

---

## 9. Create the Virtual Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should show:

```text
(.venv)
```

---

## 10. Install Dependencies

Install the project dependencies:

```bash
pip install -r requirements.txt
```

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Install frontend dependencies:

```bash
pip install -r frontend/requirements.txt
```

---

## 11. Ollama Setup

The project uses Ollama to run the LLM locally.

Install Ollama and make sure the Ollama service is running.

Pull the required model:

```bash
ollama pull llama3.2
```

Verify that the model is available:

```bash
ollama list
```

The output should contain:

```text
llama3.2
```

The backend communicates with Ollama through:

```text
http://localhost:11434
```

---

## 12. Environment Variables

### Backend

Create:

```text
backend/.env
```

based on:

```text
backend/.env.example
```

Example configuration:

```env
VECTOR_STORE_DIR=./data/vector_store
CHROMA_COLLECTION_NAME=study_assistant_docs
EMBEDDING_MODEL_NAME=all-MiniLM-L6-v2
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2
TOP_K=4
FRONTEND_ORIGINS=http://localhost:8501
```

### Frontend

Create:

```text
frontend/.env
```

based on:

```text
frontend/.env.example
```

Example:

```env
API_BASE_URL=http://localhost:8000
```

The backend URL is configured through an environment variable rather than being hard-coded into the frontend application.

---

## 13. Vector Store

The RAG notebook creates a persisted ChromaDB vector store.

The notebook uses:

```text
data/vector_store/
```

and prepares the backend vector store under:

```text
backend/data/vector_store/
```

The vector store contains:

* ChromaDB database
* Vector embeddings
* Document chunks
* Source metadata
* Page metadata

If the vector store is not available after cloning, run the notebook:

```text
notebooks/rag_pipeline.ipynb
```

from top to bottom to recreate it.

---

## 14. Running the Backend

Open a terminal in the project directory.

Move to the backend directory:

```powershell
cd backend
```

Activate the virtual environment if it is not already active:

```powershell
..\ .venv\Scripts\Activate.ps1
```

Use this command without the space if needed:

```powershell
..\.venv\Scripts\Activate.ps1
```

Start FastAPI:

```bash
python -m uvicorn app.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

---

## 15. Health Check

The backend provides:

```text
GET /health
```

Example:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## 16. Query API

The main endpoint is:

```text
POST /query
```

### Request

```json
{
  "question": "What is overfitting?"
}
```

### Example using curl

```bash
curl -X POST "http://127.0.0.1:8000/query" ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What is overfitting?\"}"
```

### Example response

```json
{
  "answer": "Overfitting happens when a model learns the training data too closely...",
  "sources": [
    "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow — Page 60",
    "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow — Page 59"
  ]
}
```

The exact generated answer and retrieved sources may vary depending on the retrieval results and LLM generation.

---

## 17. Interactive API Documentation

FastAPI automatically provides Swagger UI.

After starting the backend, open:

```text
http://127.0.0.1:8000/docs
```

From Swagger UI, you can test:

* `GET /health`
* `POST /query`

---

## 18. Running the Frontend

Open another terminal.

Move to the frontend directory:

```powershell
cd frontend
```

Run Streamlit:

```bash
python -m streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

The frontend provides a chat-style interface where users can:

1. Enter a study question.
2. Send the question to the FastAPI backend.
3. Wait while the RAG pipeline retrieves relevant information.
4. View the generated answer.
5. View the retrieved document sources.

---

# 19. Screenshots

The following screenshots demonstrate the system running end-to-end.

### Streamlit Application

Add the application screenshot here:

```photo

```

---
<img width="1280" height="672" alt="image" src="https://github.com/user-attachments/assets/7044b7b3-8bc8-4c81-a4fe-fee6778ab3b0" />


### FastAPI Swagger Documentation

Add the Swagger screenshot here:

<img width="1280" height="672" alt="image" src="https://github.com/user-attachments/assets/f6319b1d-b673-4fae-9a26-9b8b9dcaf691" />
<img width="1280" height="672" alt="image" src="https://github.com/user-attachments/assets/9fbbcfd4-e050-42cc-b8cd-528e96a6cb07" />



### RAG Evaluation

Add the evaluation output screenshot here:

<img width="1280" height="672" alt="image" src="https://github.com/user-attachments/assets/e9fd606b-668c-427e-948e-4523a7a95ec7" />


### Retrieval with Metadata

Add the retrieval output screenshot here:

<img width="1280" height="672" alt="image" src="https://github.com/user-attachments/assets/a6ec091e-b1f4-48c3-be34-1e2e9dfaea2f" />


## 20. Evaluation

The RAG system was evaluated using 10 questions covering different machine learning concepts.

The evaluation questions included:

1. What is overfitting?
2. What is the difference between supervised and unsupervised learning?
3. Explain linear regression.
4. What is the purpose of cross-validation?
5. What is the ROC curve used for?
6. What's the difference between OvR and OvO strategies?
7. What is a Random Forest?
8. What is a GAN?
9. What is Q-learning?
10. What is the bias/variance trade-off?

For every question, the system:

1. Retrieved the top relevant document chunks.
2. Retrieved source and page metadata.
3. Passed the retrieved context to the local LLM.
4. Generated a grounded answer.
5. Recorded the retrieved sources and generated answer.

The evaluation results were saved to:

<img width="960" height="504" alt="image" src="https://github.com/user-attachments/assets/012bb8b8-8e23-41c3-9e20-3ba9b77455a2" />
<img width="960" height="504" alt="image" src="https://github.com/user-attachments/assets/1315dc60-e672-4013-822a-e483876832c4" />
<img width="960" height="504" alt="image" src="https://github.com/user-attachments/assets/86e3ce66-8931-40bf-967a-b4f0c67543ab" />
<img width="960" height="504" alt="image" src="https://github.com/user-attachments/assets/bd3076ef-0b67-497b-bbe4-1ad6262056a4" />
<img width="960" height="504" alt="image" src="https://github.com/user-attachments/assets/2876f4b3-e2d0-4f19-afcd-3c5080c608a8" />





### Evaluation Summary

| Metric          | Result |
| --------------- | -----: |
| Total questions |     10 |
| Correct answers |     10 |
| Accuracy        |   100% |

The evaluation was based on manual inspection of the generated answers against the retrieved document context.

---

## 21. Retrieval Evaluation

A page-aware retrieval test was performed using ChromaDB.

The final collection contains:

```text
2,449 document chunks
```

Example retrieval result for:

```text
What is overfitting?
```

```text
Source:
Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow

Page: 60
Distance: 0.5688
```

The retrieved text directly discusses overfitting.

Additional retrieved pages included:

```text
Page 59
Distance: 0.7698
```

and:

```text
Page 164
Distance: 0.7949
```

This demonstrates that the retrieval system can identify semantically related content and preserve page-level source information.

---

## 22. Out-of-Domain Behavior

The system was also tested with a question outside the knowledge contained in the study documents.

Example:

```text
Who is the current president of France?
```

The system responded:

```text
I don't have enough information in the documents to answer that.
```

This behavior is intentional.

The RAG pipeline is designed to prioritize retrieved document context rather than allowing the LLM to freely answer using information outside the provided knowledge base.

---

## 23. Failure Cases and Mitigation

RAG systems can fail when the relevant information is not retrieved or when the retrieved context is insufficient.

Potential failure cases include:

### 23.1 Irrelevant Retrieval

The vector database may return chunks that are semantically related but do not directly answer the question.

Mitigation:

* Improve chunking strategy.
* Tune chunk size and overlap.
* Adjust the number of retrieved chunks.
* Evaluate alternative embedding models.
* Improve retrieval thresholds.

### 23.2 Insufficient Context

If the required information is not present in the retrieved chunks, the LLM may not have enough information to answer.

Mitigation:

The generation prompt explicitly instructs the model to avoid unsupported answers and return:

```text
I don't have enough information in the documents to answer that.
```

### 23.3 Out-of-Domain Questions

Questions unrelated to the document collection should not be answered using the model's general knowledge.

Mitigation:

The system uses retrieved context as the knowledge source and can refuse to answer when sufficient supporting information is unavailable.

### 23.4 Metadata Retrieval

Incorrect or missing metadata could make source citation unreliable.

Mitigation:

Each document chunk stores source and page metadata during ingestion, allowing the retrieval layer to return the original document and page information.

---

## 24. Backend Testing

The backend includes automated tests using Pytest and FastAPI's TestClient.

The tests cover:

### Happy Path

A valid question is submitted to:

```text
POST /query
```

The test verifies that the endpoint successfully returns a response.

### Invalid Input

An empty or invalid question is submitted.

The API is expected to return:

```text
422 Unprocessable Entity
```

Run the tests with:

```bash
pytest
```

---

## 25. Security and Configuration

Sensitive environment variables are not committed to GitHub.

The `.gitignore` excludes:

```text
.env
backend/.env
frontend/.env
.venv/
__pycache__/
*.pyc
*.log
```

The project uses `.env.example` files to document the required configuration without exposing private environment values.

---

## 26. Docker

The backend includes a Dockerfile for containerized deployment.

Build the backend image:

```bash
docker build -t rag-study-assistant-backend ./backend
```

Run the container:

```bash
docker run -p 8000:8000 rag-study-assistant-backend
```

The Ollama service must also be accessible to the container when using local LLM generation.

---

## 27. Reproducibility

The complete RAG pipeline is implemented in:

```text
notebooks/rag_pipeline.ipynb
```

The notebook contains the main stages required to reproduce the system:

1. Load and inspect the source documents.
2. Process the document pages.
3. Chunk the content.
4. Generate embeddings.
5. Create the ChromaDB collection.
6. Store document metadata.
7. Test semantic retrieval.
8. Evaluate the RAG pipeline using 10 questions.
9. Save the evaluation results.
10. Persist the vector store for backend use.

The notebook is designed to run from top to bottom.

---

## 28. Future Improvements

Possible future improvements include:

* Adding more study documents.
* Supporting multiple document formats.
* Improving chunking strategies.
* Adding hybrid keyword and semantic retrieval.
* Adding reranking models.
* Adding conversation memory.
* Adding document upload functionality.
* Adding authentication.
* Adding streaming LLM responses.
* Adding more extensive automated RAG evaluation.
* Adding a larger evaluation dataset.
* Adding deployment to a cloud platform.

---

## 29. Project Goal

The main goal of this project is to demonstrate a complete Retrieval-Augmented Generation workflow:

```text
Documents
    ↓
Document Processing
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Semantic Retrieval
    ↓
Retrieved Context
    ↓
Ollama / Llama 3.2
    ↓
Grounded Answer
    ↓
FastAPI
    ↓
Streamlit
```

The project combines information retrieval, vector databases, embeddings, local LLM inference, API development, and frontend development into one complete AI application.

---

## 30. Author 

**Rawan Mahmoud & Roaa Hatem **

AI Student and Applied AI Developer

GitHub:

https://github.com/RawanMahmoud30

https://github.com/roaahatem10

Project Repository:

https://github.com/RawanMahmoud30/rag-assistant-project

https://github.com/roaahatem10/rag-assistant-project.git

---

## 31. License

This project was developed as an educational graduation project for the Level 2 Summer Training program.

The source document used for the RAG knowledge base is referenced for educational retrieval purposes.
