import os
import json
import re
from model import strip_html_tags

def clean_chat_history_files():
    """Clean all chat history files from HTML tags"""
    chat_dir = "chat_history"
    
    if not os.path.exists(chat_dir):
        print("Chat history directory not found")
        return
    
    cleaned_count = 0
    
    for filename in os.listdir(chat_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(chat_dir, filename)
            print(f"Cleaning {filename}...")
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                
                # Clean each message
                cleaned_history = []
                for msg in history:
                    if isinstance(msg, dict) and "content" in msg:
                        cleaned_content = strip_html_tags(msg["content"])
                        # Remove extra whitespace and timestamps
                        cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()
                        # Remove timestamp patterns like "21:07   Anda" or "21:08   Bot"
                        cleaned_content = re.sub(r'\d{1,2}:\d{2}\s+\w+$', '', cleaned_content).strip()
                        
                        if cleaned_content:  # Only keep non-empty messages
                            cleaned_history.append({
                                "role": msg["role"],
                                "content": cleaned_content
                            })
                
                # Save cleaned data
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(cleaned_history, f, ensure_ascii=False, indent=2)
                
                print(f"  Cleaned {len(history)} -> {len(cleaned_history)} messages")
                cleaned_count += 1
                
            except Exception as e:
                print(f"  Error cleaning {filename}: {e}")
    
    print(f"\nCleaned {cleaned_count} files")

if __name__ == "__main__":
    clean_chat_history_files() 