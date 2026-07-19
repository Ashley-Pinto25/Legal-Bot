from pathlib import Path

from src.retriever import get_retriever
from src.prompts import RAG_PROMPT
from src.gemini import generate_response


# Initialize the retriever once
retriever = get_retriever()


def ask(question: str):
    """
    Retrieves relevant documents, builds the prompt,
    sends it to Gemini, and appends deterministic citations.
    """

    # Retrieve relevant documents
    docs = retriever.invoke(question)

    if not docs:
        return "I couldn't find that information in the knowledge base."

    # Build context for Gemini
    context_parts = []

    # Build citations for the final answer
    citations = []

    seen = set()

    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "Unknown")

        path = Path(source)

        department = path.parent.name if path.parent.name else "General"
        pdf_name = path.name

        context_parts.append(
            f"""
Department: {department}
PDF: {pdf_name}
Page: {page}

Content:
{doc.page_content}
"""
        )

        citation = f"{department}: {pdf_name} - Pg. No. {page + 1}"

        if citation not in seen:
            seen.add(citation)
            citations.append(citation)

    context = "\n\n".join(context_parts)

    # Create prompt
    prompt = RAG_PROMPT.format(
        context=context,
        question=question
    )

    # Generate answer
    answer = generate_response(prompt).strip()

    # If Gemini couldn't answer, return immediately
    if "couldn't find" in answer.lower():
        return answer

    # Append citations
    if citations:
        answer += "\n\nSources:\n"

        for citation in citations:
            answer += f"• {citation}\n"

    return answer