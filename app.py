import gradio as gr
import os

logs = []

def downloader(url, output_path, civitai_token):
  logs.clear()
  prompt = f"civitai-downloader --url={url} --output_path={output_path} --token={civitai_token}"
  os.system(prompt)
  logs.append(f"Downloaded! Check the output path: {output_path}")
  yield "\n".join(logs)

with gr.Blocks(title = "CivitAI Downloader") as app:
  gr.Markdown("<h1> ⬇️ CivitAI Downloader ⬇️ </h1>")
  with gr.Row():
    link = gr.Textbox(
        label = "URL",
        placeholder = "Paste the URL here",
        interactive = True,
    )
    out_path = gr.Textbox(
        label = "Output Path",
        placeholder = "Place the output path here",
        interactive = True,
    )
  with gr.Row():
    token = gr.Textbox(
        label = "CivitAI API Key",
        placeholder = "Paste the API Key here. Only needed the first time per session",
        interactive = True,
    )
  with gr.Row():
    button = gr.Button("Download!", variant = "primary")
  with gr.Row():
    outputs = gr.Textbox(
        label = "Output information",
        interactive = False,
    )

  button.click(downloader, [link, out_path, token], [outputs])

app.launch(share=True)