All-in-One App Studio
Create an Instance

What is this template?
This template gives you a complete creative AI studio with eight powerful applications, a GPU-accelerated remote desktop with KDE Plasma and Blender, all in a single container. Generate images, create videos, make music, synthesize voices, transcribe audio, train LoRAs, fine-tune LLMs, and work in a full desktop environment with 3D rendering — all from one instance.

Think: "One GPU instance, eight creative AI tools, a full desktop with Blender — start what you need, stop what you don't."

Important: We recommend setting the environment variable ENABLE_HTTPS=true as described below. You will need to install the Vast.ai certificate to avoid browser warnings.

What's included?
Application	What it does
Desktop	GPU-accelerated KDE Plasma desktop via WebRTC (Selkies)
Blender	3D modeling, rendering, and animation (GPU Cycles)
ComfyUI	Node-based image & video generation
SD Forge	Stable Diffusion WebUI (neo)
Wan2GP	Video generation
ACE Step 1.5	AI music generation
Voicebox	Text-to-speech synthesis
Whisper WebUI	Speech-to-text transcription
Ostris AI Toolkit	LoRA and model training
Unsloth Studio	LLM fine-tuning & serving
No applications auto-start. You choose what to run via the Supervisor tab in Instance Portal. This keeps VRAM free for the tools you actually need.

Who is this for?
This is perfect if you:

Want multiple creative AI tools without managing separate instances
Need a GPU-accelerated remote desktop for Blender, Chrome, or other GUI applications
Want to render 3D scenes on powerful cloud GPUs with Blender's Cycles renderer
Need to switch between image generation, video, music, voice, and training workflows
Are exploring different tools and want everything in one place
Want to use ComfyUI and SD Forge with a shared model library
Need dedicated video generation with Wan2GP alongside image workflows
Want speech-to-text transcription alongside text-to-speech synthesis
Need to train LoRAs with AI Toolkit and immediately test them in ComfyUI or Forge
Want to fine-tune LLMs and serve them immediately via an OpenAI-compatible API
Are building multi-modal creative pipelines
Quick Start Guide
Step 1: Launch Instance
Click "Rent" when you've found a suitable GPU instance. We recommend 24 GB+ VRAM for most use cases (48 GB+ if running multiple apps or training).

Step 2: Wait for Setup
The container will start with Instance Portal and Jupyter ready. Applications are installed but not running yet.

Step 3: Start Your Applications
Open Instance Portal and go to the Supervisor tab. Click Start next to the applications you want to use. Or use the terminal:

# Example: start the desktop and ComfyUI
supervisorctl start desktop comfyui
Step 4: Access Your Applications
Click the application tabs in Instance Portal to open each tool in your browser. Each application has its own tab.

Key Features
GPU-Accelerated Remote Desktop
Start the desktop service to get a full KDE Plasma desktop streamed to your browser via low-latency WebRTC:

supervisorctl start desktop
The desktop includes:

Blender — Full 3D suite with GPU-accelerated Cycles rendering
Google Chrome — Web browser
LibreOffice — Office suite
VLC — Media player
KDE Plasma — Full desktop environment with file manager, settings, etc.
Access via the Desktop tab in Instance Portal. VNC is also available on port 5900 for external VNC clients.

Tip: The desktop starts with the NVIDIA display drivers being installed on first launch. This takes a minute but only happens once.

Nine Applications + Desktop
Application	Start Command	Port
Desktop	supervisorctl start desktop	6100
ComfyUI	supervisorctl start comfyui	8188
SD Forge	supervisorctl start forge	7860
Wan2GP	supervisorctl start wan2gp	7861
ACE Step	supervisorctl start ace-step	13000
Voicebox	supervisorctl start voicebox	7493
Whisper WebUI	supervisorctl start whisper-webui	17862
AI Toolkit	supervisorctl start ai-toolkit	18675
Unsloth Studio	supervisorctl start unsloth-studio	8888
Shared Model Library
ComfyUI and SD Forge share the same model directories. Download a checkpoint in one tool, use it in both:

/workspace/ComfyUI/models/
├── checkpoints/     # Shared with Forge (models/Stable-diffusion)
├── loras/           # Shared with Forge (models/Lora)
├── vae/             # Shared with Forge (models/VAE)
├── controlnet/      # Shared with Forge (models/ControlNet)
├── embeddings/      # Shared with Forge (embeddings)
└── upscale_models/  # Shared with Forge (models/ESRGAN)
Unsloth Studio: Train and Serve
Unsloth Studio isn't just for fine-tuning — it can also serve your models directly. Use the Chat tab in Studio to interact with any loaded model, or connect external tools via the built-in OpenAI-compatible API:

