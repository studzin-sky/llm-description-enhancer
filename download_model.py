# This script is intended to be run in a Docker container with the Hugging Face token mounted as a secret.
from huggingface_hub import snapshot_download
from huggingface_hub.errors import HfHubHTTPError
import os
import sys
import traceback

def main():
    token_path = '/run/secrets/huggingface_token'
    model_dir_path = os.environ.get('MODEL_DIR')
    repo_id_to_download = 'speakleash/Bielik-1.5B-v3.0-Instruct'

    print(f'--- Python SCRIPT DEBUG: Target model directory: {model_dir_path}')
    if not model_dir_path:
        print('--- Python SCRIPT CRITICAL ERROR: MODEL_DIR environment variable not set!')
        sys.exit(1)

    token_value = None
    try:
        with open(token_path, 'r') as f:
            token_value = f.read().strip()
        print(f'--- Python SCRIPT DEBUG: Token file {token_path} read successfully.')
        if token_value:
            masked_token = f"{token_value[:4]}****{token_value[-4:] if len(token_value) > 4 else '(token too short)'}"
            print(f'--- Python SCRIPT DEBUG: Token content (masked): {masked_token}')
            if not token_value.startswith('hf_'):
                print('--- Python SCRIPT WARNING: Token does not appear to start with hf_! Check token file content.')
        else:
            print('--- Python SCRIPT CRITICAL ERROR: Token file was empty or only whitespace!')
            sys.exit(1)
    except FileNotFoundError:
        print(f'--- Python SCRIPT CRITICAL ERROR: Token secret file {token_path} not found! Ensure --mount is correct.')
        sys.exit(1)
    except Exception as e:
        print(f'--- Python SCRIPT CRITICAL ERROR: Could not read token from {token_path}: {e}')
        traceback.print_exc()
        sys.exit(1)

    try:
        print(f'--- Python SCRIPT INFO: Calling snapshot_download for {repo_id_to_download}...')
        snapshot_download(
            repo_id=repo_id_to_download,
            local_dir=model_dir_path,
            token=token_value,
            local_dir_use_symlinks=False,
            resume_download=True
            # Removed ignore_patterns for now to ensure no interference
        )
        print(f'--- Python SCRIPT INFO: snapshot_download completed for {repo_id_to_download}.')
    except HfHubHTTPError as http_e:
        print(f'--- Python SCRIPT ERROR: HfHubHTTPError during snapshot_download: {http_e}')
        if http_e.response is not None:
            print(f'--- Python SCRIPT ERROR: Response status: {http_e.response.status_code}')
            print(f'--- Python SCRIPT ERROR: Response headers: {http_e.response.headers}')
            try:
                response_content = http_e.response.content.decode()
            except UnicodeDecodeError:
                response_content = str(http_e.response.content)
            print(f'--- Python SCRIPT ERROR: Response content: {response_content}')
        if http_e.request_id:
            print(f'--- Python SCRIPT ERROR: Request ID: {http_e.request_id}')
        sys.exit(1)
    except Exception as e:
        print(f'--- Python SCRIPT ERROR: Other Exception during snapshot_download: {e}')
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()