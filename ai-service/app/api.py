from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import ProcessRequest, Question
from app.services import process_document
from app.retriever import retrieve
from app.gemini_service import ask_gemini
from app.query import search_graph
from app.entity_extractor import extract_question_entities

app = FastAPI()

# ------------------ CORS ------------------ #

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ Home ------------------ #

@app.get("/")
def home():
    return {
        "message": "Industrial Knowledge AI is running!"
    }

# ------------------ Process Document ------------------ #

@app.post("/process")
def process(request: ProcessRequest):

    try:

        process_document(
            request.documentId,
            request.chunks
        )

        return {
            "status": "success",
            "chunksIndexed": len(request.chunks)
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }

# ------------------ Ask AI ------------------ #

@app.post("/ask")
def ask(question: Question):

    try:

        # ---------------- Validation ---------------- #

        if not question.question.strip():
            return {
                "error": "Question cannot be empty."
            }

        print("\n==============================")
        print("Question:", question.question)

        # ---------------- Vector Retrieval ---------------- #

        results = retrieve(question.question)

        documents = results["documents"][0]

        vector_context = "\n\n".join(documents)

        print("\n----- VECTOR CONTEXT -----")
        print(vector_context[:500])   # print first 500 chars

        # ---------------- Graph Retrieval ---------------- #

        graph_context = ""

        entities = extract_question_entities(question.question)

        print("\nExtracted Entities:", entities)

        for entity in entities:

            print(f"\nSearching graph for: {entity}")

            graph_results = search_graph(entity)

            print("Graph Results:", graph_results)

            if graph_results:

                graph_context += f"\nKnowledge about {entity}:\n"

                for row in graph_results:

                    graph_context += (
                        f'{row["source"]} '
                        f'--{row["relation"]}--> '
                        f'{row["target"]}\n'
                    )

        print("\n----- GRAPH CONTEXT -----")
        print(graph_context if graph_context else "No graph context found.")

        # ---------------- Final Context ---------------- #

        final_context = vector_context

        if graph_context.strip():
            final_context += "\n\n" + graph_context

        print("\n----- FINAL CONTEXT -----")
        print(final_context[:1000])

        # ---------------- Gemini ---------------- #

        answer = ask_gemini(
            question.question,
            final_context
        )

        print("\n----- GEMINI ANSWER -----")
        print(answer)

        return {
            "question": question.question,
            "answer": answer
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            "error": str(e)
        }