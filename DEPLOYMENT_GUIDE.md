# DEPLOYMENT & GLOBAL READINESS GUIDE

**Application Name:** E-Waste Intelligence System / E-Waste AI  
**Author:** Azhar Fareed Mulla (USN: 2SA25MC002) | Guide: Dr. Nisha S Amin  
**Live URL:** https://ewaste-ai-azhar.streamlit.app/  
**Source Repository:** https://github.com/azharlionkgf/ewaste-ai  

---

## 1. Environment & Runtime Specifications
- **Python Version:** 3.12 (Recommended for Streamlit Cloud)
- **Main Entrypoint:** `app/streamlit_app.py`
- **Dependencies:** Managed via `requirements.txt` (Pinned to compatible versions for headless cloud execution)

## 2. Streamlit Cloud Secrets Configuration
To enable the Google Gemini AI features (image analysis, multimodal parsing, conversational intelligence):
1. Navigate to [share.streamlit.io](https://share.streamlit.io).
2. Open the App Settings for `ewaste-ai`.
3. In the **Secrets** section, configure:
```toml
GEMINI_API_KEY = "your-google-gemini-api-key-here"
```
*Note: The platform is architected to operate fully offline if the secret is not provided; all 15 device models, 3D visualizations, and rule-based recovery engines function without API keys.*

## 3. Local Execution Instructions
To run the platform locally on Windows, Linux, or macOS:
```bash
# Clone the repository
git clone https://github.com/azharlionkgf/ewaste-ai.git
cd ewaste-ai

# Create virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run automated tests
python -m unittest tests/test_platform.py

# Launch application
streamlit run app/streamlit_app.py
```

## 4. Security & Privacy Safeguards
- No API keys or passwords are committed to git (`.gitignore` protects `.env`, database cache, and credentials).
- Admin access uses SHA-256 hashed password verification.
- Uploaded images and documents are processed in memory and never stored without user intent.
- User data and files are strictly sandboxed.
