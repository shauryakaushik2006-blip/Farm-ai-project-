[12:29 am, 8/9/2026] Shaurya kaushik: import io
import os
import torch
import torchvision.transforms as transforms
from fastapi import FastAPI, UploadFile, File, Form
from typing import List
from PIL import Image

app = FastAPI(title="Advanced Crop Disease API")

# 1. Image Preprocessing Pipeline for PyTorch
def transform_image(image_bytes):
    my_transforms = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return my_transforms(image).unsqueeze(0)

# 2. Simulated MySQL output based on your requirements
MOCK_DATABASE = {
    "Tomato_Early_Blight": {
        "en": {
            "name": "Tomato Early Blight (Tizón Temprano)",
            "symptoms": "Dark concentric rings forming target-like patterns on older leaves, yellowing halos.",
            "early": "1. Prune the lowest infected leaves immediately.\n2. Spray commercial fungicide 'Antracol' or 'Kavach' (Chlorothalonil).",
            "normal": "1. Improve plant spacing for airflow.\n2. Apply 'Amistar Top' (Azoxystrobin + Difenoconazole) to stop structural spreading.",
            "deep": "1. Destroy severely affected plants away from the field.\n2. Apply a heavy systemic cure like 'Ridomil Gold' immediately to save remaining yield."
        },
        "hi": {
            "name": "टमाटर अगेती झुलसा (Tomato Early Blight)",
            "symptoms": "पुरानी पत्तियों पर गोल छल्लेदार काले धब्बे बनना और पत्तियों का पीला पड़ना।",
            "early": "1. संक्रमित निचली पत्तियों को तुरंत काटकर हटा दें।\n2. बाजार से लाकर 'Antracol' या 'Kavach' (Chlorothalonil) फंगीसाइड का छिड़काव करें।",
            "normal": "1. पौधों के बीच हवा का प्रवाह सुधारने के लिए दूरी बढ़ाएं।\n2. बीमारी को फैलने से रोकने के लिए 'Amistar Top' का छिड़काव करें।",
            "deep": "1. गंभीर रूप से खराब पौधों को उखाड़कर खेत से दूर नष्ट कर दें।\n2. बची हुई फसल को बचाने के लिए तुरंत 'Ridomil Gold' का उपयोग करें।"
        }
    }
}

@app.post("/predict")
async def predict(
    files: List[UploadFile] = File(...), 
    lang: str = Form("en"),
    region: str = Form("North India"),
    crop_type: str = Form("Vegetable")
):
    # Process files through PyTorch pipeline
    for file in files:
        file_bytes = await file.read()
        # tensor_data = transform_image(file_bytes)
        
    predicted_class = "Tomato_Early_Blight"
    
    disease_info = MOCK_DATABASE.get(predicted_class, {}).get(lang, {
        "name": "Unknown Condition", "symptoms": "N/A", "early": "N/A", "normal": "N/A", "deep": "N/A"
    })
    
    return {
        "disease_code": predicted_class,
        "region_applied": region,
        "crop_type": crop_type,
        "details": disease_info
    }
