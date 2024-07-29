from flask import Flask, request, jsonify
from flask_cors import CORS
import torch
from transformers import BartTokenizer, BartForConditionalGeneration, T5Tokenizer, T5ForConditionalGeneration

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

tokenizer_b = BartTokenizer.from_pretrained(r"C:\Users\JAYSA\Downloads\QA\qa-webapp\backend\bart_results\checkpoint-25000")
model_b = BartForConditionalGeneration.from_pretrained(r"C:\Users\JAYSA\Downloads\QA\qa-webapp\backend\bart_results\checkpoint-25000")

tokenizer_t = T5Tokenizer.from_pretrained(r"C:\Users\JAYSA\Downloads\QA\qa-webapp\backend\t5_results\checkpoint-15000")
model_t = T5ForConditionalGeneration.from_pretrained(r"C:\Users\JAYSA\Downloads\QA\qa-webapp\backend\t5_results\checkpoint-15000")

@app.route('/generate', methods=['POST'])
def generate():
    print("Received request")  # Debugging log
    data = request.get_json()
    print(f"Request data: {data}")  # Debugging log
    question = data['question']
    inputs = tokenizer_b.encode("question: " + question, return_tensors="pt")
    outputs = model_b.generate(inputs, max_new_tokens=150)  # Adjust max_new_tokens as needed
    answer = tokenizer_b.decode(outputs[0], skip_special_tokens=True)  # Use skip_special_tokens=True

    inputs_t = tokenizer_t.encode("question: " + question, return_tensors="pt")
    outputs_t = model_t.generate(inputs_t, max_new_tokens=150)  # Adjust max_new_tokens as needed
    answer_t = tokenizer_t.decode(outputs_t[0], skip_special_tokens=True)  # Use skip_special_tokens=True

    print(f"Generated answer 1: {answer} \n\nGenerated answer2: {answer_t}")  # Debugging log
    return jsonify([{'answer1': answer}, {'answer2':answer_t}])


if __name__ == '__main__':
    app.run(debug=False)
