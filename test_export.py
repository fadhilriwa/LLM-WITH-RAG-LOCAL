#!/usr/bin/env python3
"""
Test script untuk fungsi ekspor PDF
"""

from logic import export_chat_from_html

# Test HTML dengan chat history
test_html = '''
<div class="message user-message">
    <div class="message-label">Anda</div>
    <div class="message-content">Apa itu RAG?</div>
    <div class="message-meta">10:00</div>
</div>
<div class="message bot-message">
    <div class="message-label">Bot</div>
    <div class="message-content">RAG adalah Retrieval-Augmented Generation, teknik yang menggabungkan retrieval dan generation untuk menghasilkan jawaban yang lebih akurat.</div>
    <div class="message-meta">10:01</div>
</div>
<div class="message user-message">
    <div class="message-label">Anda</div>
    <div class="message-content">Bagaimana cara kerjanya?</div>
    <div class="message-meta">10:02</div>
</div>
<div class="message bot-message">
    <div class="message-label">Bot</div>
    <div class="message-content">RAG bekerja dengan mengambil informasi relevan dari database, kemudian menggunakan informasi tersebut untuk menghasilkan jawaban yang lebih kontekstual.</div>
    <div class="message-meta">10:03</div>
</div>
'''

print("Testing export function...")
result = export_chat_from_html(test_html, "testuser")
print(f"Result: {result}") 