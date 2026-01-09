# DreamLens (Gradio)

DreamLens is a small Gradio app that turns a dream description into:
1) an English image-generation prompt,
2) a Chinese dream interpretation,
3) Chinese “personal guidance” text,
and then generates an image via Volcengine VisualService.

This project uses:
- **Gradio** UI for a simple 4-step workflow :contentReference[oaicite:1]{index=1}
- **Ark** (chat completions) to generate the prompt / analysis / guidance :contentReference[oaicite:2]{index=2}
- **Volcengine VisualService** to generate an image and download it locally :contentReference[oaicite:3]{index=3}

---

## Features

- **Generate Image Prompt** (English prompt generator) :contentReference[oaicite:4]{index=4}  
- **Generate Dream Analysis** (Chinese interpretation) :contentReference[oaicite:5]{index=5}  
- **Generate Personal Guidance** (Chinese guidance text) :contentReference[oaicite:6]{index=6}  
- **Generate Image** via VisualService and save as `generated_image.jpg` :contentReference[oaicite:7]{index=7}  

---

## Security Notice (IMPORTANT)

The original script contains hard-coded API keys (Ark + Volcengine AK/SK).  
**Do NOT commit real keys to GitHub.** Move them into environment variables before uploading. :contentReference[oaicite:8]{index=8}

---

## Setup

### 1) Install dependencies

```bash
pip install gradio requests volcengine-sdk volcenginesdkarkruntime
