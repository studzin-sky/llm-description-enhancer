from fastapi import FastAPI, HTTPException
from app.models.gpt4all import GPT4AllService
from app.schemas.schemas import CarData, EnhancedDescriptionResponse

app = FastAPI()

# Initialize GPT4All service
gpt4all_service = GPT4AllService("Meta-Llama-3-8B-Instruct.Q4_0.gguf", device="cpu")

@app.on_event("startup")
async def startup_event():
    await gpt4all_service.initialize()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/enhance-description", response_model=EnhancedDescriptionResponse)
def enhance_description(car_data: CarData):
    try:
        # Create a prompt from car data
        prompt = f"""
        Create a short description of this car:
        - Make: {car_data.make}
        - Model: {car_data.model}
        - Year: {car_data.year}
        - Mileage: {car_data.mileage}
        - Features: {', '.join(car_data.features)}
        - Condition: {car_data.condition}
        """
        # Generate description
        description = gpt4all_service.generate_description(prompt)
        return {"description": description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
