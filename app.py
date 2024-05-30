from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # print(type(user_message))
    user_message_list = []
    user_message_list.append(user_message)
    # print(type(user_message_list))
    
    subprocess.run(["torchrun", "--nproc_per_node=1",
                    "/home/pcs4090/LLaMA/llama3/call_llama.py",
                    "--queries {}".format(user_message_list)])
    
    bot_response = "This is a bot response to: " + user_message
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100, debug=True)
