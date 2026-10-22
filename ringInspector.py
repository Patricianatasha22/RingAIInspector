import os
from enum import Enum
from typing import List
from PIL import Image
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# 1. Define the defect schema using Pydantic
class DefectSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class DefectItem(BaseModel):
    defect_type: str = Field(description="e.g. scratch, dent, burr, deformation, discoloration, corrosion")
    severity: DefectSeverity
    location: str = Field(description="Visual location on the C-ring (e.g., 'outer perimeter at 3 o'clock', 'inner edge notch')")
    box_2d: List[int] = Field(
        default_factory=list,
        description="Normalized bounding box coordinates [ymin, xmin, ymax, xmax] on a 0-1000 scale, if visible."
    )

class InspectionResult(BaseModel):
    status: str = Field(description="Must be 'PASS' if pristine with no defects or scratches, or 'FAIL' if defects are found.")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0")
    summary: str = Field(description="Brief summary of the visual condition of the C-ring.")
    defects: List[DefectItem] = Field(description="List of detected defects. Empty if status is PASS.")
    action_recommendation: str = Field(description="'Accept', 'Scrap', or 'Rework/Polish'")


# 2. Inspection function
def inspect_c_ring(image_path: str) -> InspectionResult:
    # Initialize the client (picks up GEMINI_API_KEY from environment)
    client = genai.Client(api_key= "")
    
    # Load image using Pillow
    img = Image.open(image_path)

    prompt = """
    You are an automated industrial optical quality control inspector for metallic C-rings.
    Inspect the provided image carefully for:
    - Scratches, gouges, or surface scoring
    - Edge burrs, notches, or chips
    - Ovality, warping, or dimensional deformation
    - Corrosion, pitting, discoloration, or foreign particulate contamination
    
    A "nice" C-ring (PASS) must be smooth, intact, uniform, and free of visible scratches and defects.
    If the defects detected only 1 low and 1 medium, let's just pass it
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=[img, prompt],
        config=types.GenerateContentConfig(
            temperature=0.1,  # Low temperature for deterministic, consistent QA inspection
            response_mime_type="application/json",
            response_schema=InspectionResult,
        ),
    )

    # Convert the validated JSON response into a Pydantic object
    result = InspectionResult.model_validate_json(response.text)
    return result


# 3. Example Execution
if __name__ == "__main__":
    test_image = r"C:\Users\Patricia\Desktop\Ring Inspector\Pass\master7.jpg" 
    
    if not os.path.exists(test_image):
        print(f"Please provide an image at '{test_image}' to run the inspection.")
    else:
        result = inspect_c_ring(test_image)
        
        print("\n=== INSPECTION REPORT ===")
        print(f"Status:         {result.status}")
        print(f"Confidence:     {result.confidence:.2%}")
        print(f"Action:         {result.action_recommendation}")
        print(f"Summary:        {result.summary}")
        
        if result.defects:
            print("\nDefects Detected:")
            for idx, defect in enumerate(result.defects, 1):
                print(f"  {idx}. [{defect.severity.value}] {defect.defect_type.upper()} at {defect.location}")
                if defect.box_2d:
                    print(f"     Bounding Box: {defect.box_2d}")
        else:
            print("\nNo defects detected. Part meets quality standards.")