import os

# Configuration for RAG Chatbot
CONFIG = {
    # Ollama Configuration
    "ollama_host": "http://localhost:11434",
    "ollama_timeout": 30,
    "default_model": "gemma:7b",
    "embedding_model": "nomic-embed-text",
    
    # RAG Settings
    "chunk_size": 800,
    "chunk_overlap": 100,
    "temperature": 0.8,
    "system_prompt": "Anda adalah asisten AI yang selalu merespons dalam bahasa Indonesia. Berikan jawaban yang lengkap, detail, dan informatif. Jelaskan dengan baik dan berikan contoh jika diperlukan.",
    
    # Response Prefixes
    "rag_prefix": "[Dokumen]",
    "direct_prefix": "[Langsung]",
    
    # Storage
    "temp_dir": "temp_pdf",
    "user_db": "users.json",
    "chat_history_dir": "chat_history",
    "pdf_storage": "./pdf_db/",
    "vector_db": "vector_db",
    
    # Performance Settings
    "max_retries": 3,
    "timeout": 30,
    "max_file_size": 50 * 1024 * 1024,  # 50MB
    "supported_formats": [".pdf"],
    
    # UI Theme
    "theme": {
        "primary_color": "#6e6ee6",
        "secondary_color": "#f9f9ff",
        "neutral_color": "#e0e0e6"
    }
}

# Create required directories
for path in [CONFIG["temp_dir"], CONFIG["chat_history_dir"], CONFIG["pdf_storage"], CONFIG["vector_db"]]:
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory created: {path}")
    except Exception as e:
        print(f"Failed to create directory {path}: {e}")