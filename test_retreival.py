from src.vector_store import retrieve_documents


queries = [
    "What is the maximum surge multiplier allowed at SFO?",
    "Can drivers abandon the airport queue?",
    "What approval is required before increasing surge?",
    "What is the completion rate threshold at LAX?",
    "What are the pickup rules at JFK?"
]


for query in queries:

    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)

    results = retrieve_documents(query, top_k=3)

    for rank, result in enumerate(results, start=1):

        print(f"\n--- Result {rank} ---")
        print("Source:", result["metadata"]["source"])
        print("Airport:", result["metadata"]["airport"])
        print("Policy Type:", result["metadata"]["policy_type"])
        print("Distance:", round(result["distance"], 4))
        print("Text:")
        print(result["text"][:500])
