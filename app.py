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
    data = pickle.dumps(retrieved_message)
    client_socket.send(data)
    
    response = client_socket.recv(4096)
    result = pickle.loads(response)
    # print(result)
    
    bot_response = "This is a bot response to: \n{}\n".format(user_message)
    # time.sleep(8)
    bot_response = bot_response + "\n" + result['generation']
    
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100, debug=True)
