import os
import json
import time
from datetime import datetime
from model import UserAuth, HybridChatSystem, strip_html_tags
import gradio as gr
from config import CONFIG
import markdown as md

print("Initializing logic module...")

# Initialize systems
auth = UserAuth()
chat_system = HybridChatSystem()


def register(username, password):
    """Handle user registration"""
    success, message = auth.register(username, password)
    status = "success" if success else "error"
    return message, status


def reset_password(username):
    """Reset user password to '1234'"""
    try:
        if not username:
            return "Username tidak boleh kosong", "error"

        # Load existing users
        users_file = "users.json"
        if not os.path.exists(users_file):
            return "User tidak ditemukan", "error"

        with open(users_file, 'r', encoding='utf-8') as f:
            users = json.load(f)

        # Check if user exists
        if username not in users:
            return "User tidak ditemukan", "error"

        # Generate new salt and hash password '1234'
        import hashlib
        import os
        salt = os.urandom(16).hex()
        hashed_pw = hashlib.sha256(("1234" + salt).encode()).hexdigest()

        # Update user data with new password hash and salt
        users[username]["password"] = hashed_pw
        users[username]["salt"] = salt

        # Save updated users
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

        return f"Password untuk user '{username}' berhasil direset menjadi '1234'", "success"
    except Exception as e:
        print(f"Error resetting password: {e}")
        return f"Gagal reset password: {str(e)}", "error"


def login(username, password):
    """Handle user login and return UI updates"""
    if not username or not password:
        status_html = "<span class='login-status-black error'>Username dan password tidak boleh kosong</span>"
        return (
            gr.update(visible=True),
            gr.update(visible=False),
            False,
            "",
            status_html
        )
    success, message = auth.login(username, password)
    status_html = f"<span class='login-status-black'>{message}</span>"
    if success:
        return (
            gr.update(visible=False),  # Hide login container
            gr.update(visible=True),   # Show main container
            True,                      # Update login state
            username,                  # Store username
            status_html                # Status message
        )
    return (
        gr.update(visible=True),       # Keep login visible
        gr.update(visible=False),      # Keep main hidden
        False,                         # Update login state
        "",                            # Empty username
        status_html                    # Error message
    )


def save_history(username, chat_history):
    """Save chat history to JSON file"""
    try:
        if not username:
            return

        os.makedirs(CONFIG["chat_history_dir"], exist_ok=True)
        filepath = os.path.join(CONFIG["chat_history_dir"], f"{username}.json")

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(chat_history, f, ensure_ascii=False, indent=2)
        print(f"Saved chat history for {username}: {len(chat_history)} messages")
    except Exception as e:
        print(f"Error saving history: {e}")


