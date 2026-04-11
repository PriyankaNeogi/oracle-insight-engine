from sec_edgar_downloader import Downloader
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass


def download_10k(company: str):
    """
    Downloads latest 10-K filing for a given company ticker
    """

    # Priority: .env → fallback to hardcoded email
    email = os.getenv("SEC_EMAIL", "pn13.ece@gmail.com")

    download_path = os.path.join("data", "raw")

    # Ensure directory exists
    os.makedirs(download_path, exist_ok=True)

    # Initialize downloader
    dl = Downloader(download_path, email_address=email)

    print(f"[INFO] Downloading 10-K for {company} using {email}...")
    
    try:
        dl.get("10-K", company, limit=1)
        print("[SUCCESS] Download complete!")
    except Exception as e:
        print("[ERROR] Download failed:", str(e))
        raise