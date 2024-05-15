import markdown
from flask import Flask, jsonify, request, abort, send_file, send_from_directory
import requests
import google.generativeai as palm

app = Flask(__name__)
palm.configure(api_key='AIzaSyDGbqD3xfW-MW4fETNbdp3BU5sfW-xUm4E')
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    prompt = f"{payload}"
    completion = palm.generate_text(model="models/text-bison-001" , prompt=prompt , temperature=0 ,max_output_tokens=800 , )
    return completion.result

@app.route('/')
def home():
    return send_file('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('./static/', filename)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        abort(400, description="Prompt is required")

    try:
        output = query(prompt)
        # Assuming the response format from Hugging Face is as follows:
        # {"generated_text": "response text"}
        generated_text = output if output else "Sorry, something went wrong. Please try again."
        return jsonify({"response": generated_text})
    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(debug=True)
