# Tutor Chatbot Website

A web-based chatbot interface that allows students to interact with a fine-tuned Llama language model trained as a high school tutor. Students can ask questions and receive educational guidance across multiple subjects including mathematics, science, literature, and history.

## Features

- 🎓 Interactive chat interface for educational assistance
- 🚀 Fast inference using 4-bit quantization
- 💬 Clean, distraction-free UI focused on learning
- 🔧 Simple REST API for easy integration
- ☁️ Deployable to cloud platforms (Hugging Face Spaces, Google Cloud, etc.)

## Architecture

The application consists of three main components:

1. **Frontend**: Single-page web application (HTML/CSS/JavaScript)
2. **Backend API**: FastAPI server handling model inference
3. **Model Service**: Unsloth-based model loading and inference engine

## Prerequisites

- Python 3.10 or higher
- CUDA-capable GPU (for local development)
- 16GB+ RAM recommended
- The fine-tuned model files in `tutor_model_lora/` directory

## Installation

1. Clone this repository or navigate to the project directory

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure the `tutor_model_lora` directory contains your fine-tuned model files

## Running Locally

Start the FastAPI server:

```bash
python app.py
```

The application will be available at `http://localhost:8000`

## API Endpoints

### `GET /`
Serves the frontend HTML interface

### `POST /chat`
Send a message to the tutor model

**Request:**
```json
{
  "message": "Explain Newton's second law"
}
```

**Response:**
```json
{
  "response": "Newton's second law states that...",
  "status": "success"
}
```

### `GET /health`
Check server and model status

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda:0"
}
```

## Deployment

### Hugging Face Spaces

1. Create a new Space on Hugging Face with GPU support
2. Upload all project files including the `tutor_model_lora` directory
3. Configure Git LFS for large model files (`.gitattributes` is included)
4. Set the SDK to "Docker" or "Gradio"
5. Configure environment variables:
   - `MODEL_PATH`: `tutor_model_lora`
   - `MAX_SEQ_LENGTH`: `2048`
   - `PORT`: `7860`

### Google Cloud / AWS / Azure

1. Create a GPU-enabled VM instance (e.g., T4, V100)
2. Install Python 3.10+ and CUDA drivers
3. Clone the repository and install dependencies
4. Run the application with `python app.py`
5. Configure firewall rules to allow HTTP traffic

## Project Structure

```
tutor-chatbot/
├── app.py                 # FastAPI application entry point
├── model_service.py       # Model loading and inference logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitattributes        # Git LFS configuration
├── static/
│   └── index.html        # Frontend interface
└── tutor_model_lora/     # Fine-tuned model files
    ├── adapter_config.json
    ├── adapter_model.safetensors
    └── ...
```

## Configuration

The application can be configured through environment variables:

- `MODEL_PATH`: Path to the model directory (default: `tutor_model_lora`)
- `MAX_SEQ_LENGTH`: Maximum sequence length for the model (default: `2048`)
- `PORT`: Server port (default: `8000`)
- `HOST`: Server host (default: `0.0.0.0`)

## Development

### Running Tests

```bash
pytest
```

### Code Structure

- `app.py`: FastAPI application with API endpoints
- `model_service.py`: Model service layer handling inference
- `static/index.html`: Frontend single-page application

## Troubleshooting

### Model Loading Issues

If the model fails to load:
- Verify the `tutor_model_lora` directory contains all required files
- Check GPU availability with `torch.cuda.is_available()`
- Ensure sufficient GPU memory (8GB+ recommended)

### Out of Memory Errors

- Reduce `MAX_SEQ_LENGTH` to 1024 or lower
- Ensure 4-bit quantization is enabled
- Close other GPU-intensive applications

### Slow Response Times

- First response may be slower due to model initialization
- Subsequent responses should be faster (5-15 seconds typical)
- Consider using a more powerful GPU for production

## License

This project is for educational purposes.

## Acknowledgments

- Built with [Unsloth](https://github.com/unslothai/unsloth) for efficient model inference
- Powered by [FastAPI](https://fastapi.tiangolo.com/) for the backend
- Uses Meta's Llama model architecture
