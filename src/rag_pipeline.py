import requests

from src.vector_store import retrieve_documents


OLLAMA_URL = "http://localhost:11434/api/generate"
LLM_MODEL = "qwen3:8b"


def build_context(documents):
    """
    Convert retrieved policy chunks into a context block.
    """
    #print("RETREIVED CONTEXT")
    #print(context)
    context_parts = []

    for i, doc in enumerate(documents, start=1):

        metadata = doc.get("metadata", {})

        source = metadata.get("source", "unknown")
        airport = metadata.get("airport", "unknown")
        policy_type = metadata.get("policy_type", "unknown")

        text = doc.get("text", "")

        context_parts.append(
            f"""
--- POLICY {i} ---
Source: {source}
Airport: {airport}
Policy Type: {policy_type}

{text}
"""
        )
    context="\n".join(context_parts)
    print("RETRIEVED CONTEXT")
    print(context)
    
    return context
    #return "\n".join(context_parts)


def build_prompt(question, context):
    """
    Create a strictly grounded RAG prompt.
    """

    return f"""
You are an airport operations policy assistant.

Answer the user's question using ONLY the exact information contained
in POLICY CONTEXT below.

STRICT RULES:
1. Do not use outside knowledge.
2. Do not infer, assume, or paraphrase into a new rule.
3. Only state facts that are explicitly supported by the context.
4. If the context does not explicitly answer the question, say:
   "The provided policies do not contain enough information to answer this."
5. If multiple policies are relevant, clearly distinguish them by airport
   and policy source.
6. Preserve numerical values exactly as written.
7. Keep the answer concise.
8. Mention the source policy that directly supports the answer.
9. Do not introduce terms that do not appear in the relevant policy unless
   they are necessary for basic grammar.

POLICY CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""
def generate_answer(question, top_k=3):

    # Step 1: Retrieve fewer relevant chunks
    documents = retrieve_documents(question, top_k=top_k)

    if not documents:
        return {
            "answer": "No relevant policy information was found.",
            "sources": []
        }

    # Step 2: Build context
    context = build_context(documents)

    # Step 3: Build grounded prompt
    prompt = build_prompt(question, context)

    # Step 4: Generate answer using Ollama
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "think":False,
        "options": {
            "temperature": 0.1,
            "num_predict": 200
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    result = response.json()

    answer = result.get("response", "").strip()

    # Step 5: Collect unique sources
    sources=[]
    
    for doc in documents:
        metadata=doc.get("metadata",{})
        source=metadata.get("source")
        if source and source not in sources:
            sources.append(source)
    return {
    "answer":answer,
    "sources":sources
    }
    

if __name__ == "__main__":

    print("=" * 70)
    print("AIRPORT POLICY RAG")
    print("=" * 70)

    question = input("\nEnter your question: ")

    try:

        result = generate_answer(question)

        print("\n" + "=" * 70)
        print("ANSWER")
        print("=" * 70)

        print(result["answer"])

        print("\n" + "=" * 70)
        print("SOURCES")
        print("=" * 70)

        for source in result["sources"]:
            print(f"- {source}")

    except Exception as e:

        print("\nERROR:")
        print(e)
