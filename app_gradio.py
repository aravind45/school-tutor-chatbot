"""
Gradio App for Tutor Chatbot with ZeroGPU Support

This version uses Gradio's chat interface and is compatible with
Hugging Face Spaces ZeroGPU for free GPU access.
"""

import os
import logging
import gradio as gr
from model_service import ModelService
import spaces

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global model service instance
model_service = None

def initialize_model():
    """Initialize the model service"""
    global model_service
    
    if model_service is None:
        try:
            logger.info("Initializing model service...")
            model_path = os.getenv("MODEL_PATH", "tutor_model_lora")
            max_seq_length = int(os.getenv("MAX_SEQ_LENGTH", "2048"))
            
            model_service = ModelService(
                model_path=model_path,
                max_seq_length=max_seq_length
            )
            logger.info("✅ Model service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize model: {str(e)}")
            raise
    
    return model_service

@spaces.GPU
def chat_response(message, history):
    """
    Generate a response for the chat interface.
    
    Args:
        message: User's message
        history: Chat history (list of [user_msg, bot_msg] pairs)
        
    Returns:
        Response string
    """
    try:
        # Initialize model if needed
        service = initialize_model()
        
        # Validate input
        if not message or not message.strip():
            return "Please enter a message."
        
        if len(message) > 2000:
            return "Message is too long. Please keep it under 2000 characters."
        
        # Generate response
        logger.info(f"Processing message: {message[:50]}...")
        response = service.get_response(
            user_message=message.strip(),
            max_tokens=500
        )
        
        logger.info(f"Generated response: {response[:50]}...")
        return response
        
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"

# Create Gradio interface
def create_interface():
    """Create the Gradio chat interface"""
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .message-wrap {
        max-width: 800px;
    }
    """
    
    # Create the chat interface
    demo = gr.ChatInterface(
        fn=chat_response,
        title="🎓 High School Tutor - AI Learning Assistant",
        description="""
        Welcome to your AI tutor! I can help you with:
        
        - **Mathematics**: Algebra, Geometry, Trigonometry, Calculus
        - **Science**: Physics, Chemistry, Biology
        - **Literature**: Analysis, themes, writing techniques
        - **History**: Events, causes, historical context
        
        Ask me anything, and I'll do my best to explain it clearly!
        """,
        examples=[
            "Explain Newton's second law with an example",
            "How do I solve quadratic equations?",
            "What causes seasons on Earth?",
            "Analyze the theme of To Kill a Mockingbird",
            "Why did World War I start?",
            "Help me understand photosynthesis",
            "Solve: 2x + 5 = 13"
        ],
        theme=gr.themes.Soft(
            primary_hue="purple",
            secondary_hue="blue",
        ),
        css=custom_css,
        retry_btn="🔄 Retry",
        undo_btn="↩️ Undo",
        clear_btn="🗑️ Clear",
        submit_btn="Send",
        chatbot=gr.Chatbot(
            height=500,
            show_label=False,
            avatar_images=(None, "🎓"),
        ),
    )
    
    return demo

# Main entry point
if __name__ == "__main__":
    # Initialize model on startup
    try:
        initialize_model()
    except Exception as e:
        logger.error(f"Failed to initialize on startup: {str(e)}")
    
    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
