# Design Document: Tutor Chatbot Website

## Overview

This document describes the design for a web-based chatbot application that provides students with access to a fine-tuned Llama language model trained as a high school tutor. The system consists of three main components:

1. **Frontend**: A single-page web application built with HTML, CSS, and JavaScript
2. **Backend API**: A Python FastAPI server that handles model inference
3. **Model Service**: Unsloth-based model loading and inference engine

The application will be deployable to cloud platforms like Hugging Face Spaces, which provides free GPU access for hosting machine learning applications.

## Architecture

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           Frontend (HTML/CSS/JavaScript)              │  │
│  │  - Chat Interface                                     │  │
│  │  - Message Display                                    │  │
│  │  - Input Handling                                     │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/JSON
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend Server (FastAPI)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  API Endpoints                        │  │
│  │  - POST /chat                                         │  │
│  │  - GET /health                                        │  │
│  │  - GET / (serves frontend)                           │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Model Service Layer                      │  │
│  │  - Model Loading (Unsloth)                           │  │
│  │  - Prompt Formatting                                  │  │
│  │  - Inference Execution                                │  │
│  │  - Response Processing                                │  │
│  └───────────────────────────────────────────────────────┘  │
│                            │                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Tutor Model (tutor_model_lora)               │  │
│  │  - Llama 3 8B with LoRA adapters                     │  │
│  │  - Loaded in 4-bit quantization                      │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- HTML5 for structure
- CSS3 for styling (no framework needed for simplicity)
- Vanilla JavaScript for interactivity
- Fetch API for HTTP requests

**Backend:**
- Python 3.10+
- FastAPI for the web framework
- Uvicorn as the ASGI server
- Unsloth for model loading and inference
- PyTorch for tensor operations

**Deployment:**
- Hugging Face Spaces (Gradio SDK or Docker)
- Alternative: Google Colab with ngrok tunnel
- Alternative: Cloud providers (AWS, GCP, Azure) with GPU instances

## Components and Interfaces

### 1. Frontend Component

**Responsibilities:**
- Render the chat interface
- Handle user input
- Send messages to the backend
- Display responses
- Manage UI state (loading indicators, error messages)

**Key Elements:**
- Message container (scrollable div)
- Input field (textarea with auto-resize)
- Send button
- Loading indicator
- Welcome message

**Interface with Backend:**
```javascript
// POST /chat
Request: {
  "message": "Explain Newton's second law"
}

Response: {
  "response": "Newton's second law states that...",
  "status": "success"
}

Error Response: {
  "error": "Model inference failed",
  "status": "error"
}
```

### 2. Backend API Component

**Endpoints:**

