import os
import hashlib
import json
import requests
from datetime import datetime
from fpdf import FPDF
from config import CONFIG
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from ollama import Client
import fitz  # PyMuPDF
import re

def strip_html_tags(text):
    if not text:
        return ""
    # Remove all HTML tags
    clean = re.sub(r'<.*?>', '', text)
    # Replace HTML entities (optional, simple ones)
    clean = clean.replace('&nbsp;', ' ').replace('&amp;', '&')
    return clean.strip()

class UserAuth:
    def __init__(self):
        self.user_db = CONFIG["user_db"]
        self.users = self._load_users()
        print(f"UserAuth initialized with {len(self.users)} registered users")

    def _load_users(self):
        try:
            if os.path.exists(self.user_db):
                with open(self.user_db, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Failed to load user database: {e}")
            return {}

    def _save_users(self):
        try:
            with open(self.user_db, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Failed to save user database: {e}")

    def register(self, username, password):
        try:
            if not username or not password:
                return False, "Username dan password tidak boleh kosong"
            if len(username) < 3:
                return False, "Username harus minimal 3 karakter"
            if len(password) < 6:
                return False, "Password harus minimal 6 karakter"
            if username in self.users:
                return False, "Username sudah ada"

            salt = os.urandom(16).hex()
            hashed_pw = hashlib.sha256((password + salt).encode()).hexdigest()
            
            self.users[username] = {
                "password": hashed_pw,
                "salt": salt,
                "created_at": datetime.now().isoformat(),
                "last_login": None
            }
            self._save_users()
            
            print(f"User registered: {username}")
            return True, "Registration berhasil"
        except Exception as e:
            print(f"Registration error: {e}")
            return False, f"Registration error: {str(e)}"

    def login(self, username, password):
        try:
            if username not in self.users:
                return False, "Username tidak ditemukan"
            
            user_data = self.users[username]
            salt = user_data.get("salt", "")
            hashed_pw = hashlib.sha256((password + salt).encode()).hexdigest()
            
            if hashed_pw == user_data["password"]:
                self.users[username]["last_login"] = datetime.now().isoformat()
                self._save_users()
                print(f"User logged in: {username}")
                return True, "Login successful"
            else:
                return False, "Incorrect password"
        except Exception as e:
            print(f"Login error: {e}")
            return False, f"Login error: {str(e)}"

class ChatPDF(FPDF):
    def __init__(self, current_model):
        super().__init__()
        self.current_model = current_model
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Laporan Percakapan AI', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 8, f"Model: {self.current_model} | Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1, 'C')
        self.ln(10)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')
        
    def add_chat_message(self, q_num, question, answer):
        # Question
        self.set_font('Arial', 'B', 12)
        self.multi_cell(0, 8, f"Pertanyaan {q_num}: {question}", 0, 'L')
        self.ln(2)
        
        # Answer
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 8, f"Jawaban: {answer}", 0, 'L')
        self.ln(8)
        
        # Add line separator
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

class HybridChatSystem:
    def __init__(self):
        try:
            print("Initializing HybridChatSystem...")
            self.ollama = Client(host=CONFIG["ollama_host"])
            self.available_models = self._fetch_available_models()
            self.current_model = CONFIG["default_model"] if CONFIG["default_model"] in self.available_models else (self.available_models[0] if self.available_models else "")
            print(f"Available models: {', '.join(self.available_models)}")
            print(f"Current model: {self.current_model}")
            
            self.embeddings = OllamaEmbeddings(
                base_url=CONFIG["ollama_host"],
                model=CONFIG["embedding_model"]
            )
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=CONFIG["chunk_size"],
                chunk_overlap=CONFIG["chunk_overlap"]
            )
            self.vectorstore = Chroma(
                embedding_function=self.embeddings,
                persist_directory=CONFIG["vector_db"]
            )
            print("RAG system initialized")
            
        except Exception as e:
            print(f"Failed to initialize HybridChatSystem: {e}")
            raise

    def _fetch_available_models(self):
        try:
            response = requests.get(
                f"{CONFIG['ollama_host']}/api/tags",
                timeout=10
            )
            if response.status_code == 200:
                models = response.json().get('models', [])
                model_names = [model['name'] for model in models]
                print(f"Fetched {len(model_names)} models: {model_names}")
                return model_names
            else:
                print(f"Failed to fetch models: HTTP {response.status_code}")
                return []
        except requests.exceptions.ConnectionError:
            print("Connection error: Ollama server is not running")
            return []
        except requests.exceptions.Timeout:
            print("Timeout error: Ollama server is not responding")
            return []
        except Exception as e:
            print(f"Couldn't fetch models: {e}")
            return []

    def get_available_models(self):
        """Public method to get available models"""
        return self._fetch_available_models()

    def set_model(self, model_name):
        if model_name in self.available_models:
            self.current_model = model_name
            print(f"Switched to model: {model_name}")
            return True
        print(f"Model not available: {model_name}")
        return False

    def process_pdf(self, file_path):
        """Process uploaded PDF file for RAG"""
        try:
            print(f"Processing PDF: {file_path}")
            
            if not os.path.exists(file_path):
                return False, "File not found"
            
            if not file_path.lower().endswith('.pdf'):
                return False, "Only PDF files are supported"
            
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                try:
                    text += page.get_text()
                except AttributeError:
                    text += page.getText()
            doc.close()
            
            if not text.strip():
                return False, "PDF contains no readable text"
            
            text = ' '.join(text.split())
            chunks = self.text_splitter.split_text(text)
            
            if not chunks:
                return False, "Failed to process PDF text"
            
            self.vectorstore = Chroma.from_texts(
                texts=chunks,
                embedding=self.embeddings,
                persist_directory=CONFIG["vector_db"]
            )
            
            print(f"PDF processed: {len(chunks)} chunks")
            return True, f"Document processed successfully ({len(chunks)} sections)"
            
        except Exception as e:
            print(f"PDF processing failed: {e}")
            return False, f"Failed to process PDF: {str(e)}"

    def generate_response(self, message, chat_history, use_rag=False):
        try:
            print(f"\nGenerating response for: {message}")
            print(f"Using RAG: {use_rag}")
            print(f"Current model: {self.current_model}")
            start_time = datetime.now()
            
            # Guard: ensure we have a valid model selected
            if not self.current_model or not isinstance(self.current_model, str) or not self.current_model.strip():
                warning_msg = (
                    "Error: Tidak ada model yang dipilih atau model kosong. "
                    "Pastikan Ollama berjalan dan model sudah ter-install (contoh: 'ollama pull gemma:7b'), "
                    "lalu klik 'Refresh Models' dan pilih model."
                )
                return "", chat_history + [
                    {"role": "user", "content": message},
                    {"role": "assistant", "content": warning_msg}
                ]
            
            # Coba jawab dengan model lokal dulu
            base_prompt = f"{CONFIG['system_prompt']}\n\nPertanyaan Pengguna: {message}\n\nBerikan jawaban yang lengkap dan detail."
            
            # Generate response dari model lokal
            response = self.ollama.generate(
                model=self.current_model,
                prompt=base_prompt,
                options={
                    'temperature': CONFIG["temperature"],
                    'num_predict': 2048,
                    'top_k': 40,
                    'top_p': 0.9
                }
            )
            answer = response['response'].strip()
            
            # Jika RAG aktif dan ada vectorstore, selalu gunakan konteks PDF untuk jawaban yang lebih lengkap
            if use_rag and self.vectorstore:
                print("RAG aktif - mencari konteks dari PDF untuk jawaban yang lebih lengkap...")
                
                # Cek apakah jawaban model mengandung kata-kata yang menunjukkan ketidakmampuan
                uncertainty_keywords = [
                    "maaf", "saya tidak tahu", "saya tidak bisa", "tidak dapat", 
                    "tidak yakin", "tidak memiliki informasi", "tidak ada data",
                    "sorry", "i don't know", "i cannot", "i'm not sure",
                    "tidak tersedia", "tidak ditemukan", "tidak ada informasi"
                ]
                
                answer_lower = answer.lower()
                needs_context = any(keyword in answer_lower for keyword in uncertainty_keywords)
                
                # Selalu gunakan konteks PDF jika tersedia untuk jawaban yang lebih lengkap
                if True:  # Selalu gunakan RAG ketika PDF tersedia
                    print("Mencari konteks dari PDF untuk jawaban yang lebih lengkap...")
                    # Gunakan lebih banyak dokumen untuk pertanyaan yang kompleks
                    k_docs = 15 if len(message.split()) > 5 else 10
                    docs = self.vectorstore.similarity_search(message, k=k_docs)
                    if docs:
                        context = "\n".join([doc.page_content for doc in docs])
                        enhanced_prompt = f"{base_prompt}\n\n=== KUTIPAN DARI PDF (gunakan untuk melengkapi jawaban) ===\n{context}\n=== END KUTIPAN ===\n\nJawab berdasarkan pengetahuan model dan kutipan di atas jika relevan. Berikan jawaban yang lengkap, detail, dan informatif. Jelaskan dengan baik dan berikan contoh jika diperlukan. Pastikan jawaban minimal 3-4 paragraf jika informasi tersedia."
                        print(f"Added context to prompt (first 200 chars): {context[:200]}...")
                        
                        # Generate response dengan konteks PDF
                        enhanced_response = self.ollama.generate(
                            model=self.current_model,
                            prompt=enhanced_prompt,
                            options={
                                'temperature': CONFIG["temperature"],
                                'num_predict': 2048,
                                'top_k': 40,
                                'top_p': 0.9
                            }
                        )
                        answer = enhanced_response['response'].strip()
                        print("Generated enhanced response with PDF context")
                    else:
                        print("No relevant PDF content found")
                else:
                    print("Model dapat menjawab dengan baik tanpa PDF context")
            
            if not answer:
                answer = "Maaf, saya tidak dapat memberikan jawaban saat ini."
                print("Warning: Empty response from model")
            
            response_time = (datetime.now() - start_time).total_seconds()
            
            # Tentukan mode yang digunakan
            if use_rag and self.vectorstore and needs_context:
                mode = "RAG (Enhanced)"
            elif use_rag and self.vectorstore:
                mode = "RAG (Available)"
            else:
                mode = "Direct"
            
            formatted_response = (
                f"{answer}\n\n"
                f"Response time: {response_time:.2f}s | "
                f"Model: {self.current_model} | "
                f"Mode: {mode}"
            )
            print(f"Generated response (first 200 chars): {formatted_response[:200]}...")
            return "", chat_history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": formatted_response}
            ]
        except Exception as e:
            print(f"Error in generate_response: {str(e)}")
            error_msg = f"Error: {str(e)}"
            if "connection" in str(e).lower():
                error_msg = "Error: Tidak dapat terhubung ke Ollama. Pastikan server Ollama berjalan!"
            return "", chat_history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": error_msg}
            ]

    def export_chat_to_pdf(self, chat_history, username):
        try:
            if not chat_history:
                return False, "No chat history available"
            
            print(f"Processing chat history for PDF export: {len(chat_history)} messages")
            print(f"First few messages: {chat_history[:3]}")
            
            os.makedirs(CONFIG["temp_dir"], exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_{username}_{timestamp}.pdf"
            filepath = os.path.join(CONFIG["temp_dir"], filename)
            
            pdf = ChatPDF(self.current_model)
            q_num = 1
            i = 0
            
            while i < len(chat_history):
                msg = chat_history[i]
                if isinstance(msg, dict) and msg.get("role") == "user":
                    question = strip_html_tags(msg.get("content", ""))
                    answer = ""
                    # Look for the next assistant message
                    for j in range(i+1, len(chat_history)):
                        next_msg = chat_history[j]
                        if isinstance(next_msg, dict) and next_msg.get("role") == "assistant":
                            answer = strip_html_tags(next_msg.get("content", ""))
                            break
                    if question and answer:  # Only add if both question and answer exist
                        pdf.add_chat_message(q_num, question, answer)
                        q_num += 1
                i += 1
            
            pdf.output(filepath)
            
            if os.path.exists(filepath):
                print(f"Exported chat to: {filepath}")
                return True, filepath
            else:
                return False, "Failed to create PDF file"
        except Exception as e:
            print(f"PDF export failed: {e}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            return False, f"PDF export error: {str(e)}"