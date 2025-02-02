from gpt4all import GPT4All

class GPT4AllService:
    def __init__(self, model_path: str, device="cpu"):
        try:
            available_gpus = GPT4All.list_gpus()
            print(f"Detected GPUs: {available_gpus}")
            device = "gpu" if available_gpus else device
        except ValueError:
            print("No compatible GPUs found - falling back to CPU")
            device = "cpu"
        
        self.model = GPT4All(model_path, device=device)

    def generate_description(self, prompt: str) -> str:
        response = self.model.generate(prompt, max_tokens=300)
        return response
    
    async def initialize(self):
        # If there's any async initialization needed, put it here
        pass