def load_history(username):
    """Load chat history from JSON file and convert to HTML format"""
    try:
        if not username:
            return ""

        filepath = os.path.join(CONFIG["chat_history_dir"], f"{username}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                history = json.load(f)

                html_history = ""
                for i in range(0, len(history), 2):
                    if i + 1 < len(history):
                        user_msg = history[i]["content"] if history[i]["role"] == "user" else ""
                        bot_msg = history[i + 1]["content"] if history[i + 1]["role"] == "assistant" else ""

                        user_msg = strip_html_tags(user_msg)
                        bot_msg = strip_html_tags(bot_msg)

                        if user_msg and bot_msg:
                            try:
                                bot_msg_html = md.markdown(bot_msg, extensions=['extra'])
                            except Exception:
                                import re
                                bot_msg_html = re.sub(r'\* (.+)', r'<ul><li>\1</li></ul>', bot_msg)

                            user_bubble = f'''
                            <div class="message user-message">
                                <div class="message-label">Anda</div>
                                <div class="message-content">{user_msg}</div>
                                <div class="message-meta">--:--</div>
                            </div>'''

                            bot_bubble = f'''
                            <div class="message bot-message">
                                <div class="message-label">Bot</div>
                                <div class="message-content">{bot_msg_html}</div>
                                <div class="message-meta">--:--</div>
                            </div>'''

                            html_history += user_bubble + bot_bubble
                return html_history
        return ""
    except Exception as e:
        print(f"Error loading history: {e}")
        return ""


def load_chat_history_for_export(username):
    """Load chat history from JSON file in format suitable for PDF export"""
    try:
        if not username:
            return []

        filepath = os.path.join(CONFIG["chat_history_dir"], f"{username}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                history = json.load(f)

                formatted_history = []
                for i in range(0, len(history), 2):
                    if i + 1 < len(history):
                        user_msg = history[i]["content"] if history[i]["role"] == "user" else ""
                        bot_msg = history[i + 1]["content"] if history[i + 1]["role"] == "assistant" else ""

                        user_msg = strip_html_tags(user_msg)
                        bot_msg = strip_html_tags(bot_msg)

                        if user_msg and bot_msg:
                            formatted_history.append({"role": "user", "content": user_msg})
                            formatted_history.append({"role": "assistant", "content": bot_msg})
                return formatted_history
        return []
    except Exception as e:
        print(f"Error loading chat history for export: {e}")
        return []


def get_models():
    """Get available models excluding embedding model"""
    try:
        models = chat_system.get_available_models()
        # Do not show fallback models in the dropdown; if empty, return empty list
        if not models:
            return []
        return [m for m in models if m != CONFIG["embedding_model"]]
    except Exception as e:
        print(f"Error getting models: {e}")
        # On error, return empty to avoid misleading selections
        return []


def respond(message, chat_history, use_rag, is_logged_in, username):
    try:
        if not message or not message.strip():
            return "", "", chat_history

        now = datetime.now().strftime("%H:%M")
        user_bubble = f'''
        <div class="message user-message">
            <div class="bubble">
                <div class="message-content">{message}</div>
                <div class="message-meta">{now}</div>
            </div>
        </div>'''

        if isinstance(chat_history, str):
            html_history = chat_history
        else:
            html_history = "".join([a + b for a, b in chat_history]) if chat_history else ""

        internal_history = []
        if isinstance(chat_history, list):
            for msg in chat_history:
                if isinstance(msg, (list, tuple)) and len(msg) == 2:
                    internal_history.append({"role": "user", "content": msg[0]})
                    internal_history.append({"role": "assistant", "content": msg[1]})
                elif isinstance(msg, dict):
                    internal_history.append(msg)

        t0 = time.time()
        _, new_history = chat_system.generate_response(
            message=message,
            chat_history=internal_history,
            use_rag=use_rag
        )
        response_time = time.time() - t0

        bot_msg = ""
        model_name = getattr(chat_system, 'current_model', 'model')
        mode_str = "RAG" if use_rag else "Direct"
        for i in range(len(new_history) - 1, -1, -1):
            if new_history[i]["role"] == "assistant":
                bot_msg = new_history[i]["content"]
                break

        try:
            bot_msg_html = md.markdown(bot_msg, extensions=['extra'])
        except Exception:
            import re
            bot_msg_html = re.sub(r'\* (.+)', r'<ul><li>\1</li></ul>', bot_msg)

        bot_bubble = f'''
        <div class="message bot-message">
            <div class="bubble">
                <div class="message-content">{bot_msg_html}</div>
                <div class="message-meta">{datetime.now().strftime("%H:%M")} | Model: {model_name} | Mode: {mode_str} | Response: {response_time:.2f}s</div>
            </div>
        </div>'''

        html_history += user_bubble + bot_bubble
        print(f"USER ({now}): {message}")
        print(f"BOT ({datetime.now().strftime('%H:%M')}): {bot_msg}")
        return "", html_history, html_history
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print("[RESPOND ERROR]", error_detail)
        error_msg = f"Maaf, terjadi kesalahan: {str(e)}<br><pre style='color:#b91c1c;font-size:0.95em'>{error_detail}</pre>"
        user_bubble = f'<div class="message user-message"><div class="bubble"><div class="message-content">{message}</div></div></div>'
        bot_bubble = f'<div class="message bot-message"><div class="bubble"><div class="message-content">{error_msg}</div></div></div>'
        if isinstance(chat_history, str):
            return "", chat_history + user_bubble + bot_bubble, chat_history + user_bubble + bot_bubble
        else:
            html_history = "".join([a + b for a, b in chat_history]) if chat_history else ""
            return "", html_history + user_bubble + bot_bubble, html_history + user_bubble + bot_bubble


def process_pdf(file):
    """Process uploaded PDF file for RAG"""
    if file:
        print(f"Processing PDF file: {file.name}")
        success, message = chat_system.process_pdf(file.name)
        return f"{message}" if success else f"{message}"
    return "Silakan upload file PDF terlebih dahulu"


def export_chat(chat_history, username):
    """Export active chat (list Q&A) to PDF."""
    print(f"Exporting chat for user: {username}")
    print(f"Current chat_history format: {type(chat_history)} with {len(chat_history) if chat_history else 0} items")
    print(f"Chat history content: {chat_history}")

    if not chat_history or not isinstance(chat_history, list) or len(chat_history) == 0:
        print("Chat history is empty or invalid")
        return None, "Tidak ada riwayat percakapan untuk diekspor"

    print(f"Final chat history for export: {len(chat_history)} items")
    print(f"First few items: {chat_history[:3]}")

    try:
        success, result = chat_system.export_chat_to_pdf(
            chat_history=chat_history,
            username=username
        )
        if success:
            print(f"PDF generated successfully: {result}")
            return gr.File(value=result, visible=True), f"Chat berhasil diekspor: {result}"
        print(f"Failed to generate PDF: {result}")
        return None, f"Gagal mengekspor chat: {result}"
    except Exception as e:
        import traceback
        print("[EXPORT_CHAT ERROR]", traceback.format_exc())
        return None, f"Gagal parsing chat: {str(e)}"


def export_chat_from_html(chat_html_history, username):
    """Export active chat from HTML history to PDF, sertakan timestamp, model, mode, response time di setiap Q&A."""
    print(f"Exporting chat from HTML for user: {username}")
    print(f"HTML history length: {len(chat_html_history) if chat_html_history else 0}")

    if not chat_html_history:
        return None, "Tidak ada riwayat percakapan untuk diekspor"

    try:
        import re
        from model import strip_html_tags
        user_pattern = r'<div class="message user-message">.*?<div class="bubble">.*?<div class="message-content">(.*?)</div>.*?<div class="message-meta">(.*?)</div>.*?</div>'
        bot_pattern = r'<div class="message bot-message">.*?<div class="bubble">.*?<div class="message-content">(.*?)</div>.*?<div class="message-meta">(.*?)</div>.*?</div>'
        user_msgs = re.findall(user_pattern, chat_html_history, re.DOTALL)
        bot_msgs = re.findall(bot_pattern, chat_html_history, re.DOTALL)
        print(f"Found {len(user_msgs)} user messages and {len(bot_msgs)} bot messages")
        if len(user_msgs) == 0 or len(bot_msgs) == 0:
            return None, "Tidak ada riwayat percakapan untuk diekspor"

        chat_history = []
        for i, (u, b) in enumerate(zip(user_msgs, bot_msgs)):
            q, qmeta = u
            a, ameta = b
            q = strip_html_tags(q)
            a = strip_html_tags(a)
            qmeta = strip_html_tags(qmeta)
            ameta = strip_html_tags(ameta)
            if q and a:
                chat_history.append({"role": "user", "content": f"[{qmeta}] {q}"})
                chat_history.append({"role": "assistant", "content": f"[{ameta}] {a}"})
                print(f"Added Q&A pair {i+1}: Q='{q[:50]}...' A='{a[:50]}...' META: {ameta}")

        if not chat_history:
            return None, "Tidak ada riwayat percakapan untuk diekspor"

        print(f"Final chat history for export: {len(chat_history)} items")
        success, result = chat_system.export_chat_to_pdf(
            chat_history=chat_history,
            username=username
        )
        if success:
            print(f"PDF generated successfully: {result}")
            return gr.File(value=result, visible=True), f"Chat berhasil diekspor: {result}"
        print(f"Failed to generate PDF: {result}")
        return None, f"Gagal mengekspor chat: {result}"
    except Exception as e:
        import traceback
        print("[EXPORT_CHAT_FROM_HTML ERROR]", traceback.format_exc())
        return None, f"Gagal parsing chat: {str(e)}"


def clear_chat():
    """Clear the chat history"""
    return []


def refresh_models():
    """Refresh available models list"""
    try:
        chat_system.available_models = chat_system._fetch_available_models()

        if not chat_system.available_models:
            return (
                gr.update(choices=[], value=""),
                "Tidak ada model yang tersedia. Pastikan Ollama berjalan!"
            )

        if chat_system.current_model not in chat_system.available_models:
            chat_system.current_model = chat_system.available_models[0]

        embedding_model = CONFIG["embedding_model"]
        embedding_installed = embedding_model in chat_system.available_models
        status_suffix = (
            f" | Embedding: {embedding_model} {'TERPASANG' if embedding_installed else 'TIDAK DITEMUKAN (jalankan: ollama pull ' + embedding_model + ')'}"
        )
        return (
            gr.update(
                choices=[m for m in chat_system.available_models
                         if m != CONFIG["embedding_model"]],
                value=chat_system.current_model
            ),
            f"Model tersedia: {', '.join(chat_system.available_models)}{status_suffix}"
        )
    except Exception as e:
        print(f"Error refreshing models: {e}")
        return (
            gr.update(choices=[], value=""),
            f"Error: {str(e)}"
        )


def update_model(model_name):
    """Update the current model"""
    try:
        if chat_system.set_model(model_name):
            return f"Model berhasil diubah ke: {model_name}"
        return f"Gagal mengubah model: {model_name} tidak tersedia"
    except Exception as e:
        print(f"Error updating model: {e}")
        return f"Error: {str(e)}"


print("Logic module initialized successfully")
