# Deployment Guide

This guide covers deploying the Tutor Chatbot to various platforms.

## Table of Contents

1. [Hugging Face Spaces (Recommended)](#hugging-face-spaces)
2. [Google Colab with ngrok](#google-colab)
3. [Cloud Providers (AWS/GCP/Azure)](#cloud-providers)
4. [Troubleshooting](#troubleshooting)

---

## Hugging Face Spaces

Hugging Face Spaces provides free GPU hosting, making it the recommended deployment option.

### Prerequisites

- Hugging Face account (free)
- Git installed locally
- Git LFS installed (`git lfs install`)

### Step-by-Step Deployment

#### 1. Create a New Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Configure your Space:
   - **Name**: `tutor-chatbot` (or your preferred name)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: GPU (T4 or better) - Required!
   - **Visibility**: Public or Private

#### 2. Prepare Your Repository

```bash
# Clone your new Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/tutor-chatbot
cd tutor-chatbot

# Copy all project files
cp -r /path/to/your/project/* .

# Important: Ensure these files are present:
# - Dockerfile
# - app.py
# - model_service.py
# - requirements.txt
# - static/index.html
# - tutor_model_lora/ (entire directory)
# - README_HF_SPACES.md (rename to README.md)
```

#### 3. Configure Git LFS for Large Files

The `.gitattributes` file is already configured, but verify it includes:

```
*.safetensors filter=lfs diff=lfs merge=lfs -text
*.bin filter=lfs diff=lfs merge=lfs -text
*.pt filter=lfs diff=lfs merge=lfs -text
*.pth filter=lfs diff=lfs merge=lfs -text
```

#### 4. Push to Hugging Face

```bash
# Initialize Git LFS
git lfs install

# Add all files
git add .

# Commit
git commit -m "Initial deployment of tutor chatbot"

# Push to Hugging Face
git push
```

**Note**: Uploading large model files may take 10-30 minutes depending on your connection.

#### 5. Configure Space Settings

In your Space settings on Hugging Face:

1. **Hardware**: Select "GPU" (T4 recommended, A10G for better performance)
2. **Environment Variables** (optional):
   - `MODEL_PATH`: `tutor_model_lora` (default)
   - `MAX_SEQ_LENGTH`: `2048` (default)
   - `PORT`: `7860` (default)

#### 6. Wait for Build

- The Space will automatically build using your Dockerfile
- Build time: 5-15 minutes
- Check the "Logs" tab for build progress

#### 7. Test Your Deployment

Once the build completes:
1. Your Space will be available at: `https://huggingface.co/spaces/YOUR_USERNAME/tutor-chatbot`
2. Test by asking a question in the chat interface
3. First response may take 10-20 seconds (model loading)

### Hugging Face Spaces Features

**Automatic Sleep/Wake**:
- Spaces automatically sleep after 48 hours of inactivity
- Wake up automatically when someone visits
- Cold start takes ~30 seconds

**Persistent Storage**:
- Model files persist between restarts
- No need to reload model files

**Free GPU Access**:
- Limited to community GPU tier
- May have queue times during peak usage

---

## Google Colab

For temporary testing or development.

### Setup

1. Create a new Colab notebook
2. Select GPU runtime: Runtime → Change runtime type → GPU

### Installation

```python
# Install dependencies
!pip install fastapi uvicorn[standard] pydantic
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install torch transformers peft

# Upload your project files
from google.colab import files
# Upload: app.py, model_service.py, and static/index.html

# Upload model files to Google Drive (recommended)
from google.colab import drive
drive.mount('/content/drive')
```

### Run Server with ngrok

```python
# Install ngrok
!pip install pyngrok

# Set up ngrok (get free token from ngrok.com)
from pyngrok import ngrok
ngrok.set_auth_token("YOUR_NGROK_TOKEN")

# Start FastAPI server in background
import subprocess
import time

# Start server
proc = subprocess.Popen(["python", "app.py"])
time.sleep(5)

# Create public URL
public_url = ngrok.connect(7860)
print(f"Public URL: {public_url}")
```

### Limitations

- Session expires after inactivity
- URL changes on each restart
- Not suitable for production
- Good for testing and development

---

## Cloud Providers

For production deployments with full control.

### AWS EC2

#### Instance Requirements

- **Instance Type**: g4dn.xlarge or better
- **GPU**: NVIDIA T4 (16GB VRAM minimum)
- **Storage**: 50GB+ SSD
- **OS**: Ubuntu 20.04 LTS

#### Setup Steps

```bash
# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install NVIDIA drivers
sudo apt install nvidia-driver-525 -y
sudo reboot

# 3. Install CUDA toolkit
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-ubuntu2004.pin
sudo mv cuda-ubuntu2004.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
sudo add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/ /"
sudo apt update
sudo apt install cuda -y

# 4. Install Python and dependencies
sudo apt install python3.10 python3-pip -y
pip3 install -r requirements.txt

# 5. Upload project files
# Use scp or git clone

# 6. Run with systemd (production)
sudo nano /etc/systemd/system/tutor-chatbot.service
```

**systemd service file**:
```ini
[Unit]
Description=Tutor Chatbot Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/tutor-chatbot
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl enable tutor-chatbot
sudo systemctl start tutor-chatbot
sudo systemctl status tutor-chatbot
```

#### Configure Nginx (Optional)

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/tutor-chatbot
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:7860;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/tutor-chatbot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Google Cloud Platform

Similar to AWS, use:
- **Instance Type**: n1-standard-4 with NVIDIA T4 GPU
- Follow similar setup steps as AWS

### Azure

- **Instance Type**: NC4as_T4_v3 or similar
- Follow similar setup steps as AWS

---

## Troubleshooting

### Model Loading Issues

**Problem**: Model fails to load

**Solutions**:
```bash
# Check if model files exist
ls -lh tutor_model_lora/

# Verify GPU availability
python -c "import torch; print(torch.cuda.is_available())"

# Check CUDA version
nvidia-smi
```

### Out of Memory Errors

**Problem**: CUDA out of memory

**Solutions**:
1. Reduce `MAX_SEQ_LENGTH` to 1024
2. Ensure 4-bit quantization is enabled
3. Close other GPU processes
4. Use a GPU with more VRAM (16GB+)

### Slow Response Times

**Problem**: Responses take too long

**Solutions**:
1. First response is always slower (model initialization)
2. Upgrade to better GPU (T4 → A10G)
3. Check server load: `nvidia-smi`
4. Reduce `max_new_tokens` in model_service.py

### Port Already in Use

**Problem**: Port 7860 is already in use

**Solutions**:
```bash
# Find process using port
lsof -i :7860

# Kill process
kill -9 <PID>

# Or use different port
export PORT=8000
python app.py
```

### Git LFS Issues

**Problem**: Large files not uploading

**Solutions**:
```bash
# Reinstall Git LFS
git lfs install --force

# Track large files
git lfs track "*.safetensors"
git lfs track "*.bin"

# Verify tracking
git lfs ls-files

# Push with LFS
git lfs push --all origin main
```

### Hugging Face Space Build Fails

**Problem**: Docker build fails

**Solutions**:
1. Check Dockerfile syntax
2. Verify all files are committed
3. Check build logs in Space settings
4. Ensure requirements.txt is valid
5. Try rebuilding: Settings → Factory reboot

### Connection Timeout

**Problem**: Frontend can't connect to backend

**Solutions**:
1. Check if server is running: `curl http://localhost:7860/health`
2. Verify CORS settings in app.py
3. Check firewall rules
4. Ensure correct port in frontend code

---

## Performance Optimization

### For Production

1. **Enable caching** for common questions
2. **Implement request queuing** for concurrent users
3. **Use load balancer** for multiple instances
4. **Monitor GPU usage** with prometheus/grafana
5. **Set up logging** with ELK stack

### Cost Optimization

1. **Use Hugging Face Spaces** for free hosting
2. **Implement auto-scaling** on cloud providers
3. **Use spot instances** for development
4. **Enable auto-sleep** when idle

---

## Monitoring

### Health Check

```bash
# Check if service is healthy
curl http://your-domain.com/health

# Expected response:
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda:0",
  "gpu_name": "Tesla T4",
  "gpu_memory_gb": 15.0
}
```

### Logs

```bash
# View application logs
tail -f /var/log/tutor-chatbot.log

# View systemd logs
sudo journalctl -u tutor-chatbot -f

# View Hugging Face Space logs
# Check "Logs" tab in Space settings
```

---

## Security Considerations

1. **Rate Limiting**: Implement rate limiting to prevent abuse
2. **Input Validation**: Already implemented in backend
3. **HTTPS**: Use SSL certificates in production
4. **Authentication**: Add if needed for private deployment
5. **Content Filtering**: Monitor for inappropriate usage

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review application logs
3. Check Hugging Face Spaces documentation
4. Open an issue on GitHub

---

## Next Steps

After successful deployment:
1. Test with various questions
2. Monitor performance and errors
3. Gather user feedback
4. Iterate and improve the model
5. Add new features (conversation history, etc.)

Good luck with your deployment! 🚀
