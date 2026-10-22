# AI-Powered C-Ring Inspector

A Python-based AI automation project that uses Google's Gemini API to inspect metallic C-ring images for potential defects and generate structured quality inspection results.

## Problem Statement

Manual inspection of individual C-rings can be tedious and time-consuming. This project explores how AI can help automate visual quality checks and reduce repetitive inspection work.

## Features

- **AI-powered inspection:** Analyze C-ring images for potential defects.
- **Defect detection:** Identify scratches, dents, burrs, deformation, corrosion, and other visible defects.
- **Severity classification:** Categorize defects as LOW, MEDIUM, HIGH, or CRITICAL.
- **Inspection summary:** Generate a PASS/FAIL status, confidence score, and recommended action.
- **Structured output:** Validate inspection results using Pydantic.

## Tech Stack

- Python
- Google Gemini API
- Pillow (PIL)
- Pydantic

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

### 2. Install dependencies

```bash
pip install google-genai pillow pydantic
```

### 3. Configure your API key

Set your Gemini API key as an environment variable.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="your-api-key"
```

Ensure your Python code reads the environment variable:

```python
client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)
```

### 4. Run the application

Update the image path in `ringInspector.py` to point to your C-ring image, then run:

```bash
python ringInspector.py
```

## Example Output

```text
=== INSPECTION REPORT ===
Status:         PASS
Confidence:     95.00%
Action:         Accept
Summary:        No significant visible defects detected.

No defects detected. Part meets quality standards.
```

*Example output only; actual results depend on the image and AI model response.*

## Future Improvements

- Process multiple images from a folder.
- Generate consolidated inspection reports in CSV or Excel.
- Visualize detected defects using bounding boxes.
- Evaluate inspection accuracy against expert assessments.

## Disclaimer

This project is a prototype for AI-assisted visual inspection. Results should be validated by qualified personnel before being used for actual industrial quality-control decisions.
