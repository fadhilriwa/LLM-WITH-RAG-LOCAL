import gradio as gr
from logic import (
    login, 
    register, 
    reset_password,
    respond, 
    process_pdf, 
    export_chat, 
    export_chat_from_html,
    clear_chat,
    update_model,
    refresh_models,
    get_models,
    load_history,
    save_history
)
from model import strip_html_tags

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

/* Global scroll prevention - but allow scroll in chat area */
* {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Allow scroll only in chat area */
.full-chat-area, #chat-html-history {
  overscroll-behavior: auto !important;
  touch-action: pan-y !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Prevent scroll on all other elements */
.navbar-chat, .sidebar, .full-input-area, .main-content-row, .chat-content, .main-app-layout {
  overflow: hidden !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

/* Ensure only chat area can scroll */
.chat-content > div:first-child {
  overflow: hidden !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

.chat-content > div:first-child > div {
  overflow: hidden !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

/* Prevent scroll on all elements */
html, body, div, form, input, button, textarea, label, span, p, h1, h2, h3, h4, h5, h6 {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Gradio specific scroll prevention */
.gradio-container, .gradio-interface, .gradio-app, #root {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: hidden !important;
  height: 100vh !important;
  width: 100vw !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}

/* Prevent scroll on all containers */
.container, .main-container, .login-container, .form-container {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: hidden !important;
}

/* Specific login scroll prevention */
.login-bg, .login-card, .login-form-dark, .input-field, .btn-login, .btn-register, .btn-forgot, .status-message {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: hidden !important;
}

/* Additional Gradio scroll prevention */
.gradio-container *, .gradio-interface *, .gradio-app * {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Prevent scroll on all Gradio elements */
.gradio-container, .gradio-interface, .gradio-app, .gradio-container > div, .gradio-interface > div, .gradio-app > div {
  overflow: hidden !important;
  height: 100vh !important;
  width: 100vw !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}

/* Prevent scroll on all form elements and containers */
.gradio-container form, .gradio-interface form, .gradio-app form,
.gradio-container .form, .gradio-interface .form, .gradio-app .form,
.gradio-container .container, .gradio-interface .container, .gradio-app .container {
  overflow: visible !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Prevent scroll on all Gradio blocks and components */
.gradio-container .block, .gradio-interface .block, .gradio-app .block,
.gradio-container .component, .gradio-interface .component, .gradio-app .component,
.gradio-container .column, .gradio-interface .column, .gradio-app .column,
.gradio-container .row, .gradio-interface .row, .gradio-app .row {
  overflow: visible !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Prevent scroll on all input containers */
.gradio-container input, .gradio-interface input, .gradio-app input,
.gradio-container textarea, .gradio-interface textarea, .gradio-app textarea,
.gradio-container select, .gradio-interface select, .gradio-app select {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: visible !important;
}

/* Prevent scroll on all button elements */
.gradio-container button, .gradio-interface button, .gradio-app button {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: visible !important;
}

/* Prevent scroll on all div elements */
.gradio-container div, .gradio-interface div, .gradio-app div {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: visible !important;
}

/* Specific prevention for login forms */
.login-form-dark, .login-form-dark *, 
.register-form-dark, .register-form-dark *,
.forgot-form-dark, .forgot-form-dark * {
  overflow: hidden !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Force no scroll on all Gradio elements */
.gradio-container, .gradio-interface, .gradio-app,
.gradio-container *, .gradio-interface *, .gradio-app * {
  overflow: visible !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Prevent scroll on all HTML elements */
html *, body * {
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: visible !important;
}

/* Specific login scroll prevention */
.login-bg, .login-card, .login-form-dark, .input-field, .btn-login, .btn-register, .btn-forgot, .status-message {
  overflow: visible !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Prevent scroll on all login elements */
.login-bg *, .login-card *, .login-form-dark *, .input-field *, .btn-login *, .btn-register *, .btn-forgot *, .status-message * {
  overflow: visible !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

/* Prevent scroll on all form elements */
form, form *, input, input *, textarea, textarea *, button, button * {
  overflow: visible !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

html, body {
  margin: 0 !important;
  padding: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  overflow: hidden !important;
  font-family: 'Poppins', Arial, sans-serif;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  -webkit-overflow-scrolling: touch !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  min-height: 100vh !important;
  max-height: 100vh !important;
}

/* Ensure main app layout doesn't scroll */
.main-app-layout {
  overflow: hidden !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

body {
  font-family: 'Poppins', Arial, sans-serif;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  margin: 0 !important;
  padding: 0 !important;
  width: 100vw !important;
  height: 100vh !important;
  overflow: hidden !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  min-height: 100vh !important;
  max-height: 100vh !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
}

.login-bg {
  width: 100vw !important;
  height: 100vh !important;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  padding: 20px;
  box-sizing: border-box;
  overflow: visible !important;
  position: fixed !important;
  top: 0 !important;
  left: 0 !important;
  right: 0 !important;
  bottom: 0 !important;
  min-height: 100vh !important;
  max-height: none !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}



.login-form-dark {
  background: #334155;
  border-radius: 16px;
  padding: 1.2rem;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  font-family: 'Poppins', Arial, sans-serif;
  border: 1px solid #475569;
  overflow: visible !important;
  max-height: none !important;
  height: auto !important;
  min-height: auto !important;
  flex-shrink: 0;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

.input-label {
  display: block;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #fff;
  font-size: 0.9rem;
  font-weight: 700;
  border-radius: 10px;
  padding: 0.4rem 1rem;
  margin-bottom: 0.4rem;
  font-family: 'Poppins', Arial, sans-serif;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
  text-align: center;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: hidden !important;
}

.input-field {
  width: 100%;
  border: none;
  outline: none;
  font-size: 1rem;
  font-family: 'Poppins', Arial, sans-serif;
  background: #1e293b;
  padding: 0.8rem 1rem;
  border-radius: 12px;
  color: #e5e7eb;
  border: 1px solid #475569;
  transition: all 0.3s ease;
  box-sizing: border-box;
  line-height: 1.4;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: hidden !important;
}

.input-field:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
  transform: translateY(-1px);
}

.input-field::placeholder {
  color: #94a3b8;
  font-family: 'Poppins', Arial, sans-serif;
  font-size: 1rem;
}

.login-btn-row {
  display: flex;
  gap: 1rem;
  width: 100%;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: hidden !important;
}

.btn-login {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #fff;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 600;
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Poppins', Arial, sans-serif;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
  flex: 1;
  position: relative;
  overflow: hidden !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

.btn-login::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.btn-login:hover::before {
  left: 100%;
}

.btn-login:hover {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
}

.btn-register {
  background: transparent;
  color: #3b82f6;
  border: 2px solid #3b82f6;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Poppins', Arial, sans-serif;
  flex: 1;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: hidden !important;
}

.btn-register:hover {
  background: #3b82f6;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}

.btn-forgot {
  background: transparent;
  color: #94a3b8;
  border: none;
  border-radius: 10px;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 0.8rem 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: 'Poppins', Arial, sans-serif;
  text-decoration: underline;
  text-underline-offset: 2px;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: hidden !important;
}

.btn-forgot:hover {
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
  transform: translateY(-1px);
}

.status-message {
  padding: 12px 16px;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 8px;
  font-family: 'Poppins', Arial, sans-serif;
  text-align: center;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  overflow: hidden !important;
}

.status-message.error {
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.status-message.success {
  background: #dcfce7;
  color: #16a34a;
  border: 1px solid #bbf7d0;
}
.main-app-layout {
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
  background: #0f172a;
  color: #e5e7eb;
  font-family: 'Poppins', Arial, sans-serif;
  overflow: hidden !important;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

.navbar-chat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #1e293b 0%, #23283a 100%);
  padding: 20px 32px;
  height: 72px;
  border-bottom: 2px solid #334155;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  flex-shrink: 0;
  min-height: 72px;
  max-height: 72px;
  position: relative;
  overflow: hidden !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

.navbar-chat::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, #5b4df6, #3b82f6, #2563eb);
}

.navbar-title {
  font-size: 2rem;
  font-weight: 800;
  color: #5b4df6;
  font-family: 'Poppins', Arial, sans-serif;
  letter-spacing: -0.02em;
  text-shadow: 0 2px 8px rgba(91, 77, 246, 0.3);
  position: relative;
}

.navbar-title::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #5b4df6, transparent);
  border-radius: 1px;
}

.model-dropdown {
  width: 220px;
  border-radius: 12px;
  font-size: 1rem;
  background: #334155;
  color: #e5e7eb;
  border: 2px solid #475569;
  font-family: 'Poppins', Arial, sans-serif;
  padding: 12px 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.model-dropdown:focus {
  border-color: #5b4df6;
  box-shadow: 0 0 0 3px rgba(91, 77, 246, 0.15);
  outline: none;
}

.main-content-row {
  display: flex;
  flex: 1;
  height: calc(100vh - 64px);
  overflow: hidden;
  min-height: 0;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #0f172a;
  height: 100%;
  overflow: hidden;
  min-height: 0;
  position: relative;
  justify-content: space-between;
  max-height: calc(100vh - 72px);
}

.sidebar {
  background: linear-gradient(180deg, #1e293b 0%, #23283a 100%);
  width: 280px;
  min-width: 280px;
  max-width: 280px;
  height: 100%;
  border-right: 2px solid #334155;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 24px 20px;
  gap: 16px;
  overflow-y: auto;
  flex-shrink: 0;
  box-sizing: border-box;
  scrollbar-width: thin;
  scrollbar-color: #5b4df6 #1e293b;
  position: relative;
  min-height: 100vh;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

.sidebar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #5b4df6, #3b82f6, #2563eb);
}

.sidebar::-webkit-scrollbar {
  width: 8px;
}

.sidebar::-webkit-scrollbar-track {
  background: #1e293b;
  border-radius: 4px;
}

.sidebar::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #5b4df6, #3b82f6);
  border-radius: 4px;
  border: 1px solid #334155;
}

.sidebar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #3b82f6, #2563eb);
}

.sidebar-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #5b4df6;
  margin-bottom: 12px;
  font-family: 'Poppins', Arial, sans-serif;
  letter-spacing: -0.01em;
  text-shadow: 0 2px 8px rgba(91, 77, 246, 0.3);
  position: relative;
  padding-left: 12px;
}

.sidebar-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 4px;
  height: 24px;
  background: linear-gradient(180deg, #5b4df6, #3b82f6);
  border-radius: 2px;
}

.menu-item {
  font-size: 1rem;
  color: #e5e7eb;
  font-weight: 600;
  background: linear-gradient(135deg, #334155, #475569);
  border-radius: 14px;
  padding: 12px 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  margin-bottom: 10px;
  font-family: 'Poppins', Arial, sans-serif;
  border: 2px solid transparent;
  outline: none;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  width: 100%;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.menu-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.menu-item:hover::before {
  left: 100%;
}

.menu-item:focus, .menu-item:hover, .menu-item.active {
  background: linear-gradient(135deg, #5b4df6, #3b82f6);
  color: #fff;
  box-shadow: 0 6px 20px rgba(91, 77, 246, 0.4);
  transform: translateY(-2px);
  border-color: #5b4df6;
}

.menu-item.active {
  background: linear-gradient(135deg, #5b4df6, #3b82f6);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 8px 24px rgba(91, 77, 246, 0.5);
}

.model-settings-title {
  color: #5b4df6;
  font-size: 1.2rem;
  font-weight: 700;
  margin-top: 24px;
  margin-bottom: 16px;
  letter-spacing: 0.01em;
  position: relative;
  padding-left: 12px;
}

.model-settings-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 3px;
  height: 20px;
  background: linear-gradient(180deg, #5b4df6, #3b82f6);
  border-radius: 2px;
}

.btn-refresh, .btn-export, .btn-upload {
  background: linear-gradient(135deg, #334155, #475569);
  color: #e5e7eb;
  border: 2px solid transparent;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 600;
  padding: 14px 18px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Poppins', Arial, sans-serif;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  width: 100%;
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
}

.btn-refresh::before, .btn-export::before, .btn-upload::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

.btn-refresh:hover::before, .btn-export:hover::before, .btn-upload:hover::before {
  left: 100%;
}

.btn-refresh:hover, .btn-export:hover, .btn-upload:hover {
  background: linear-gradient(135deg, #5b4df6, #3b82f6);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(91, 77, 246, 0.4);
  border-color: #5b4df6;
}

.btn-rag {
  background: linear-gradient(135deg, #1e293b, #334155);
  color: #5b4df6;
  border: 2px solid #5b4df6;
  border-radius: 14px;
  font-size: 1rem;
  font-weight: 600;
  padding: 14px 18px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Poppins', Arial, sans-serif;
  width: 100%;
  margin-bottom: 12px;
  position: relative;
  overflow: hidden;
}

.btn-rag::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(91, 77, 246, 0.1), transparent);
  transition: left 0.5s ease;
}

.btn-rag:hover::before {
  left: 100%;
}

.btn-rag:hover {
  background: linear-gradient(135deg, #5b4df6, #3b82f6);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(91, 77, 246, 0.4);
}

.navbar-chat {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #23283a;
  box-shadow: 0 2px 16px #23283a33;
  padding: 1rem 2rem 1rem 2rem;
  border-bottom: 1.5px solid #23283a;
  position: sticky;
  top: 0;
  z-index: 15;
  min-height: 56px;
}
.navbar-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #5b4df6;
  font-family: 'Poppins', Arial, sans-serif;
  letter-spacing: 0.01em;
}
.full-chat-area {
  flex: 1 !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 1.5rem !important;
  padding: 2rem 2rem 6rem 2rem !important;
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
  min-height: 0 !important;
  box-sizing: border-box !important;
  scrollbar-width: 12px !important;
  scrollbar-color: #5b4df6 #0f172a !important;
  position: relative !important;
  max-height: calc(100vh - 200px) !important;
  height: 100% !important;
  overscroll-behavior: auto !important;
  touch-action: pan-y !important;
  -webkit-overflow-scrolling: touch !important;
}

.full-chat-area::-webkit-scrollbar {
  width: 12px;
}

.full-chat-area::-webkit-scrollbar-track {
  background: #0f172a;
  border-radius: 4px;
}

.full-chat-area::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #5b4df6, #3b82f6);
  border-radius: 6px;
  border: 1px solid #334155;
  min-height: 50px;
}

.full-chat-area::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #3b82f6, #2563eb);
}

/* Ensure smooth scrolling */
.full-chat-area {
  scroll-behavior: smooth !important;
  -webkit-overflow-scrolling: touch !important;
  overflow-y: scroll !important;
  scrollbar-width: auto !important;
  overscroll-behavior: auto !important;
  touch-action: pan-y !important;
}

/* Force scrollbar to always be visible */
.full-chat-area::-webkit-scrollbar {
  width: 12px !important;
  display: block !important;
  background: #0f172a !important;
}

.full-chat-area::-webkit-scrollbar-track {
  background: #0f172a !important;
  border-radius: 6px !important;
  border: 1px solid #334155 !important;
}

.full-chat-area::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #5b4df6, #3b82f6) !important;
  border-radius: 6px !important;
  border: 1px solid #334155 !important;
  min-height: 40px !important;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3) !important;
}

.full-chat-area::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #3b82f6, #2563eb) !important;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5) !important;
}

.full-chat-area::-webkit-scrollbar-corner {
  background: #0f172a !important;
}

/* Auto-scroll to bottom for new messages */
.full-chat-area:focus-within {
  scroll-behavior: smooth !important;
}

/* Ensure chat area is scrollable */
#chat-html-history {
  overflow-y: auto !important;
  overflow-x: hidden !important;
  scroll-behavior: smooth !important;
  -webkit-overflow-scrolling: touch !important;
  overscroll-behavior: auto !important;
  touch-action: pan-y !important;
  max-height: calc(100vh - 200px) !important;
  height: 100% !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 1.5rem !important;
  padding: 2rem 2rem 6rem 2rem !important;
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
  box-sizing: border-box !important;
  position: relative !important;
  scrollbar-width: 12px !important;
  scrollbar-color: #5b4df6 #0f172a !important;
}

/* Force scrollbar to be visible */


/* Ensure main content row allows proper sizing */
.main-content-row {
  display: flex !important;
  flex: 1 !important;
  height: calc(100vh - 72px) !important;
  overflow: hidden !important;
  min-height: 0 !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

/* Ensure chat area takes remaining space */
.chat-content {
  flex: 1 !important;
  display: flex !important;
  flex-direction: column !important;
  background: #0f172a !important;
  height: 100% !important;
  overflow: hidden !important;
  min-height: 0 !important;
  position: relative !important;
  justify-content: space-between !important;
  max-height: calc(100vh - 72px) !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

/* Ensure chat area content is properly scrollable */
.chat-content > div:first-child {
  flex: 1 !important;
  overflow: hidden !important;
  min-height: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

/* Force chat area to be scrollable */
.chat-content > div:first-child > div {
  flex: 1 !important;
  overflow: hidden !important;
  min-height: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

/* Ensure the actual chat area can scroll */
.chat-content > div:first-child > div > div {
  overflow-y: scroll !important;
  overflow-x: hidden !important;
  scrollbar-width: 12px !important;
  scrollbar-color: #5b4df6 #0f172a !important;
  -webkit-overflow-scrolling: touch !important;
  scroll-behavior: smooth !important;
  overscroll-behavior: auto !important;
  touch-action: pan-y !important;
  max-height: calc(100vh - 200px) !important;
  height: 100% !important;
  min-height: 400px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 1.5rem !important;
  padding: 2rem 2rem 6rem 2rem !important;
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
  box-sizing: border-box !important;
  position: relative !important;
}

/* Force scrollbar visibility and functionality - ONLY in chat area */
.full-chat-area, #chat-html-history {
  overflow-y: scroll !important;
  overflow-x: hidden !important;
  scrollbar-width: 12px !important;
  scrollbar-color: #5b4df6 #0f172a !important;
  -webkit-overflow-scrolling: touch !important;
  scroll-behavior: smooth !important;
  overscroll-behavior: auto !important;
  touch-action: pan-y !important;
  /* Ensure this is the ONLY scrollable area */
  position: relative !important;
  z-index: 1 !important;
  /* Force scroll to work */
  max-height: calc(100vh - 200px) !important;
  height: 100% !important;
  min-height: 400px !important;
}

/* Additional CSS to ensure scroll works */
.full-chat-area {
  overflow-y: scroll !important;
  overflow-x: hidden !important;
  scrollbar-width: 12px !important;
  scrollbar-color: #5b4df6 #0f172a !important;
  -webkit-overflow-scrolling: touch !important;
  scroll-behavior: smooth !important;
  overscroll-behavior: auto !important;
  touch-action: pan-y !important;
  max-height: calc(100vh - 200px) !important;
  height: 100% !important;
  min-height: 400px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 1.5rem !important;
  padding: 2rem 2rem 6rem 2rem !important;
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
  box-sizing: border-box !important;
  position: relative !important;
}

/* Ensure scrollbar is always visible */
.full-chat-area::-webkit-scrollbar,
#chat-html-history::-webkit-scrollbar,
.chat-content > div:first-child > div > div::-webkit-scrollbar {
  width: 12px !important;
  display: block !important;
  background: #0f172a !important;
}

.full-chat-area::-webkit-scrollbar-track,
#chat-html-history::-webkit-scrollbar-track,
.chat-content > div:first-child > div > div::-webkit-scrollbar-track {
  background: #0f172a !important;
  border-radius: 6px !important;
  border: 1px solid #334155 !important;
}

.full-chat-area::-webkit-scrollbar-thumb,
#chat-html-history::-webkit-scrollbar-thumb,
.chat-content > div:first-child > div > div::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #5b4df6, #3b82f6) !important;
  border-radius: 6px !important;
  border: 1px solid #334155 !important;
  min-height: 40px !important;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3) !important;
}

.full-chat-area::-webkit-scrollbar-thumb:hover,
#chat-html-history::-webkit-scrollbar-thumb:hover,
.chat-content > div:first-child > div > div::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #3b82f6, #2563eb) !important;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5) !important;
}

/* Custom scrollbar for chat area */
#chat-html-history::-webkit-scrollbar {
  width: 12px !important;
  display: block !important;
  background: #0f172a !important;
}

#chat-html-history::-webkit-scrollbar-track {
  background: #0f172a !important;
  border-radius: 6px !important;
  border: 1px solid #334155 !important;
}

#chat-html-history::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #5b4df6, #3b82f6) !important;
  border-radius: 6px !important;
  border: 1px solid #334155 !important;
  min-height: 40px !important;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3) !important;
}

#chat-html-history::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #3b82f6, #2563eb) !important;
  box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5) !important;
}

#chat-html-history::-webkit-scrollbar-corner {
  background: #0f172a !important;
}
.message {
  display: flex;
  margin-bottom: 1rem;
  animation: fadeIn 0.3s ease-in;
  padding: 0.5rem 0;
}
.message.user-message {
  justify-content: flex-end;
}
.message.bot-message {
  justify-content: flex-start;
}
.bubble {
  max-width: 70%;
  padding: 16px 20px;
  border-radius: 18px;
  font-family: 'Poppins', Arial, sans-serif;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  word-wrap: break-word;
  line-height: 1.6;
}
.message.user-message .bubble {
  background: linear-gradient(135deg, #5b4df6, #3b82f6);
  color: #fff;
  border-radius: 20px 20px 6px 20px;
  box-shadow: 0 4px 16px rgba(91, 77, 246, 0.3);
  border: 1px solid rgba(91, 77, 246, 0.2);
}
.message.bot-message .bubble {
  background: linear-gradient(135deg, #334155, #475569);
  color: #e5e7eb;
  border: 1px solid #475569;
  border-radius: 20px 20px 20px 6px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.message-content {
  font-family: 'Poppins', Arial, sans-serif !important;
  font-size: 1.1rem;
  line-height: 1.7;
  margin-bottom: 8px;
}
.message-meta {
  font-size: 0.85rem;
  opacity: 0.8;
  margin-top: 8px;
  font-family: 'Poppins', Arial, sans-serif;
}

/* Status Message Styles */
.status-message {
  padding: 0.8rem 1rem;
  border-radius: 0.8rem;
  font-size: 0.95rem;
  font-weight: 500;
  margin-top: 1rem;
  font-family: 'Poppins', Arial, sans-serif;
}
.status-message.error {
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
}
.status-message.success {
  background: #dcfce7;
  color: #16a34a;
  border: 1px solid #bbf7d0;
}
.full-input-area {
  width: 100%;
  background: linear-gradient(180deg, #1e293b 0%, #23283a 100%);
  border-top: 1px solid #334155;
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.15);
  padding: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-sizing: border-box;
  flex-shrink: 0;
  min-height: 160px;
  max-height: 160px;
  position: relative;
  z-index: 10;
  visibility: visible !important;
  opacity: 1 !important;
  margin-top: auto !important;
  overflow: hidden !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
}

.input-container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  visibility: visible !important;
  opacity: 1 !important;
}

.input-row {
  display: flex;
  align-items: center;
  gap: 16px;
  background: linear-gradient(135deg, #1e293b, #334155);
  border: 2px solid #475569;
  border-radius: 20px;
  padding: 16px 20px;
  transition: all 0.2s ease;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(10px);
  visibility: visible !important;
  opacity: 1 !important;
}

.input-row::before {
  display: none;
}

.input-row:focus-within::before {
  display: none;
}

.input-row:focus-within {
  border-color: #5b4df6;
  box-shadow: 0 0 0 3px rgba(91, 77, 246, 0.2), 0 4px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.input-row:hover {
  border-color: #64748b;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
  transform: translateY(-1px);
}

.full-input-field {
  flex: 1;
  border: none;
  outline: none;
  font-size: 1.1rem;
  font-family: 'Poppins', Arial, sans-serif;
  background: transparent;
  padding: 12px 16px;
  color: #f8fafc;
  transition: all 0.2s ease;
  line-height: 1.4;
  position: relative;
  z-index: 1;
  font-weight: 500;
  letter-spacing: 0.01em;
  visibility: visible !important;
  opacity: 1 !important;
}

.full-input-field:focus {
  border: none;
  box-shadow: none;
  color: #ffffff;
}

.full-input-field::placeholder {
  color: #94a3b8;
  font-family: 'Poppins', Arial, sans-serif;
  font-size: 1.1rem;
  font-weight: 400;
  opacity: 0.6;
  transition: opacity 0.2s ease;
  letter-spacing: 0.01em;
}

.full-input-field:focus::placeholder {
  opacity: 0.3;
}

.btn-send {
  background: transparent;
  color: #5b4df6;
  border: none;
  border-radius: 50%;
  font-size: 1.2rem;
  font-weight: 600;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'Poppins', Arial, sans-serif;
  min-width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: none;
  position: relative;
  overflow: hidden;
  visibility: visible !important;
  opacity: 1 !important;
}

.btn-send::before {
  display: none;
}

.btn-send:hover::before {
  display: none;
}

.btn-send:hover {
  background: rgba(91, 77, 246, 0.1);
  color: #3b82f6;
  transform: scale(1.1);
  box-shadow: 0 2px 8px rgba(91, 77, 246, 0.2);
}

.btn-send:active {
  transform: scale(0.9);
  box-shadow: none;
}

.btn-send.loading {
  animation: pulse 1.5s ease-in-out infinite;
  pointer-events: none;
}

.btn-send.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 20px;
  margin: -10px 0 0 -10px;
  border: 2px solid transparent;
  border-top: 2px solid #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.login-card {
  animation: fadeInUp 0.6s ease-out;
}

.status-message {
  animation: slideInRight 0.4s ease-out;
}

@media (max-width: 900px) {
  .main-app-layout {
    flex-direction: column;
    width: 100vw;
    height: 100vh;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
  }
  .navbar-chat {
    padding: 16px 20px;
    height: 64px;
    min-height: 64px;
    max-height: 64px;
  }
  .navbar-title {
    font-size: 1.6rem;
  }
  .model-dropdown {
    width: 180px;
    font-size: 0.9rem;
  }
  .main-content-row {
    flex-direction: column;
    height: calc(100vh - 64px);
    overflow: hidden;
  }
  
  .sidebar {
    width: 100%;
    min-width: 0;
    max-width: 100%;
    height: auto;
    border-radius: 0;
    border-right: none;
    border-bottom: 2px solid #334155;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    gap: 12px;
    overflow-x: auto;
    flex-shrink: 0;
    min-height: auto;
    max-height: none;
    min-height: 100px;
  }
  
  .chat-content {
    flex: 1;
    height: calc(100vh - 64px - 100px);
    overflow: hidden;
    max-height: calc(100vh - 64px - 100px);
  }
  .bubble {
    max-width: 92%;
    font-size: 1.1rem;
    padding: 16px 20px;
  }
  .full-chat-area {
    padding: 1.5rem 1.5rem 3rem 1.5rem;
    height: calc(100vh - 64px - 100px);
    overflow-y: auto !important;
    overflow-x: hidden !important;
    max-height: calc(100vh - 64px - 140px);
    scrollbar-width: 12px !important;
    scrollbar-color: #5b4df6 #0f172a !important;
    overscroll-behavior: auto !important;
    touch-action: pan-y !important;
    -webkit-overflow-scrolling: touch !important;
    scroll-behavior: smooth !important;
  }
  
  .full-chat-area::-webkit-scrollbar {
    width: 12px !important;
    display: block !important;
    background: #0f172a !important;
  }
  
  .full-chat-area::-webkit-scrollbar-track {
    background: #0f172a !important;
    border-radius: 6px !important;
    border: 1px solid #334155 !important;
  }
  
  .full-chat-area::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #5b4df6, #3b82f6) !important;
    border-radius: 6px !important;
    border: 1px solid #334155 !important;
    min-height: 40px !important;
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3) !important;
  }
  
  .full-chat-area::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #3b82f6, #2563eb) !important;
    box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.5) !important;
  }
  .full-input-area {
    padding: 24px 16px;
    min-height: 140px;
    max-height: 140px;
  }
  .input-container {
    max-width: 100%;
    padding: 0 5px;
  }
  .input-row {
    padding: 16px 20px;
    border-radius: 20px;
    gap: 16px;
  }
  .full-input-field {
    font-size: 1.1rem;
    padding: 12px 16px;
  }
  .btn-send {
    min-width: 40px;
    height: 40px;
    font-size: 1.1rem;
    padding: 12px;
  }
  
  .pdf-upload-section {
    padding: 16px;
    margin-top: 12px;
  }
  
  .pdf-upload-label {
    font-size: 1rem;
    margin-bottom: 12px;
  }
  .login-card { 
    max-width: 95vw; 
    padding: 2rem 1.5rem; 
    border-radius: 20px;
  }
  .login-form-dark { 
    padding: 0.8rem; 
    border-radius: 14px;
    gap: 0.5rem;
    max-height: 100%;
    overflow: hidden;
  }
  .login-title {
    font-size: 1.6rem;
    margin-bottom: 0.1rem;
  }
  .login-subtitle {
    font-size: 0.85rem;
    margin-bottom: 0.6rem;
  }
  .input-field {
    font-size: 1rem;
    padding: 0.9rem 1rem;
  }
  .btn-login, .btn-register {
    font-size: 1rem;
    padding: 0.9rem 1.2rem;
  }
  .btn-forgot {
    font-size: 0.9rem;
    padding: 0.7rem 1rem;
  }
}
/* LOGIN CARD MODERN */
.login-card {
  background: #fff;
  max-width: 410px;
  width: 100%;
  max-height: none !important;
  margin: 0 auto;
  padding: 2.2rem 1.8rem 1.8rem 1.8rem;
  border-radius: 2rem;
  box-shadow: 0 16px 64px 0 rgba(99,102,241,0.15), 0 2px 12px 0 rgba(0,0,0,0.10);
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: visible !important;
  box-sizing: border-box;
  transform: translateY(0);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  flex-shrink: 0;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  height: auto !important;
  min-height: auto !important;
}

.login-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #5b4df6, #3b82f6, #2563eb);
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 80px 0 rgba(99,102,241,0.25), 0 4px 20px 0 rgba(0,0,0,0.15);
}
.login-title {
  font-size: 2.2rem;
  font-weight: 800;
  color: #5b4df6;
  text-align: center;
  margin-bottom: 0.3rem;
  font-family: 'Poppins', Arial, sans-serif;
  letter-spacing: 0.01em;
}
.login-subtitle {
  font-size: 1.08rem;
  color: #8b8fa7;
  text-align: center;
  margin-bottom: 1.2rem;
  font-weight: 500;
  letter-spacing: 0.01em;
}
.input-label {
  display: inline-block;
  background: #5b4df6;
  color: #fff;
  font-size: 1rem;
  font-weight: 700;
  border-radius: 0.7rem;
  padding: 0.25rem 1.1rem 0.25rem 1.1rem;
  margin-bottom: 0.5rem;
  margin-top: 0.2rem;
  margin-left: 0.1rem;
  margin-right: 0.1rem;
  letter-spacing: 0.01em;
}
.input-field {
  width: 100%;
  border-radius: 1.1rem;
  border: 1.5px solid #23283a;
  padding: 15px 18px;
  font-size: 1.13rem;
  background: #31364a;
  color: #fff;
  margin-bottom: 1.2rem;
  transition: border 0.2s, box-shadow 0.2s;
  outline: none;
  box-shadow: 0 2px 8px #23283a33;
  font-family: 'Poppins', Arial, sans-serif;
}
.input-field:focus {
  border: 1.5px solid #5b4df6;
  background: #23283a;
  box-shadow: 0 0 0 4px #5b4df620;
}
.input-field::placeholder {
  color: #bfc6e6 !important;
  opacity: 1;
}
.login-btn-row {
  display: flex;
  gap: 1.1rem;
  width: 100%;
  margin-top: 0.5rem;
  margin-bottom: 0.2rem;
}
.btn-login {
  flex: 1;
  padding: 15px 0;
  font-size: 1.13rem;
  font-weight: 700;
  border: none;
  border-radius: 1.1rem;
  background: #5b4df6;
  color: #fff;
  cursor: pointer;
  box-shadow: 0 2px 12px #5b4df620;
  transition: background 0.2s, transform 0.15s, box-shadow 0.2s;
  font-family: 'Poppins', Arial, sans-serif;
}
.btn-login:hover, .btn-login:focus {
  background: #3b82f6;
  transform: translateY(-2px) scale(1.03);
  box-shadow: 0 8px 32px #3b82f640;
}
.btn-register {
  flex: 1;
  padding: 15px 0;
  font-size: 1.13rem;
  font-weight: 700;
  border: 2px solid #5b4df6;
  border-radius: 1.1rem;
  background: #fff;
  color: #5b4df6;
  cursor: pointer;
  box-shadow: 0 2px 12px #5b4df620;
  transition: background 0.2s, color 0.2s, border 0.2s;
  font-family: 'Poppins', Arial, sans-serif;
}
.btn-register:hover, .btn-register:focus {
  background: #f1f5ff;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}
.login-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.2rem;
  margin-bottom: 0.2rem;
  font-size: 0.98rem;
  width: 100%;
}
.login-link {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0 2px;
  border-radius: 4px;
  transition: background 0.2s, color 0.2s;
  font-family: 'Poppins', Arial, sans-serif;
}
.login-link:hover {
  background: #e0e7ff;
  color: #2563eb;
}
.status-message {
  font-size: 1rem;
  text-align: center;
  border-radius: 16px;
  padding: 1rem 1.2rem;
  margin-top: 0.8rem;
  margin-bottom: 0.8rem;
  background: linear-gradient(135deg, #f8fafc, #e2e8f0);
  color: #5b4df6;
  font-weight: 600;
  font-family: 'Poppins', Arial, sans-serif;
  box-shadow: 0 4px 16px rgba(91, 77, 246, 0.15);
  border: 2px solid rgba(91, 77, 246, 0.2);
  position: relative;
  overflow: hidden !important;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideInRight 0.4s ease-out;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
  max-height: none !important;
  height: auto !important;
}

.status-message::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #5b4df6, #3b82f6);
  border-radius: 2px 0 0 2px;
}

.status-message:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(91, 77, 246, 0.2);
}

.status-message.error:hover {
  box-shadow: 0 6px 20px rgba(220, 38, 38, 0.2);
}

.status-message.success:hover {
  box-shadow: 0 6px 20px rgba(22, 163, 74, 0.2);
}
.status-message.error {
  color: #dc2626;
  background: linear-gradient(135deg, #fef2f2, #fee2e2);
  border: 2px solid rgba(220, 38, 38, 0.3);
  box-shadow: 0 4px 16px rgba(220, 38, 38, 0.15);
  overflow: visible !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

.status-message.error::before {
  background: linear-gradient(180deg, #dc2626, #ef4444);
}

.status-message.success {
  color: #16a34a;
  background: linear-gradient(135deg, #f0fdf4, #dcfce7);
  border: 2px solid rgba(22, 163, 74, 0.3);
  box-shadow: 0 4px 16px rgba(22, 163, 74, 0.15);
  overflow: visible !important;
  overscroll-behavior: none !important;
  touch-action: none !important;
  -webkit-overflow-scrolling: touch !important;
}

.status-message.success::before {
  background: linear-gradient(180deg, #16a34a, #22c55e);
}
@media (max-width: 768px) {
  .login-bg { 
    padding: 8px; 
    overflow: visible !important;
    align-items: center;
    justify-content: center;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .login-card { 
    max-width: 95vw; 
    max-height: none !important;
    padding: 1.5rem 1rem; 
    border-radius: 20px;
    overflow: visible !important;
    margin: 0 auto;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .login-card:hover {
    transform: translateY(-3px);
  }
  .status-message {
    font-size: 0.95rem;
    padding: 0.9rem 1rem;
    margin-top: 0.6rem;
    margin-bottom: 0.6rem;
    gap: 0.4rem;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
    overflow: visible !important;
  }
  .login-form-dark { 
    padding: 1.2rem; 
    border-radius: 14px;
    overflow: visible !important;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .login-title {
    font-size: 1.8rem;
    margin-bottom: 0.3rem;
  }
  .login-subtitle {
    font-size: 0.95rem;
    margin-bottom: 1rem;
  }
  .input-field {
    font-size: 1rem;
    padding: 0.9rem 1rem;
  }
  .btn-login, .btn-register {
    font-size: 1rem;
    padding: 0.9rem 1.2rem;
  }
  .btn-forgot {
    font-size: 0.9rem;
    padding: 0.7rem 1rem;
  }
}

@media (max-width: 480px) {
  .login-bg { 
    padding: 5px; 
    overflow: visible !important;
    align-items: center;
    justify-content: center;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .login-card { 
    max-width: 98vw; 
    max-height: none !important;
    padding: 1rem 0.6rem; 
    border-radius: 16px;
    overflow: visible !important;
    margin: 0 auto;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
  }
  .login-card:hover {
    transform: translateY(-2px);
  }
  .status-message {
    font-size: 0.9rem;
    padding: 0.8rem 0.9rem;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    border-radius: 12px;
    gap: 0.3rem;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
    overflow: visible !important;
  }
  .login-form-dark { 
    padding: 1rem; 
    border-radius: 12px;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
    overflow: visible !important;
  }
  .login-title {
    font-size: 1.6rem;
    margin-bottom: 0.2rem;
  }
  .login-subtitle {
    font-size: 0.9rem;
    margin-bottom: 0.8rem;
  }
  .input-field {
    font-size: 0.95rem;
    padding: 0.8rem 0.9rem;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
    overflow: visible !important;
  }
  .btn-login, .btn-register {
    font-size: 0.95rem;
    padding: 0.8rem 1rem;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
    overflow: visible !important;
  }
  .btn-forgot {
    font-size: 0.85rem;
    padding: 0.6rem 0.8rem;
    overscroll-behavior: none !important;
    touch-action: none !important;
    -webkit-overflow-scrolling: touch !important;
    overflow: visible !important;
  }
  
  /* Input area responsive */
  .input-row {
    gap: 12px;
    padding: 12px 16px;
    border-radius: 20px;
  }
  
  .full-input-field {
    font-size: 1rem;
    padding: 10px 14px;
  }
  
  .full-input-field::placeholder {
    font-size: 1rem;
  }
  
  .btn-send {
    font-size: 1rem;
    padding: 10px;
    min-width: 40px;
    height: 40px;
  }
}

@media (max-width: 480px) {
  .sidebar {
    padding: 12px 16px;
    gap: 8px;
    min-height: 80px;
  }
  
  .chat-content {
    height: calc(100vh - 64px - 80px);
    max-height: calc(100vh - 64px - 80px);
  }
  
  .full-chat-area {
    padding: 1rem 1rem 2rem 1rem;
    height: calc(100vh - 64px - 80px);
    overflow-y: auto !important;
    overflow-x: hidden !important;
    max-height: calc(100vh - 64px - 120px);
    scrollbar-width: 12px !important;
    scrollbar-color: #5b4df6 #0f172a !important;
    overscroll-behavior: auto !important;
    touch-action: pan-y !important;
    -webkit-overflow-scrolling: touch !important;
    scroll-behavior: smooth !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 1.5rem !important;
  }
  
  .full-chat-area::-webkit-scrollbar {
    width: 8px !important;
    display: block !important;
  }
  
  .full-chat-area::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #5b4df6, #3b82f6) !important;
    border-radius: 4px !important;
    min-height: 30px !important;
  }
  
  .full-input-area {
    padding: 20px 12px;
    min-height: 120px;
    max-height: 120px;
  }
  
  .input-row {
    padding: 14px 18px;
    border-radius: 18px;
    gap: 14px;
  }
  
  .full-input-field {
    font-size: 1rem;
    padding: 10px 14px;
  }
  
  .full-input-field::placeholder {
    font-size: 1rem;
  }
  
  .btn-send {
    font-size: 1rem;
    padding: 8px;
    min-width: 36px;
    height: 36px;
  }
}

@media (max-width: 480px) {
  .input-row {
    gap: 12px;
    padding: 12px 16px;
    border-radius: 18px;
    margin: 0 2px;
  }
  
  .full-input-field {
    font-size: 1rem;
    padding: 10px 14px;
  }
  
  .full-input-field::placeholder {
    font-size: 1rem;
  }
  
  .btn-send {
    font-size: 1rem;
    padding: 10px;
    min-width: 38px;
    height: 38px;
  }
}
.help-settings-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px #e0e7ff33;
  padding: 2.2rem 2rem 1.5rem 2rem;
  max-width: 480px;
  margin: 2.5rem auto 0 auto;
  font-family: 'Poppins', Arial, sans-serif;
  color: #334155;
  border: 1.5px solid #e0e7ff;
}
.help-settings-title {
  font-size: 1.35rem;
  font-weight: 700;
  color: #3b82f6;
  margin-bottom: 1.1rem;
  letter-spacing: 0.01em;
  text-align: left;
}
.help-settings-list {
  list-style: none;
  padding: 0;
  margin: 0;
  margin-left: 0.2em;
}
.help-settings-list li {
  display: flex;
  align-items: flex-start;
  gap: 0.7em;
  margin-bottom: 1.1em;
  font-size: 1.08rem;
  position: relative;
  padding-left: 0.2em;
}
.help-settings-list .icon {
  color: #60a5fa;
  font-size: 1.25em;
  margin-top: 0.1em;
}
.pdf-upload-label {
  color: #5b4df6;
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 16px;
  font-family: 'Poppins', Arial, sans-serif;
  letter-spacing: 0.01em;
  position: relative;
  padding-left: 12px;
  margin-top: 20px;
}

.pdf-upload-label::before {
  content: '📄';
  margin-right: 10px;
  font-size: 1.2rem;
}

.pdf-upload-section {
  background: linear-gradient(135deg, #334155, #475569);
  border-radius: 16px;
  padding: 20px;
  margin-top: 16px;
  border: 2px solid #475569;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}
#pdf-upload { margin-bottom: 0.5rem; }
#upload-status { margin-bottom: 0.5rem; font-size: 0.98rem; }
.upload-icon {
  display: inline-block;
  vertical-align: middle;
  margin-right: 0.5em;
}
.upload-icon svg {
  width: 1.3em;
  height: 1.3em;
  fill: #a78bfa;
}
.main-content {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
  padding: 0;
}
"""

def create_login_ui():
    page_mode = gr.State("login")
    with gr.Column(elem_classes=["login-bg"], visible=True) as login_container:
        with gr.Column(elem_classes=["login-card"]):
            gr.HTML('<div class="login-title">ChatDil</div>')
            gr.HTML('<div class="login-subtitle">Asisten AI Pintar dengan Kemampuan RAG</div>')
            
            # Login Form
            with gr.Column(elem_classes=["login-form-dark"], visible=True) as login_form:
                gr.HTML('<label class="input-label" for="login-username-input">Username</label>')
                login_username = gr.Textbox(label="", show_label=False, placeholder="Username", elem_id="login-username-input", elem_classes=["input-field"])
                gr.HTML('<label class="input-label" for="login-password-input">Password</label>')
                login_password = gr.Textbox(label="", show_label=False, placeholder="Password", type="password", elem_id="login-password-input", elem_classes=["input-field"])
                with gr.Row(elem_classes=["login-btn-row"]):
                    login_btn = gr.Button("Login", elem_classes=["btn-login"])
                    register_btn = gr.Button("Register", elem_classes=["btn-register"])
                forgot_btn = gr.Button("Lupa Password?", elem_classes=["btn-forgot"])
                login_status = gr.HTML()
            
            # Register Form
            with gr.Column(elem_classes=["login-form-dark"], visible=False) as register_form:
                gr.HTML('<label class="input-label" for="reg-username-input">Username</label>')
                reg_username = gr.Textbox(label="", show_label=False, placeholder="Username", elem_id="reg-username-input", elem_classes=["input-field"])
                gr.HTML('<label class="input-label" for="reg-password-input">Password</label>')
                reg_password = gr.Textbox(label="", show_label=False, placeholder="Password", type="password", elem_id="reg-password-input", elem_classes=["input-field"])
                gr.HTML('<label class="input-label" for="reg-password2-input">Konfirmasi Password</label>')
                reg_password2 = gr.Textbox(label="", show_label=False, placeholder="Konfirmasi Password", type="password", elem_id="reg-password2-input", elem_classes=["input-field"])
                with gr.Row(elem_classes=["login-btn-row"]):
                    reg_btn = gr.Button("Daftar", elem_classes=["btn-login"])
                    reg_login_btn = gr.Button("Kembali ke Login", elem_classes=["btn-register"])
                register_status = gr.HTML()
            
            # Forgot Password Form
            with gr.Column(elem_classes=["login-form-dark"], visible=False) as forgot_form:
                gr.HTML('<label class="input-label" for="forgot-username-input">Username</label>')
                forgot_username = gr.Textbox(label="", show_label=False, placeholder="Username", elem_id="forgot-username-input", elem_classes=["input-field"])
                with gr.Row(elem_classes=["login-btn-row"]):
                    forgot_send_btn = gr.Button("Kirim Reset", elem_classes=["btn-login"])
                    forgot_login_btn = gr.Button("Kembali ke Login", elem_classes=["btn-register"])
                forgot_status = gr.HTML()
    
    return (
        login_container, 
        login_form, register_form, forgot_form,
        login_username, login_password, login_btn, register_btn, forgot_btn, login_status,
        reg_username, reg_password, reg_password2, reg_btn, reg_login_btn, register_status,
        forgot_username, forgot_send_btn, forgot_login_btn, forgot_status,
        page_mode
    )

def create_main_ui():
    models = get_models()
    with gr.Column(elem_classes=["main-app-layout"], visible=False) as main_container:
        with gr.Row(elem_classes=["navbar-chat"]):
            gr.HTML('<div class="navbar-title">ChatDil</div>')
            model_dropdown = gr.Dropdown(label="", show_label=False, choices=models, value=models[0] if models else "", elem_id="model-dropdown", elem_classes=["model-dropdown"])
        with gr.Row(elem_classes=["main-content-row"]):
            with gr.Column(elem_classes=["sidebar"]):
                gr.HTML('<div class="sidebar-title">Menu</div>')
                new_chat_btn = gr.Button("+ New Chat", elem_classes=["menu-item"])
                chat_btn = gr.Button("Chat", elem_classes=["menu-item active"])
                gr.HTML('<div class="model-settings-title">Model Settings</div>')
                model_status = gr.Markdown("", elem_id="model-status-md")
                refresh_btn = gr.Button("Refresh Models", elem_classes=["btn-refresh"])
                rag_toggle = gr.Checkbox(label="Aktifkan RAG Mode", value=True, elem_id="rag-toggle", elem_classes=["btn-rag"])
                rag_status = gr.Markdown("<span id='rag-status'>RAG: Aktif</span>", elem_id="rag-status-md")
                export_btn = gr.Button("Export Chat", elem_classes=["btn-export"])
                # Upload PDF di sidebar
                gr.HTML('<span class="pdf-upload-label">Upload PDF untuk RAG</span>')
                pdf_upload = gr.File(label="", show_label=False, file_types=[".pdf"], file_count="single", elem_id="pdf-upload")
                upload_btn = gr.Button("Proses PDF", elem_classes=["btn-upload"])
                upload_status = gr.Markdown(elem_id="upload-status")
            with gr.Column(elem_classes=["chat-content"]):
                chat_html = gr.HTML("""
                    <div class='full-chat-area' id='chat-html-history'>
                        <script>
                            // Auto-scroll to bottom when content changes
                            const chatArea = document.getElementById('chat-html-history');
                            if (chatArea) {
                                // Force enable scroll ONLY for chat area
                                chatArea.style.overflowY = 'scroll';
                                chatArea.style.overflowX = 'hidden';
                                chatArea.style.scrollBehavior = 'smooth';
                                chatArea.style.webkitOverflowScrolling = 'touch';
                                chatArea.style.maxHeight = 'calc(100vh - 200px)';
                                chatArea.style.height = '100%';
                                chatArea.style.minHeight = '400px';
                                chatArea.style.display = 'flex';
                                chatArea.style.flexDirection = 'column';
                                chatArea.style.gap = '1.5rem';
                                chatArea.style.padding = '2rem 2rem 6rem 2rem';
                                chatArea.style.background = 'linear-gradient(180deg, #0f172a 0%, #1e293b 100%)';
                                chatArea.style.boxSizing = 'border-box';
                                chatArea.style.position = 'relative';
                                chatArea.style.overscrollBehavior = 'auto';
                                chatArea.style.touchAction = 'pan-y';
                                
                                // Custom scrollbar styles
                                chatArea.style.scrollbarWidth = '12px';
                                chatArea.style.scrollbarColor = '#5b4df6 #0f172a';
                                
                                // Prevent scroll on parent elements
                                const parentElements = chatArea.parentElement;
                                if (parentElements) {
                                    parentElements.style.overflow = 'hidden';
                                    parentElements.style.overscrollBehavior = 'none';
                                    parentElements.style.touchAction = 'none';
                                }
                                
                                // Prevent scroll on all parent containers
                                let currentParent = chatArea.parentElement;
                                while (currentParent) {
                                    if (currentParent !== chatArea) {
                                        currentParent.style.overflow = 'hidden';
                                        currentParent.style.overscrollBehavior = 'none';
                                        currentParent.style.touchAction = 'none';
                                    }
                                    currentParent = currentParent.parentElement;
                                }
                                
                                const observer = new MutationObserver(function() {
                                    setTimeout(() => {
                                        chatArea.scrollTop = chatArea.scrollHeight;
                                    }, 100);
                                });
                                observer.observe(chatArea, { childList: true, subtree: true });
                                
                                // Also scroll on window resize
                                window.addEventListener('resize', function() {
                                    setTimeout(() => {
                                        chatArea.scrollTop = chatArea.scrollHeight;
                                    }, 100);
                                });
                                
                                // Force scroll to bottom on load
                                setTimeout(() => {
                                    chatArea.scrollTop = chatArea.scrollHeight;
                                }, 500);
                                
                                // Prevent scroll on document body
                                document.body.style.overflow = 'hidden';
                                document.body.style.overscrollBehavior = 'none';
                                document.body.style.touchAction = 'none';
                                
                                // Ensure scroll works by forcing a reflow
                                chatArea.offsetHeight;
                            }
                        </script>
                    </div>
                """)
                with gr.Row(elem_classes=["full-input-area"]):
                    with gr.Column(elem_classes=["input-container"]):
                        with gr.Row(elem_classes=["input-row"]):
                            msg = gr.Textbox(label="", show_label=False, placeholder="Ketik pertanyaan Anda di sini...", elem_id="chat-input", elem_classes=["full-input-field"])
                            send_btn = gr.Button("➤", elem_classes=["btn-send"], elem_id="send-btn")
                download_pdf = gr.File(visible=False)
                status = gr.Markdown()
    return (
        main_container,
        model_dropdown,
        model_status,
        chat_html,
        msg,
        rag_toggle,
        rag_status,
        export_btn,
        chat_btn,
        refresh_btn,
        pdf_upload,
        upload_btn,
        upload_status,
        download_pdf,
        status,
        new_chat_btn,
        send_btn
    )

def build_ui():
    with gr.Blocks(
        title="ChatDil",
        theme=gr.themes.Soft(
            primary_hue="indigo",
            secondary_hue="gray",
            neutral_hue="slate"
        ),
        css=CSS
    ) as app:
        # States
        login_state = gr.State(False)
        username_state = gr.State("")
        model_state = gr.State("")
        rag_state = gr.State(False)
        chat_html_history = gr.State("")
        chat_history = gr.State([])  # Tambahkan state list Q&A
        menu_state = gr.State("chat")
        page_mode = gr.State("login")

        # Create UI components
        (login_container, login_form, register_form, forgot_form, login_username, login_password, login_btn, register_btn, forgot_btn, login_status, reg_username, reg_password, reg_password2, reg_btn, reg_login_btn, register_status, forgot_username, forgot_send_btn, forgot_login_btn, forgot_status, page_mode) = create_login_ui()
        
        (main_container, model_dropdown, model_status, chat_html, msg, rag_toggle, rag_status, export_btn, chat_btn, refresh_btn, pdf_upload, upload_btn, upload_status, download_pdf, status, new_chat_btn, send_btn) = create_main_ui()

        # Awal: hanya login_form yang visible
        # main_container.visible = False # This line is removed as per new_code

        # Fungsi untuk switch antar form
        def switch_form(mode):
            if mode == "login":
                return (
                    gr.update(visible=True),
                    gr.update(visible=False),
                    gr.update(visible=False)
                )
            elif mode == "register":
                return (
                    gr.update(visible=False),
                    gr.update(visible=True),
                    gr.update(visible=False)
                )
            elif mode == "forgot":
                return (
                    gr.update(visible=False),
                    gr.update(visible=False),
                    gr.update(visible=True)
                )
            return (
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False)
            )

        # Event handler untuk switch form
        register_btn.click(
            lambda: switch_form("register"),
            outputs=[login_form, register_form, forgot_form]
        )
        reg_login_btn.click(
            lambda: switch_form("login"),
            outputs=[login_form, register_form, forgot_form]
        )
        forgot_btn.click(
            lambda: switch_form("forgot"),
            outputs=[login_form, register_form, forgot_form]
        )
        forgot_login_btn.click(
            lambda: switch_form("login"),
            outputs=[login_form, register_form, forgot_form]
        )

        # Validasi register
        def register_validate(username, pw1, pw2):
            if not username or not pw1 or not pw2:
                return '<div class="status-message error">Semua field wajib diisi.</div>'
            if len(username) < 3:
                return '<div class="status-message error">Username minimal 3 karakter.</div>'
            if len(pw1) < 6:
                return '<div class="status-message error">Password minimal 6 karakter.</div>'
            if pw1 != pw2:
                return '<div class="status-message error">Password tidak cocok.</div>'
            msg, status = register(username, pw1)
            if status == "success":
                return f'<div class="status-message success">{msg}</div>'
            return f'<div class="status-message error">{msg}</div>'
        
        reg_btn.click(register_validate, [reg_username, reg_password, reg_password2], register_status)

        # Validasi forgot password - reset password menjadi 1234
        def forgot_validate(username):
            if not username:
                return '<div class="status-message error">Masukkan username</div>'
            
            message, status = reset_password(username)
            if status == "success":
                return f'<div class="status-message success">{message}</div>'
            else:
                return f'<div class="status-message error">{message}</div>'
        
        forgot_send_btn.click(forgot_validate, [forgot_username], forgot_status)

        # Handler login tetap
        def login_with_validation(username, password):
            if not username or not password:
                return (
                    gr.update(visible=False),
                    gr.update(visible=True),
                    False,
                    "",
                    '<span class="status-message error">Username atau password yang anda masukkan salah. Silahkan coba lagi.</span>'
                )
            result = login(username, password)
            if result[1]:  # login berhasil
                return (
                    gr.update(visible=True),
                    gr.update(visible=False),
                    result[2],
                    result[3],
                    result[4]
                )
            else:  # login gagal
                return (
                    gr.update(visible=False),
                    gr.update(visible=True),
                    result[2],
                    result[3],
                    result[4]
                )
        login_btn.click(
            login_with_validation,
            [login_username, login_password],
            [main_container, login_container, login_state, username_state, login_status]
        )

        # Handler untuk new chat
        def new_chat():
            return "", []
        
        new_chat_btn.click(new_chat, outputs=[chat_html, chat_history])
        
        # Highlight menu item saat new chat
        def highlight_new_chat():
            return gr.Button.update(elem_classes=["menu-item active"]), gr.Button.update(elem_classes=["menu-item"])
        
        new_chat_btn.click(highlight_new_chat, outputs=[new_chat_btn, chat_btn])

        # Handler untuk respond dan update history
        def respond_and_update_history(message, chat_html_history, rag_toggle, login_state, username_state, chat_history):
            # Panggil respond asli dengan parameter yang benar
            _, html_history, _ = respond(message, chat_html_history, rag_toggle, login_state, username_state)
            
            # Hanya update HTML history, tidak simpan ke chat_history
            return html_history
        
        msg.submit(
            respond_and_update_history,
            [msg, chat_html, rag_toggle, login_state, username_state, chat_history],
            [chat_html]
        ).then(
            lambda: "",
            None,
            [msg]
        )
        
        send_btn.click(
            respond_and_update_history,
            [msg, chat_html, rag_toggle, login_state, username_state, chat_history],
            [chat_html]
        ).then(
            lambda: "",
            None,
            [msg]
        )

        # Event handler untuk model dropdown
        model_dropdown.change(
            update_model,
            model_dropdown,
            status
        )

        # Event handler upload PDF
        upload_btn.click(
            process_pdf,
            pdf_upload,
            upload_status
        )

        # Event handler update status RAG
        def update_rag_status(is_active):
            return f"<span id='rag-status'>RAG: {'Aktif' if is_active else 'Nonaktif'}</span>"
        rag_toggle.change(update_rag_status, rag_toggle, rag_status)

        # Event handler update model status
        def update_model_status(model_name):
            return f"<span style='color:#5b4df6;font-weight:600;'>Model diganti ke: <b>{model_name}</b></span>"
        model_dropdown.change(update_model_status, model_dropdown, model_status)

        # Event handler refresh models
        refresh_btn.click(refresh_models, outputs=[model_dropdown, model_status])

        # Event handler export chat
        export_btn.click(
            export_chat_from_html,
            [chat_html, username_state],
            [download_pdf, status]
        )

        # Handler untuk clear chat
        def clear_chat_history():
            return "", []
        
        # clear_btn.click(clear_chat_history, outputs=[chat_html, chat_history]) # Removed as per new_code

        # Handler untuk respond dan update history

    return app