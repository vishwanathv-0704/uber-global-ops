from pathlib import Path
import re


def clean_text(text):
    """Clean policy text while preserving useful structure."""

    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def load_policy_documents(policy_dir="data/airport_policies"):
    """Load all Markdown policy documents."""

    documents = []

    policy_path = Path(policy_dir)

    for file_path in sorted(policy_path.glob("*.md")):

        raw_text = file_path.read_text(encoding="utf-8")
        cleaned_text = clean_text(raw_text)

        documents.append({
            "text": cleaned_text,
            "metadata": {
                "source": file_path.name,
                "airport": file_path.name.split("_")[0].upper(),
                "policy_type": file_path.stem.split("_", 1)[1]
            }
        })

    return documents
