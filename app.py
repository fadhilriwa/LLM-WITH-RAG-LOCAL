from ui import build_ui
import gradio as gr
from logic import *

if __name__ == "__main__":
    app = build_ui()

    app.launch(
        server_port=8080,
        server_name="127.0.0.1",
        inbrowser=True,
        debug=True
    )
