from flask import Flask, render_template, request, jsonify

import os
import time
import socket
import pickle

from rag import retrieve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # print(type(user_message))
    
    retrieved_message = retrieve(user_message)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8101))
    
    data = pickle.dumps(user_message)
    client_socket.send(data)
    
    response = client_socket.recv(4096)
    result = pickle.loads(response)
    # print(result)
    
    bot_response = "This is a generated text without RAG: \n\n"
    # time.sleep(8)
    bot_response = bot_response + result['generation']
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8101))
    
    data = pickle.dumps(retrieved_message)
    client_socket.send(data)
    
    response = client_socket.recv(4096)
    result = pickle.loads(response)
    # print(result)
    
    retrieved_result = retrieved_message.replace(user_message, "")
    
    bot_response = bot_response + "\n\n" + "This is a generated text with RAG :\n\n"
    # time.sleep(8)
    bot_response = bot_response + retrieved_result + result['generation']
    
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(host='140.113.110.15', port=8100, debug=True)
