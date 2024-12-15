import uvicorn
from fastapi import FastAPI, File, UploadFile
import pandas as pd 
import numpy as np 
import pickle
from fastapi.responses import JSONResponse
from PIL import Image
import io

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Chilli Leaf Prediction ML API'}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        health_status = ""
        disease=""
        recommendation = ""
        # Read the uploaded image file
        
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Preprocess the image (resize, normalize, etc.)
        image = image.resize((256, 256))  # Example resize
        image_array = np.array(image) / 255.0  # Normalize to [0, 1]

        
        # Convert to model's input shape (e.g., add batch dimension if needed)
        # Adjust preprocessing based on your model
        
        with open('HealthyOrDiseaseModel.pkl', 'rb') as file:
            model1 = pickle.load(file)

        with open('disease_model.pkl', 'rb') as file:
            model2 = pickle.load(file)
        print("29 succefully")
        model_input = np.expand_dims(image_array, axis=0)
        print("Model Loaded succefully")
        # Perform prediction
        prediction1 = model1.predict(model_input)
        print(prediction1[0][0])
        if prediction1[0][0]<prediction1[0][1]:
                print("Healthy Plant")
                health_status = "Healthy Leaf"
        else:
             print("Unhealthy Plant")
             health_status = "Unhealthy Leaf"
             prediction2 = model2.predict(model_input)
             
             pred_arr = prediction2[0]
             print(pred_arr)
             print(type(pred_arr))
             max_index = max_index = np.argmax(pred_arr)
             print(max_index)
        match max_index:
            case 0 :
                  disease = "Anthracnose"
                  recommendation="Carbendazim 50% WP: Effective at 0.1 spray.\n Mancozeb 75% WP: Use at 2.5 g per liter of water.\n Azoxystrobin 23% SC: Apply as a foliar spray.\n Chlorothalonil 75% WP: Broad-spectrum fungicide."
            case 1 :
                  disease = "Cercospora Leaf Spot (Cercospora capsici)(frog - eye)"
                  recommendation="Copper Oxychloride 50% WP: Use at 3 g per liter of water.\n Mancozeb 75% WP: Effective against Cercospora spp.\n Propiconazole 25% EC: Systemic fungicide; use at 1 ml per liter. "
            case 3 :
                  disease = "Chilli Leaf Curl Disease"
                  recommendation="Control whiteflies (primary vector) using insecticides like Imidacloprid 17.8% SL or Spirotetramat 150 OD.\nPesticides:\nNeem-based products: Use neem oil (1-2%) for vector management.\nAbamectin 1.8% EC: Effective against whiteflies."
            case 4 :
                  disease = "Powdery Mildew (Leveillula taurica)"
                  recommendation="Sulfur 80% WG: Dust or spray at recommended doses.\nPenconazole 10% EC: Use at 1 ml per liter of water.\nTriadimefon 25% WP: Effective systemic fungicide.\n"
            case 5 :
                  disease = "Bacterial Spot (Xanthomonas campestris pv. vesicatoria)"
                  recommendation="Copper-based fungicides: Like Copper Hydroxide 77% WP or Copper Oxychloride 50% WP.\nStreptomycin Sulfate 9% + Tetracycline Hydrochloride 1% SP: Use as a foliar spray.\nPreventive Measures:\nUse resistant varieties and ensure proper sanitation of tools."
            case 6 :
                  disease = "Chilli Veinal Mottle Virus"
                  recommendation="Prevention:\nUse virus-free seeds or resistant varieties.\nControl aphid populations (the primary vectors) using insecticides like Imidacloprid 17.8% SL or Thiamethoxam 25% WG.\nPesticides:\nNeem Oil (1-2%): Acts as a repellent for aphids.\nPymetrozine 50% WG: Controls aphid vectors effectively.\n"
        
                  
        
        # Create a response with the prediction result
        response = {
            "message": "Prediction Leaf Aid API",
            "prediction": health_status,
            "disease":disease,
            "recommendation":recommendation
        }
        print(response)

        return JSONResponse(content=response)

    except Exception as e:
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"}, status_code=500
        )


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)