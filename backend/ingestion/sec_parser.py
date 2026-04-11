from bs4 import BeautifulSoup
import re


def extract_full_text(file_path: str) -> str:
    """
    Extract full clean text from SEC filing (HTML or TXT)
    """

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Parse using BeautifulSoup (works for HTML + TXT)
    soup = BeautifulSoup(content, "lxml")
    text = soup.get_text(separator=" ", strip=True)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)

    return text


def extract_risk_factors(text: str) -> str:
    """
    Robust extraction of Item 1A Risk Factors section

    Handles:
    - Table of Contents false matches
    - Multiple occurrences of Item 1A
    - Different SEC formatting styles
    - Cleans page headers and noise
    """

    # Normalize text
    text = re.sub(r'\s+', ' ', text)

    # Main pattern
    pattern = re.compile(
        r"item\s+1a[\.\:\-\s]*risk\s+factors(.*?)(item\s+1b|item\s+2)",
        re.IGNORECASE
    )

    matches = pattern.findall(text)

    if matches:
        # Extract candidates
        candidates = [m[0] for m in matches]

        # Choose longest match (real section, not TOC)
        best_match = max(candidates, key=len)

        # --- CLEANING STEP ---

        # Remove page headers like "Apple Inc. | 2025 Form 10-K | 5"
        best_match = re.sub(
            r"Apple Inc\.\s*\|\s*\d{4}\s*Form\s*10-K\s*\|\s*\d+",
            "",
            best_match
        )

        # Remove extra whitespace again
        best_match = re.sub(r'\s+', ' ', best_match)

        return best_match.strip()

    # --- FALLBACK (in case main pattern fails) ---
    fallback_pattern = re.compile(
        r"risk\s+factors(.*?)(unresolved\s+staff\s+comments|item\s+2)",
        re.IGNORECASE
    )

    fallback_match = fallback_pattern.search(text)

    if fallback_match:
        cleaned = fallback_match.group(1)

        cleaned = re.sub(
            r"Apple Inc\.\s*\|\s*\d{4}\s*Form\s*10-K\s*\|\s*\d+",
            "",
            cleaned
        )

        cleaned = re.sub(r'\s+', ' ', cleaned)

        return cleaned.strip()

    return "Risk Factors section not found"