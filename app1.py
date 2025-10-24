from flask import Flask, request, jsonify, render_template, send_file
from chatbot_backend import chat_with_yesu_mitra, run_cli
import os
import threading

app = Flask(__name__)

# Directory for storing temporary TTS files
TTS_DIR = "tts_audio"
if not os.path.exists(TTS_DIR):
    os.makedirs(TTS_DIR)

# --- Web Interface Route ---

@app.route('/')
def index():
    """Serves the main web interface (HTML/CSS/JS)."""
    return render_template('index.html')

# --- Chat API Endpoint ---

@app.route('/chat', methods=['POST'])
def chat():
    """Handles the chat request, processes it through the backend, and returns the response."""
    data = request.get_json()
    user_query = data.get('query', '')

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # The backend function handles RAG, LLM call, and TTS generation
    result = chat_with_yesu_mitra(user_query)

    # The TTS audio file is saved locally by the backend.
    # We will serve it via a separate endpoint.
    audio_filename = os.path.basename(result["audio_path"]) if result["audio_path"] else None
    audio_url = f"/tts/{audio_filename}" if audio_filename else None

    # Clean up the old TTS file after sending the new one
    # This is a simple cleanup mechanism for a single-user sandbox environment
    for filename in os.listdir(TTS_DIR):
        if filename != audio_filename:
            os.remove(os.path.join(TTS_DIR, filename))

    return jsonify({
        "response": result["response"],
        "audio_url": audio_url
    })

# --- TTS Audio Endpoint ---

@app.route('/tts/<filename>')
def serve_tts_audio(filename):
    """Serves the generated TTS audio file."""
    try:
        return send_file(filename, mimetype='audio/mp3')
    except FileNotFoundError:
        return jsonify({"error": "Audio file not found"}), 404

# --- Helper to run CLI in a separate thread (for demonstration) ---
# This is mainly for the user to see the CLI option is available,
# but the web app will be the main focus.
def start_cli_in_thread():
    """Starts the CLI in a separate thread."""
    print("\n--- Starting CLI in a separate thread (for user reference) ---")
    run_cli()

if __name__ == '__main__':
    # We need to ensure the TTS output from the backend goes to the correct directory
    # by updating the path in the backend before running.
    import chatbot_backend
    chatbot_backend.TTS_OUTPUT_PATH = os.path.join(TTS_DIR, "latest_response.mp3")

    # Start the Flask server
    # We will use the `expose` tool to get a public URL
    print("Starting Yesu Mitra Web Server...")
    app.run(host='0.0.0.0', port=5000, debug=False)

    # Note: The CLI part is commented out for now as the server will block the thread.
    # If the user wants to run the CLI, they can execute 'python3.11 chatbot_backend.py'
    # directly in a separate terminal session.

