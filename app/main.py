from fastapi import FastAPI, HTTPException
from app.models.huggingface_service import HuggingFaceTextGenerationService
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.schemas import CarData, EnhancedDescriptionResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH_IN_CONTAINER = "/app/pretrain_model"
hf_service = HuggingFaceTextGenerationService(
    model_name_or_path=MODEL_PATH_IN_CONTAINER,
    device="cpu"
)


@app.on_event("startup")
async def startup_event():
    print("Starting up and initializing HuggingFace service...")
    try:
        await hf_service.initialize()
        print(f"HuggingFace service initialized successfully from {MODEL_PATH_IN_CONTAINER}.")
    except HTTPException as e:
        print(f"Failed to initialize HuggingFace service: {e.detail}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during HuggingFace service initialization: {e}")
        raise


@app.get("/health")
async def health_check():
    return {"status": "ok", "model_initialized": hf_service.pipeline is not None}

@app.post("/enhance-description", response_model=EnhancedDescriptionResponse)
async def enhance_description(car_data: CarData):
    chat_messages = [
        {
            "role": "system",
            "content": (
                "Jesteś pomocnym asystentem AI. Twoim zadaniem jest tworzenie krótkich, "
                "atrakcyjnych opisów marketingowych samochodów na podstawie dostarczonych danych. "
                "Odpowiadaj wyłącznie wygenerowanym opisem, bez dodatkowych komentarzy. "
                "Staraj się, aby opis był zwięzły i kompletny, idealnie mieszcząc się w około 100-120 słowach, " 
                "i zawsze kończył się pełnym zdaniem." 
            )
        },
        {
            "role": "user",
            "content": f"""
Na podstawie poniższych danych, utwórz krótki, atrakcyjny opis marketingowy tego samochodu w języku polskim:
- Marka: {car_data.make}
- Model: {car_data.model}
- Rok produkcji: {car_data.year}
- Przebieg: {car_data.mileage} km
- Wyposażenie: {', '.join(car_data.features)}
- Stan: {car_data.condition}
"""
        }
    ]
    
    try:
        description = await hf_service.generate_text(
            prompt_text=None,
            chat_template_messages=chat_messages,
            max_new_tokens=150, 
            temperature=0.75,
            top_p=0.9,
        )
        return {"description": description.strip()}
    except HTTPException:
        raise 
    except Exception as e:
        print(f"Unexpected error in /enhance-description: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")