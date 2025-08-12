import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import PyPDF2
import re
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import MistralAI
from langchain.chat_models import ChatMistralAI
import tiktoken

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables to store PDF data
pdf_text = ""
pdf_chunks = []
vector_store = None
current_filename = ""

# Initialize Mistral AI
mistral_api_key = os.getenv('MISTRAL_API_KEY')
mistral_client = MistralClient(api_key=mistral_api_key) if mistral_api_key else None

class PDFProcessor:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
    
    def extract_text_from_pdf(self, filepath):
        """Extract text from PDF file"""
        try:
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text() or ""
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
                return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def split_text_into_chunks(self, text):
        """Split text into manageable chunks for processing"""
        if not text.strip():
            return []
        
        # Clean the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split into chunks
        chunks = self.text_splitter.split_text(text)
        return chunks
    
    def create_vector_store(self, chunks):
        """Create vector store from text chunks"""
        try:
            if not chunks:
                return None
            
            # Use HuggingFace embeddings (free alternative to OpenAI)
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'}
            )
            vector_store = FAISS.from_texts(chunks, embeddings)
            return vector_store
        except Exception as e:
            print(f"Error creating vector store: {e}")
            return None

class AIAssistant:
    def __init__(self):
        if mistral_client:
            self.llm = ChatMistralAI(
                model="mistral-small-latest",
                temperature=0.7,
                max_tokens=1000
            )
        else:
            self.llm = None
    
    def generate_summary(self, text):
        """Generate a comprehensive summary of the PDF"""
        try:
            if not text.strip():
                return "No text content found in the PDF."
            
            if not mistral_client:
                return "Mistral AI API key not configured. Please set MISTRAL_API_KEY in your .env file."
            
            # Truncate text if too long
            max_tokens = 3000
            encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Using this as reference
            tokens = encoding.encode(text)
            if len(tokens) > max_tokens:
                text = encoding.decode(tokens[:max_tokens])
            
            prompt = f"""
            Please provide a comprehensive summary of the following document. 
            Include:
            1. Main topics and themes
            2. Key findings and conclusions
            3. Important data or statistics mentioned
            4. Overall purpose and scope of the document
            
            Document content:
            {text}
            
            Summary:
            """
            
            messages = [
                ChatMessage(role="user", content=prompt)
            ]
            
            response = mistral_client.chat(
                model="mistral-small-latest",
                messages=messages,
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Unable to generate summary at this time."
    
    def answer_question(self, question, vector_store):
        """Answer questions using the vector store and AI"""
        try:
            if not vector_store:
                return "No PDF has been uploaded yet. Please upload a PDF first."
            
            if not mistral_client:
                return "Mistral AI API key not configured. Please set MISTRAL_API_KEY in your .env file."
            
            # Create a retrieval QA chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=vector_store.as_retriever(search_kwargs={"k": 3})
            )
            
            # Get the answer
            result = qa_chain.run(question)
            return result.strip()
            
        except Exception as e:
            print(f"Error answering question: {e}")
            return "I'm sorry, I encountered an error while processing your question. Please try again."

# Initialize processors
pdf_processor = PDFProcessor()
ai_assistant = AIAssistant()

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global pdf_text, pdf_chunks, vector_store, current_filename
    
    try:
        if 'pdf' not in request.files:
            return jsonify({'error': 'No PDF file provided'}), 400
        
        file = request.files['pdf']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Only PDF files are allowed'}), 400
        
        # Save file
        filename = file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract text
        pdf_text = pdf_processor.extract_text_from_pdf(filepath)
        if not pdf_text.strip():
            return jsonify({'error': 'Could not extract text from PDF. The file might be corrupted or contain only images.'}), 400
        
        # Split into chunks
        pdf_chunks = pdf_processor.split_text_into_chunks(pdf_text)
        if not pdf_chunks:
            return jsonify({'error': 'Failed to process PDF text into chunks'}), 400
        
        # Create vector store
        vector_store = pdf_processor.create_vector_store(pdf_chunks)
        if not vector_store:
            return jsonify({'error': 'Failed to create vector store for AI processing'}), 400
        
        current_filename = filename
        
        # Generate initial summary
        summary = ai_assistant.generate_summary(pdf_text)
        
        return jsonify({
            'message': f'PDF "{filename}" uploaded and processed successfully!',
            'filename': filename,
            'pages': len(pdf_chunks),
            'summary': summary
        })
        
    except Exception as e:
        print(f"Error in upload: {e}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/chat', methods=['POST'])
def chat():
    global vector_store, pdf_text
    
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        question = data.get('message', '').strip()
        if not question:
            return jsonify({'error': 'No question provided'}), 400
        
        if not vector_store:
            return jsonify({'error': 'No PDF uploaded yet. Please upload a PDF first.'}), 400
        
        # Answer the question using AI
        answer = ai_assistant.answer_question(question, vector_store)
        
        return jsonify({
            'response': answer,
            'question': question
        })
        
    except Exception as e:
        print(f"Error in chat: {e}")
        return jsonify({'error': f'Failed to process question: {str(e)}'}), 500

@app.route('/summary', methods=['GET'])
def get_summary():
    global pdf_text
    
    if not pdf_text:
        return jsonify({'error': 'No PDF uploaded yet'}), 400
    
    try:
        summary = ai_assistant.generate_summary(pdf_text)
        return jsonify({'summary': summary})
    except Exception as e:
        print(f"Error generating summary: {e}")
        return jsonify({'error': 'Failed to generate summary'}), 500

@app.route('/status', methods=['GET'])
def get_status():
    global current_filename, pdf_chunks, vector_store, mistral_client
    
    return jsonify({
        'has_pdf': bool(current_filename),
        'filename': current_filename,
        'chunks_count': len(pdf_chunks) if pdf_chunks else 0,
        'vector_store_ready': bool(vector_store),
        'mistral_ai_configured': bool(mistral_client)
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'PDF Chatbot backend is running with Mistral AI'})

if __name__ == '__main__':
    # Check if Mistral AI API key is set
    if not os.getenv('MISTRAL_API_KEY'):
        print("Warning: MISTRAL_API_KEY not found in environment variables.")
        print("Please set your Mistral AI API key to use AI features.")
        print("You can create a .env file with: MISTRAL_API_KEY=your_api_key_here")
        print("Get your free API key from: https://console.mistral.ai/")
    
    print("Starting PDF Chatbot backend with Mistral AI...")
    print("Make sure to set MISTRAL_API_KEY in your .env file for AI features")
    app.run(debug=True, host='0.0.0.0', port=5000)