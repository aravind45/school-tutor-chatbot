# Deployment Checklist

Use this checklist before deploying to ensure everything is ready.

## Pre-Deployment Checks

### ✅ Files Present

- [ ] `app.py` - FastAPI backend
- [ ] `model_service.py` - Model service layer
- [ ] `requirements.txt` - Python dependencies
- [ ] `Dockerfile` - Docker configuration
- [ ] `static/index.html` - Frontend interface
- [ ] `.gitattributes` - Git LFS configuration
- [ ] `.gitignore` - Git ignore rules
- [ ] `README.md` or `README_HF_SPACES.md` - Documentation

### ✅ Model Files

- [ ] `tutor_model_lora/adapter_config.json`
- [ ] `tutor_model_lora/adapter_model.safetensors`
- [ ] `tutor_model_lora/tokenizer.json`
- [ ] `tutor_model_lora/tokenizer_config.json`
- [ ] `tutor_model_lora/special_tokens_map.json`

### ✅ Configuration

- [ ] Port set to 7860 in `app.py` (for Hugging Face Spaces)
- [ ] CORS configured in `app.py`
- [ ] Environment variables documented
- [ ] Model path is correct (`tutor_model_lora`)

## Deployment Options

Choose one:

### Option 1: Hugging Face Spaces (Recommended - Free GPU)

1. **Create Hugging Face Account**
   - Go to https://huggingface.co/join
   - Verify your email

2. **Create New Space**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Name: `tutor-chatbot` (or your choice)
   - SDK: **Docker**
   - Hardware: **GPU** (T4 or better)
   - Visibility: Public or Private

3. **Prepare Repository**
   ```bash
   # Clone your new Space
   git clone https://huggingface.co/spaces/YOUR_USERNAME/tutor-chatbot
   cd tutor-chatbot
   
   # Copy all files from your project
   # (Make sure you're in your project directory first)
   ```

4. **Set Up Git LFS**
   ```bash
   git lfs install
   git lfs track "*.safetensors"
   git lfs track "*.bin"
   git lfs track "*.pt"
   ```

5. **Rename README for Hugging Face**
   ```bash
   # Use the HF-specific README
   cp README_HF_SPACES.md README.md
   ```

6. **Commit and Push**
   ```bash
   git add .
   git commit -m "Initial deployment of tutor chatbot"
   git push
   ```

7. **Wait for Build**
   - Check the "Logs" tab in your Space
   - Build takes 5-15 minutes
   - First run may take longer (model loading)

8. **Test Your Space**
   - Visit: `https://huggingface.co/spaces/YOUR_USERNAME/tutor-chatbot`
   - Ask a test question
   - Verify response quality

### Option 2: GitHub Repository (For Version Control)

1. **Create GitHub Repository**
   - Go to https://github.com/new
   - Name: `tutor-chatbot`
   - Visibility: Public or Private
   - Don't initialize with README (we have one)

2. **Initialize Git (if not already)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Tutor chatbot web application"
   ```

3. **Set Up Git LFS**
   ```bash
   git lfs install
   git lfs track "*.safetensors"
   git lfs track "*.bin"
   git add .gitattributes
   git commit -m "Configure Git LFS"
   ```

4. **Add Remote and Push**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/tutor-chatbot.git
   git branch -M main
   git push -u origin main
   ```

5. **Push LFS Files**
   ```bash
   git lfs push --all origin main
   ```

### Option 3: Both (Recommended)

1. Push to GitHub first (for version control)
2. Then deploy to Hugging Face Spaces (for hosting)
3. You can link them so updates to GitHub auto-deploy to HF

## Post-Deployment

### ✅ Testing

- [ ] Visit the deployed URL
- [ ] Test with a simple question: "What is 2+2?"
- [ ] Test with a subject question: "Explain photosynthesis"
- [ ] Test with a math problem: "Solve x^2 - 5x + 6 = 0"
- [ ] Verify loading indicator appears
- [ ] Verify error handling (try empty message)
- [ ] Check response time (should be 5-15 seconds)

### ✅ Monitoring

- [ ] Check health endpoint: `/health`
- [ ] Monitor GPU usage (if on HF Spaces, check logs)
- [ ] Watch for errors in logs
- [ ] Test from different devices/browsers

### ✅ Documentation

- [ ] Update README with deployed URL
- [ ] Add usage examples
- [ ] Document any issues encountered
- [ ] Share with test users

## Troubleshooting

### Build Fails on Hugging Face

1. Check "Logs" tab for error messages
2. Verify Dockerfile syntax
3. Ensure all files are committed
4. Check requirements.txt for typos
5. Try "Factory reboot" in Settings

### Model Doesn't Load

1. Verify model files are uploaded (check file sizes)
2. Check Git LFS is working: `git lfs ls-files`
3. Ensure GPU is selected in Space settings
4. Check logs for CUDA errors

### Slow Responses

1. First response is always slower (model loading)
2. Upgrade to better GPU (A10G vs T4)
3. Check if Space is sleeping (cold start)
4. Reduce max_seq_length if needed

### Can't Connect to Server

1. Verify Space is running (not building)
2. Check if Space is public
3. Try health endpoint: `YOUR_URL/health`
4. Check browser console for errors

## Cost Considerations

### Hugging Face Spaces
- **Free Tier**: Community GPU (may have queue)
- **Pro Tier**: $9/month for better GPU access
- **Enterprise**: Custom pricing

### GitHub
- **Free**: Unlimited public repos
- **LFS**: 1GB free, then $5/month per 50GB

### Cloud Providers
- **AWS EC2 g4dn.xlarge**: ~$0.50/hour (~$360/month)
- **GCP**: Similar pricing
- **Azure**: Similar pricing

## Next Steps After Deployment

1. **Gather Feedback**
   - Share with students
   - Collect usage data
   - Note common questions

2. **Monitor Performance**
   - Track response times
   - Monitor error rates
   - Check GPU utilization

3. **Iterate**
   - Fine-tune model with new data
   - Improve prompts
   - Add new features

4. **Scale**
   - Add conversation history
   - Implement user accounts
   - Add more subjects

## Support

If you encounter issues:
1. Check DEPLOYMENT_GUIDE.md for detailed troubleshooting
2. Review Hugging Face Spaces documentation
3. Check GitHub Issues (if public repo)
4. Ask in Hugging Face forums

---

Good luck with your deployment! 🚀