1. **GET /**
   - Serves the frontend HTML page
   - Returns: HTML content

2. **POST /chat**
   - Accepts user messages
   - Processes through model
   - Returns generated response
   - Request body: `{"message": string}`
   - Response body: `{"response": string, "status": string}`

3. **GET /health**
   - Health check endpoint
   - Returns model status and GPU availability
   - Response: `{"status": "healthy", "model_loaded": boolean, "device": string}`

**Request/Response Flow:**
1. Receive POST request with user message
2. Validate input (non-empty, reasonable length)
3. Format message using instruction template
4. Call model service for inference
5. Extract and clean response
6. Return JSON response

### 3. Model Service Component

**Responsibilities:**
- Load the fine-tuned model on startup
- Format prompts according to training template
- Execute inference with appropriate parameters
- Process and clean model outputs

**Key Functions:**

```python
class ModelService:
    def __init__(self, model_path: str, max_seq_length: int = 2048):
        """Initialize and load the model"""
        
    def format_prompt(self, user_message: str) -> str:
        """Format user message into instruction template"""
        
    def generate_response(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate response from model"""
        
    def cleanup_response(self, raw_output: str) -> str:
        """Extract and clean the response portion"""
```

**Model Loading:**
- Use Unsloth's `FastLanguageModel.from_pretrained()`
- Load from `tutor_model_lora` directory
- Enable 4-bit quantization for memory efficiency
- Set model to inference mode with `FastLanguageModel.for_inference()`

**Prompt Template:**
```
### Instruction:
{user_message}

### Response:

```

**Generation Parameters:**
- `max_new_tokens`: 500
- `temperature`: 0.7
- `do_sample`: True
- `pad_token_id`: tokenizer.pad_token_id

## Data Models

### Message Object (Frontend)
```javascript
{
  id: string,           // Unique identifier
  role: "user" | "assistant",
  content: string,      // Message text
  timestamp: Date
}
```

### Chat Request (API)
```python
class ChatRequest(BaseModel):
    message: str
    
    @validator('message')
    def validate_message(cls, v):
        if not v or not v.strip():
            raise ValueError('Message cannot be empty')
        if len(v) > 2000:
            raise ValueError('Message too long (max 2000 characters)')
        return v.strip()
```

### Chat Response (API)
```python
class ChatResponse(BaseModel):
    response: str
    status: str = "success"
```

### Error Response (API)
```python
class ErrorResponse(BaseModel):
    error: str
    status: str = "error"
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Non-empty input validation
*For any* user message submitted through the Web Interface, if the message is empty or contains only whitespace, the system should reject the submission and the message history should remain unchanged.
**Validates: Requirements 2.5**

### Property 2: Response generation completeness
*For any* valid user message, when processed by the Backend Server, the system should return a response that contains the generated text and a success status.
**Validates: Requirements 2.1, 2.3**

### Property 3: Prompt formatting consistency
*For any* user message, the formatted prompt should follow the instruction-response template format with the exact structure used during model training.
**Validates: Requirements 2.2**

### Property 4: Message ordering preservation
*For any* sequence of messages in a Chat Session, the messages should appear in the Web Interface in the same chronological order they were sent.
**Validates: Requirements 3.1**

### Property 5: Model initialization idempotence
*For any* Backend Server startup, loading the Tutor Model should result in the same inference-ready state regardless of previous server runs.
**Validates: Requirements 5.1, 5.2**

### Property 6: API error handling
*For any* error condition during inference, the Backend Server should return a valid JSON error response with an appropriate HTTP status code within the timeout period.
**Validates: Requirements 4.4, 6.4**

### Property 7: Health check availability
*For any* time when the Backend Server is running, the health check endpoint should return a valid status response indicating model readiness.
**Validates: Requirements 6.3**

## Error Handling

### Frontend Error Handling

**Network Errors:**
- Display user-friendly message: "Unable to connect to server. Please check your connection."
- Retry button for failed requests
- Timeout after 30 seconds

**Invalid Input:**
- Prevent submission of empty messages
- Show character count for long messages
- Disable send button during processing

**Server Errors:**
- Display error message from server response
- Log errors to console for debugging
- Allow user to retry

### Backend Error Handling

**Model Loading Errors:**
- Log detailed error information
- Return 503 Service Unavailable
- Provide clear error message about model availability

**Inference Errors:**
- Catch PyTorch/CUDA errors
- Return 500 Internal Server Error
- Log stack trace for debugging
- Return generic error message to user

**Validation Errors:**
- Return 400 Bad Request
- Include specific validation error message
- Log validation failures

**Resource Errors:**
- Handle out-of-memory errors
- Implement request queuing if needed
- Return 503 if resources unavailable

### Error Response Format

All errors follow consistent JSON structure:
```json
{
  "error": "Human-readable error message",
  "status": "error",
  "code": "ERROR_CODE"
}
```

## Testing Strategy

### Unit Testing

**Backend Unit Tests:**
- Test prompt formatting with various inputs
- Test input validation (empty, too long, special characters)
- Test response cleaning and extraction
- Test API endpoint request/response handling
- Mock model inference for fast testing

**Frontend Unit Tests:**
- Test message rendering
- Test input validation
- Test API call formatting
- Test error display logic

### Property-Based Testing

We will use **Hypothesis** (Python property-based testing library) for backend testing.

**Configuration:**
- Minimum 100 iterations per property test
- Each test tagged with format: `**Feature: tutor-chatbot-website, Property {number}: {property_text}**`

**Property Tests to Implement:**

1. **Property 1: Non-empty input validation**
   - Generate random strings (including whitespace-only)
   - Verify empty/whitespace strings are rejected
   - Verify valid strings are accepted

2. **Property 2: Response generation completeness**
   - Generate random valid messages
   - Mock model to return test responses
   - Verify response structure is always complete

3. **Property 3: Prompt formatting consistency**
   - Generate random user messages
   - Verify formatted prompts match template structure
   - Verify instruction section contains user message

4. **Property 4: Message ordering preservation**
   - Generate random sequences of messages
   - Verify frontend maintains chronological order
   - Test with varying message counts

5. **Property 6: API error handling**
   - Generate error conditions (model failures, timeouts)
   - Verify error responses have correct structure
   - Verify appropriate HTTP status codes

6. **Property 7: Health check availability**
   - Call health endpoint multiple times
   - Verify consistent response structure
   - Verify status information is present

### Integration Testing

**End-to-End Tests:**
- Test complete flow: user input → backend → model → response → display
- Test with actual model (slower, fewer iterations)
- Verify response quality for sample questions

**Deployment Tests:**
- Test model loading on target platform
- Verify GPU availability
- Test cold start performance
- Verify frontend assets load correctly

### Manual Testing

**User Experience Testing:**
- Test on different browsers (Chrome, Firefox, Safari)
- Test on different screen sizes
- Verify visual design and readability
- Test conversation flow feels natural

**Model Quality Testing:**
- Test with various subject questions (math, science, literature)
- Verify responses are helpful and accurate
- Test edge cases (very short questions, complex questions)

## Deployment Architecture

### Hugging Face Spaces Deployment

**Structure:**
```
tutor-chatbot/
├── app.py                 # FastAPI application
├── requirements.txt       # Python dependencies
├── README.md             # Space description
├── static/
│   └── index.html        # Frontend
├── tutor_model_lora/     # Model files (uploaded)
│   ├── adapter_config.json
│   ├── adapter_model.safetensors
│   └── ...
└── .gitattributes        # Git LFS configuration
```

**Requirements.txt:**
```
fastapi
uvicorn[standard]
unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git
torch
transformers
peft
```

**Hugging Face Space Configuration:**
- SDK: Docker or Gradio
- Hardware: GPU (T4 or better)
- Python version: 3.10
- Persistent storage: Enabled (for model files)

**Environment Variables:**
- `MODEL_PATH`: Path to model directory
- `MAX_SEQ_LENGTH`: Maximum sequence length (2048)
- `PORT`: Server port (7860 for HF Spaces)

### Alternative: Google Colab Deployment

**Approach:**
- Run FastAPI server in Colab notebook
- Use ngrok to create public URL
- Upload model files to Google Drive
- Mount Drive and load model

**Limitations:**
- Temporary URLs (reset on disconnect)
- Session timeouts after inactivity
- Not suitable for production

### Alternative: Cloud Provider Deployment

**Options:**
- AWS EC2 with GPU (g4dn.xlarge or similar)
- Google Cloud Compute Engine with GPU
- Azure VM with GPU

**Considerations:**
- Higher cost than Hugging Face Spaces
- More control over infrastructure
- Requires more DevOps knowledge
- Better for production workloads

## Performance Considerations

### Model Loading
- Load model once on startup (not per request)
- Use 4-bit quantization to reduce memory
- Expect 5-10 second startup time

### Inference Performance
- First token latency: ~1-2 seconds
- Generation speed: ~10-20 tokens/second on T4 GPU
- Total response time: 5-15 seconds for typical responses

### Optimization Strategies
- Implement request queuing for concurrent requests
- Set reasonable max_new_tokens limit (500)
- Use caching for common questions (future enhancement)
- Consider batch processing if multiple users

### Resource Management
- Monitor GPU memory usage
- Implement automatic cleanup if memory issues
- Log performance metrics
- Set request timeouts (30 seconds)

## Security Considerations

### Input Validation
- Sanitize user input to prevent injection attacks
- Limit message length to prevent resource exhaustion
- Rate limiting to prevent abuse (future enhancement)

### API Security
- CORS configuration for frontend access
- No authentication required for MVP (add later if needed)
- Input validation on all endpoints

### Model Safety
- Model trained on educational content
- No explicit content filtering in MVP
- Monitor for inappropriate usage patterns

### Deployment Security
- Use HTTPS in production
- Keep dependencies updated
- Follow platform security best practices
- Don't expose internal error details to users

## Future Enhancements

### Conversation History Persistence
- Store conversations in database
- Allow users to resume previous sessions
- Export conversation history

### Streaming Responses
- Implement Server-Sent Events (SSE)
- Stream tokens as they're generated
- Improve perceived responsiveness

### Multi-turn Context
- Maintain conversation context across messages
- Allow follow-up questions
- Implement context window management

### User Accounts
- Authentication and authorization
- Personal conversation history
- Usage tracking and limits

### Enhanced UI
- Markdown rendering for formatted responses
- Code syntax highlighting
- LaTeX math rendering
- Dark mode

### Analytics
- Track usage patterns
- Monitor response quality
- Identify common questions
- Performance metrics dashboard