Chat UI: Built into the Studio web interface
API endpoint: POST http://<host>:8888/v1/chat/completions
Model listing: GET http://<host>:8888/v1/models
Fine-tune a model, then immediately chat with it or connect tools like Open WebUI or SillyTavern.

On-Demand Services
No applications auto-start, so your VRAM stays free until you need it:

Instance Portal: Use the Supervisor tab — click Start/Stop next to each service
Terminal: supervisorctl start comfyui / supervisorctl stop comfyui
Multiple at once: supervisorctl start comfyui ace-step voicebox
Auto-Start on Boot
Want specific services to start automatically? Set the SUPERVISOR_AUTOSTART environment variable:

SUPERVISOR_AUTOSTART=comfyui,desktop
Dynamic Provisioning
Need specific models or software installed automatically? Set the PROVISIONING_SCRIPT environment variable to a plain-text script URL (GitHub, Gist, etc.), and we'll run your setup script on first boot!

Environment Variables Reference
Variable	Default	Description
ENABLE_HTTPS	true	Secure HTTPS access (strongly recommended)
WORKSPACE	/workspace	Workspace directory for models and outputs
SUPERVISOR_AUTOSTART	(none)	Comma-separated services to start on boot
COMFYUI_ARGS	--disable-auto-launch --enable-cors-header --port 18188	ComfyUI startup arguments
FORGE_ARGS	--port 17860	SD Forge startup arguments
VOICEBOX_ARGS	--host 127.0.0.1 --port 17493	Voicebox startup arguments
UNSLOTH_STUDIO_ARGS	--host 127.0.0.1 --port 18888	Unsloth Studio startup arguments
WAN2GP_PORT	7861	Wan2GP server port
WHISPER_UI_ARGS	--whisper_type whisper --server_port 7862	Whisper WebUI startup arguments
DISPLAY_SIZEW	1920	Desktop resolution width
DISPLAY_SIZEH	1080	Desktop resolution height
SELKIES_ENCODER	x264enc	Desktop streaming encoder
PROVISIONING_SCRIPT	(none)	URL to a setup script to run on first boot
Recommended GPU Memory
Use Case	Minimum VRAM	Recommended VRAM
Image generation (SD 1.5 / SDXL)	8 GB	12 GB
Image generation (FLUX)	16 GB	24 GB
Video generation (Wan2GP)	12 GB	24 GB
Music generation (ACE Step)	8 GB	16 GB
Voice synthesis (Voicebox)	8 GB	12 GB
Speech transcription (Whisper)	4 GB	8 GB
LoRA training (AI Toolkit)	16 GB	24 GB
LLM fine-tuning (Unsloth)	16 GB	48 GB+
Blender GPU rendering	8 GB	24 GB+
Multiple apps simultaneously	24 GB	48 GB+
Licenses
This template ships vendor application(s) under the following license(s):

ComfyUI — GPL-3.0 (upstream)
SD Forge (Classic) — AGPL-3.0 (upstream)
Voicebox — MIT (upstream)
Ostris AI Toolkit — MIT (upstream)
Wan2GP — WanGP Community License 2.0 (upstream)
Unsloth Studio — AGPL-3.0 (upstream)
Whisper WebUI — Apache-2.0 (upstream)
ACE-Step 1.5 — MIT (upstream)
ACE-Step UI — MIT (per upstream README) (upstream)
PyTorch — BSD-3-Clause (upstream)
Selkies-GStreamer — MPL-2.0 (upstream)
Blender — GPL-2.0-or-later (upstream)
See /LICENSES.md in the image for license details and file locations.

Need More Help?
Blender: Official Website · Documentation
ComfyUI: Official Repository · ComfyUI-Manager
SD Forge: Official Repository
Wan2GP: Official Repository
ACE Step: Official Repository
Voicebox: Official Repository
Whisper WebUI: Official Repository
AI Toolkit: Official Repository
Unsloth: Official Repository
Image Source: GitHub Repository
Instance Portal Guide: Vast.ai Documentation
Template Configuration: Vast.ai Template Guide
Support: Use the messaging icon in the Vast.ai console updated 2026-05-22 16:59