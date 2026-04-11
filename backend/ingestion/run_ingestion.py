import os
import json

from backend.ingestion.sec_downloader import download_10k
from backend.ingestion.sec_parser import extract_full_text, extract_risk_factors
from backend.processing.chunker import chunk_text


def get_latest_file() -> str:
    """
    Locate the latest SEC filing file
    """

    base_path = "sec-edgar-filings"

    if not os.path.exists(base_path):
        raise FileNotFoundError(f"SEC filings directory not found: {base_path}")

    all_files = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".html") or file.endswith(".txt"):
                all_files.append(os.path.join(root, file))

    if not all_files:
        raise FileNotFoundError("No SEC filing files found")

    latest_file = sorted(all_files)[-1]

    return latest_file


def run(company: str) -> None:
    """
    Full ingestion pipeline:
    1. Download SEC filing
    2. Locate latest file
    3. Extract full text
    4. Extract Risk Factors
    5. Chunk text
    6. Save structured output
    """

    print("Starting ingestion pipeline")

    # Step 1: Download
    try:
        print(f"Downloading 10-K for {company}")
        download_10k(company)
    except Exception as e:
        print(f"Download failed. Using existing files. Error: {e}")

    # Step 2: Locate file
    file_path = get_latest_file()
    print(f"Using filing: {file_path}")

    # Step 3: Extract full text
    full_text = extract_full_text(file_path)

    if not full_text or len(full_text) < 100:
        raise ValueError("Extracted text is empty or too small")

    # Step 4: Extract Risk Factors
    risk_factors = extract_risk_factors(full_text)

    # Step 5: Chunk text
    chunks = chunk_text(risk_factors)

    # Step 6: Save output
    os.makedirs("data/processed", exist_ok=True)

    output = {
        "company": company,
        "source_file": file_path,
        "num_chunks": len(chunks),
        "chunks": chunks[:10]  # limit for now
    }

    output_path = os.path.join("data", "processed", f"{company}.json")

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Saved processed data to {output_path}")


if __name__ == "__main__":
    run("AAPL")