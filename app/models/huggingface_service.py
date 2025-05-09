from transformers import pipeline, AutoTokenizer
import torch
from fastapi import HTTPException
import asyncio 

class HuggingFaceTextGenerationService:
    def __init__(self, model_name_or_path: str, device: str = None, task: str = "text-generation"):
        self.model_name_or_path = model_name_or_path
        self.task = task
        self.pipeline = None
        self.tokenizer = None

        if device is None:
            self.device_index = 0 if torch.cuda.is_available() else -1
        elif device == "cuda" and torch.cuda.is_available():
            self.device_index = 0
        elif device == "cpu":
            self.device_index = -1
        else:
            self.device_index = -1
        
        if self.device_index == 0:
            print("CUDA (GPU) is available. Using GPU.")
        else:
            print(f"Device set to use {'cpu' if self.device_index == -1 else f'cuda:{self.device_index}'}")


    async def initialize(self):
        try:
            print(f"Initializing Hugging Face pipeline for model: {self.model_name_or_path} on device index: {self.device_index}")
            self.tokenizer = await asyncio.to_thread(
                AutoTokenizer.from_pretrained, self.model_name_or_path, trust_remote_code=True
            )
            self.pipeline = await asyncio.to_thread(
                pipeline,
                self.task,
                model=self.model_name_or_path,
                tokenizer=self.tokenizer,
                device=self.device_index,
                torch_dtype=torch.bfloat16 if self.device_index != -1 and torch.cuda.is_available() and torch.cuda.is_bf16_supported() else torch.float32,
                trust_remote_code=True,
            )
            print(f"Pipeline for model {self.model_name_or_path} initialized successfully.")
        except Exception as e:
            print(f"Error initializing HuggingFace pipeline: {e}")
            raise HTTPException(status_code=503, detail=f"LLM (HuggingFace) model could not be loaded: {str(e)}")

    async def generate_text(self, prompt_text: str = None, chat_template_messages: list = None, max_new_tokens: int = 250, temperature: float = 0.7, top_p: float = 0.9, do_sample: bool = True, **kwargs) -> str:
        if not self.pipeline or not self.tokenizer:
            raise Exception("Pipeline is not initialized. Call initialize() first.")

        formatted_prompt_input = "" 
        if chat_template_messages:
            try:
                formatted_prompt_input = self.tokenizer.apply_chat_template(
                    chat_template_messages,
                    tokenize=False,
                    add_generation_prompt=True 
                )
            except Exception as e:
                print(f"Could not apply chat template, falling back to raw prompt if available. Error: {e}")
                if prompt_text:
                    formatted_prompt_input = prompt_text
                else:
                    raise ValueError("Cannot generate text without a valid prompt or chat_template_messages.")
        elif prompt_text:
            formatted_prompt_input = prompt_text
        else:
            raise ValueError("Either prompt_text or chat_template_messages must be provided.")

        try:
            generated_outputs = await asyncio.to_thread(
                self.pipeline,
                formatted_prompt_input, 
                max_new_tokens=max_new_tokens,
                do_sample=do_sample,
                temperature=temperature,
                top_p=top_p,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id if self.tokenizer.pad_token_id is None else self.tokenizer.pad_token_id, # Common setting
                **kwargs
            )
            
            if generated_outputs and isinstance(generated_outputs, list) and "generated_text" in generated_outputs[0]:
                full_generated_sequence = generated_outputs[0]["generated_text"]
                
                assistant_response = ""
                if full_generated_sequence.startswith(formatted_prompt_input):
                    assistant_response = full_generated_sequence[len(formatted_prompt_input):]
                else:
                    assistant_marker = "<|im_start|>assistant\n" 
                    last_marker_pos = full_generated_sequence.rfind(assistant_marker)
                    if last_marker_pos != -1:
                        assistant_response = full_generated_sequence[last_marker_pos + len(assistant_marker):]
                        print("Warning: Used fallback parsing for assistant response.")
                    else:
                        print("Error: Could not isolate assistant response from the full generated sequence.")
                        assistant_response = full_generated_sequence 

                if assistant_response.endswith("<|im_end|>"):
                    assistant_response = assistant_response[:-len("<|im_end|>")]
                
                return assistant_response.strip() 
            else:
                print(f"Unexpected output format from pipeline: {generated_outputs}")
                return "Error: Could not parse generated text from pipeline output."

        except Exception as e:
            print(f"Error during text generation with {self.model_name_or_path}: {e}")
            raise HTTPException(status_code=500, detail=f"Error generating text: {str(e)}")

