import os
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote
import gradio as gr
from pyngrok import ngrok


CHUNK_SIZE = 1638400
TOKEN_FILE = Path.home() / '.civitai' / 'config'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

def get_token(args_token: str):
    if args_token:
        store_token(args_token)
        return args_token
    try:
        with open(TOKEN_FILE, 'r') as file:
            return file.read().strip()
    except Exception:
        return prompt_for_civitai_token()

def store_token(token: str):
    TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TOKEN_FILE, 'w') as file:
        file.write(token)

def prompt_for_civitai_token():
    token = input('Please enter your CivitAI API token: ')
    store_token(token)
    return token

def download_file(url: str, output_path: str, token: str):
    headers = {
        'Authorization': f'Bearer {token}',
        'User-Agent': USER_AGENT,
    }

    class NoRedirection(urllib.request.HTTPErrorProcessor):
        def http_response(self, request, response):
            return response
        https_response = http_response

    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener(NoRedirection)
    response = opener.open(request)

    if response.status in [301, 302, 303, 307, 308]:
        redirect_url = response.getheader('Location')
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        content_disposition = query_params.get('response-content-disposition', [None])[0]

        if content_disposition:
            filename = unquote(content_disposition.split('filename=')[1].strip('"'))
        else:
            filename = os.path.basename(parsed_url.path)

        response = urllib.request.urlopen(redirect_url)
    elif response.status == 404:
        raise Exception('File not found')
    else:
        raise Exception('No redirect found, something went wrong')

    total_size = response.getheader('Content-Length')
    if total_size is not None:
        total_size = int(total_size)

    output_file = os.path.join(output_path, filename)

    with open(output_file, 'wb') as f:
        downloaded = 0
        start_time = time.time()

        while True:
            chunk_start_time = time.time()
            buffer = response.read(CHUNK_SIZE)
            if not buffer:
                break

            downloaded += len(buffer)
            f.write(buffer)
            chunk_time = time.time() - chunk_start_time
            if chunk_time > 0:
                speed = len(buffer) / chunk_time / (1024 ** 2)
            if total_size is not None:
                progress = downloaded / total_size
                sys.stdout.write(f'\rDownloading: {filename} [{progress*100:.2f}%] - {speed:.2f} MB/s')
                sys.stdout.flush()

    return f'\nDownload completed. File saved as: {output_file}\nDownloaded in {time.time() - start_time:.2f} seconds', output_file

def civitai_downloader(url, output_path, token):
    token = get_token(token)
    try:
        result, output_file = download_file(url, output_path, token)
        return result, output_file
    except Exception as e:
        return f'ERROR: {e}', None

# Gradio UI
def launch_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# CivitAI Model Downloader")

        with gr.Row():
            url_input = gr.Textbox(label="CivitAI Download URL", placeholder="Enter the CivitAI model URL")
            output_path_input = gr.Textbox(label="Output Path", placeholder="Enter the destination folder path")
            token_input = gr.Textbox(label="CivitAI API Token (optional)", placeholder="Enter your CivitAI token (leave blank to use saved token)", type="password")

        download_button = gr.Button("Download")
        output = gr.Textbox(label="Download Status", interactive=False)
        output_file = gr.File(label="Downloaded File", interactive=False)

        download_button.click(civitai_downloader, inputs=[url_input, output_path_input, token_input], outputs=[output, output_file])

    
    demo.launch(debug=True, share=True)

if __name__ == "__main__":
    launch_ui()
