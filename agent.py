import os
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
from docx import Document as WordDocument

# Project paths
BASE_DIR = Path(__file__).resolve().parent
RESEARCH_DIR = BASE_DIR / "research_pack"
OUTPUT_DIR = BASE_DIR / "outputs"
PROMPT_FILE = BASE_DIR / "system_prompt.md"

SUPPORTED_EXTENSIONS = {
    ".pdf", ".txt", ".md", ".docx", ".html", ".htm", ".csv"
}

def extract_text(file_path):
    """Extract readable text from supported document types."""
    extension = file_path.suffix.lower()

    try:
        if extension == ".pdf":
            reader = PdfReader(str(file_path))
            return "\n".join(
                page.extract_text() or "" for page in reader.pages
            )

        if extension == ".docx":
            document = WordDocument(str(file_path))
            return "\n".join(p.text for p in document.paragraphs)

        content = file_path.read_text(
            encoding="utf-8", errors="ignore"
        )

        if extension in {".html", ".htm"}:
            content = re.sub(
                r"(?is)<(script|style).*?>.*?</\1>", " ", content
            )
            content = re.sub(r"(?s)<[^>]+>", " ", content)

        return content

    except Exception as error:
        print(f"Could not read {file_path.name}: {error}")
        return ""


def load_research_documents():
    """Read documents and assign source IDs."""
    documents = []

    for file_path in sorted(RESEARCH_DIR.rglob("*")):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        content = extract_text(file_path).strip()

        if not content:
            print(f"Warning: No readable text in {file_path.name}")
            continue

        source_id = f"S{len(documents) + 1}"

        documents.append({
            "id": source_id,
            "filename": file_path.name,
            "content": content[:30000],
        })

    return documents


def build_document_context(documents):
    """Format documents so the model can reference them."""
    sections = []

    for document in documents:
        sections.append(
            f"\n--- SOURCE [{document['id']}] ---\n"
            f"Filename: {document['filename']}\n"
            f"Document content:\n{document['content']}\n"
        )

    return "\n".join(sections)


def generate_brief(ticker, documents, prompt_version):
    """Ask Gemini to produce the research brief."""
    system_prompt = PROMPT_FILE.read_text(encoding="utf-8")
    context = build_document_context(documents)

    client = genai.Client(
        api_key=os.environ["GEMINI_API_KEY"]
    )

    prompt = f"""
{system_prompt}

Ticker: {ticker}
Assumed current date: 23 September 2026.

DESIGN VARIATION:
{prompt_version}

Use only the supplied documents. Do not browse the web.
The company in this test case is fictional.

For each source, use its actual filename and inspect the
document's opening metadata for source URL and publication date.
Never invent missing source details.

RESEARCH DOCUMENTS:
{context}

Return only the final Markdown research brief.
"""

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt,
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text.strip()


def main():
    load_dotenv(BASE_DIR / ".env")

    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    if not RESEARCH_DIR.exists():
        raise FileNotFoundError(
            f"Research folder not found: {RESEARCH_DIR}"
        )

    documents = load_research_documents()

    if not documents:
        raise RuntimeError(
            "No readable research documents found. "
            "Check the research_pack folder and file types."
        )

    print(f"\nLoaded {len(documents)} documents.")

    if len(documents) != 8:
        print(
            "Warning: The assignment expects 8 documents. "
            "Check whether any files were missed or unsupported."
        )

    OUTPUT_DIR.mkdir(exist_ok=True)

    variations = [
        (
            "run1_baseline.md",
            "Baseline: create a balanced brief with inline source IDs."
        ),
        (
            "run2_citations.md",
            "Prioritize traceability. Cite each factual claim and "
            "financial figure immediately with source IDs."
        ),
        (
            "run3_conflicts.md",
            "Compare sources carefully. Identify conflicting numbers, "
            "outdated information, missing periods, and unsupported "
            "claims. Explain important uncertainties."
        ),
    ]

    for filename, variation in variations:
        print(f"\nGenerating {filename}...")

        try:
            brief = generate_brief(
                "SRVCABLE", documents, variation
            )

            output_path = OUTPUT_DIR / filename
            output_path.write_text(
                brief + "\n", encoding="utf-8"
            )

            print(f"Saved to: {output_path}")
            print("\n" + brief + "\n")

        except Exception as error:
            print(f"Generation failed: {error}")
            print(
                "Check your API key, model availability, "
                "internet connection, and API quota."
            )


if __name__ == "__main__":
    main()
