# AI PDF Assistant - Enhanced Chatbot (Mistral AI)

A powerful AI-powered chatbot that can analyze PDF documents, provide summaries, and answer questions intelligently using Mistral AI's free models and LangChain.

## Features

### 🚀 **Enhanced Frontend**
- Modern, responsive UI with beautiful gradients and animations
- Drag & drop PDF upload with visual feedback
- Real-time chat interface with typing indicators
- Suggestion buttons for common questions
- Mobile-responsive design

### 🤖 **AI-Powered Backend (Mistral AI)**
- Intelligent PDF text extraction and processing
- Advanced text chunking for better AI understanding
- Vector embeddings using HuggingFace (free alternative)
- Mistral AI powered Q&A system (free tier available)
- Automatic document summarization
- Context-aware responses based on PDF content

### 📊 **Smart Analysis**
- Automatic document summarization upon upload
- Key topics and themes identification
- Important findings extraction
- Statistical data recognition
- Purpose and scope analysis

## Setup Instructions

### 1. **Install Dependencies**
```bash
cd project-root/chatbot
pip install -r requirements.txt
```

### 2. **Get Free Mistral AI API Key**
1. Visit [Mistral AI Console](https://console.mistral.ai/)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key

### 3. **Configure Mistral AI API Key**
Create a `.env` file in the `chatbot` directory:
```bash
# Create .env file
echo "MISTRAL_API_KEY=your_mistral_api_key_here" > .env
```

**Get your free API key from:** [Mistral AI Console](https://console.mistral.ai/)

### 4. **Start the Backend**
```bash
cd backend
python app.py
```

The backend will start on `http://127.0.0.1:5000`

### 5. **Open the Frontend**
Open `frontend/index.html` in your web browser or serve it using a local server.

## Testing Guide

### **Basic Functionality Test**
1. **Start the backend** - Run `python app.py` in the backend directory
2. **Open the frontend** - Open `frontend/index.html` in your browser
3. **Upload a PDF** - Drag & drop or click to select a PDF file
4. **Verify upload** - Check that the file is processed and summary appears
5. **Test chat** - Ask questions about the uploaded PDF

### **Test Scenarios**

#### **PDF Upload Test**
- ✅ Upload a valid PDF file
- ✅ Verify text extraction works
- ✅ Check that AI summary is generated
- ✅ Confirm vector store is created

#### **Chat Functionality Test**
- ✅ Ask general questions about the document
- ✅ Test specific content queries
- ✅ Verify context-aware responses
- ✅ Check error handling for invalid questions

#### **Edge Cases Test**
- ✅ Try uploading non-PDF files (should be rejected)
- ✅ Test with corrupted PDFs
- ✅ Verify behavior when no PDF is uploaded
- ✅ Check network error handling

### **Sample Test Questions**
After uploading a PDF, try these questions:
- "What is this document about?"
- "Summarize the main points"
- "What are the key findings?"
- "What methodology was used?"
- "What are the conclusions?"

## API Endpoints

### **POST /upload**
Upload and process a PDF file
- **Input**: PDF file in form data
- **Output**: Processing status and summary

### **POST /chat**
Ask questions about the uploaded PDF
- **Input**: JSON with `message` field
- **Output**: AI-generated answer

### **GET /summary**
Get document summary
- **Output**: Current document summary

### **GET /status**
Get current system status
- **Output**: PDF status and processing info

### **GET /health**
Health check endpoint
- **Output**: Backend status

## Architecture

### **Frontend (HTML/CSS/JavaScript)**
- Modern ES6+ JavaScript with classes
- Responsive CSS Grid layout
- Font Awesome icons
- Drag & drop file handling
- Real-time chat interface

### **Backend (Python/Flask)**
- Flask web framework with CORS support
- PyPDF2 for PDF text extraction
- LangChain for AI processing
- Mistral AI for intelligent responses
- HuggingFace embeddings for vector search
- FAISS vector store for semantic search

### **AI Processing Pipeline**
1. **PDF Upload** → Text extraction
2. **Text Processing** → Chunking and cleaning
3. **Vector Creation** → HuggingFace embeddings
4. **AI Analysis** → Mistral AI processing
5. **Response Generation** → Context-aware answers

## Why Mistral AI?

### **Free Tier Benefits**
- **No Credit Card Required**: Sign up with just an email
- **Generous Limits**: Free tier includes substantial API usage
- **High Quality**: Professional-grade AI models
- **Fast Response**: Optimized for real-time interactions

### **Model Capabilities**
- **Mistral Small**: Fast, efficient model for quick responses
- **Context Understanding**: Excellent at understanding document context
- **Multilingual Support**: Works with documents in multiple languages
- **Cost Effective**: Much cheaper than OpenAI for production use

## Troubleshooting

### **Common Issues**

#### **"MISTRAL_API_KEY not found"**
- Ensure `.env` file exists in the chatbot directory
- Verify API key is correctly set
- Restart the backend after creating `.env`

#### **PDF Upload Fails**
- Check file format (PDF only)
- Verify file isn't corrupted
- Check backend logs for errors

#### **AI Responses Not Working**
- Verify Mistral AI API key is valid
- Check API quota and billing
- Ensure internet connection is stable

#### **Frontend Can't Connect**
- Verify backend is running on port 5000
- Check CORS settings
- Ensure firewall isn't blocking connections

### **Performance Tips**
- Use smaller PDFs for faster processing
- Close other applications to free up memory
- Ensure stable internet connection for AI features

## Development

### **Adding New Features**
- Frontend: Modify `frontend/index.html`
- Backend: Extend `backend/app.py`
- Dependencies: Update `requirements.txt`

### **Customizing AI Behavior**
- Modify prompts in `AIAssistant` class
- Adjust chunk size and overlap in `PDFProcessor`
- Change Mistral AI model parameters

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review backend console logs
3. Verify Mistral AI API key configuration
4. Test with a simple PDF first
5. Visit [Mistral AI Documentation](https://docs.mistral.ai/) for API details 