from flask import Flask, render_template, request, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    # print(type(user_message))
    
    # read_user_message(user_message=user_message)
    
    response = os.popen("torchrun --nproc_per_node 1 \
             /home/pcs4090/LLaMA/llama3/call_llama.py \
             --ckpt_dir /home/pcs4090/LLaMA/llama3/Meta-Llama-3-8B \
             --tokenizer_path /home/pcs4090/LLaMA/llama3/Meta-Llama-3-8B/tokenizer.model \
             --query '{}'".format(user_message)).read()
    
    response = response.split("Answer =")[-1].split("===")[0]
    
    bot_response = "This is a bot response to: \n{}\n".format(user_message)
    time.sleep(8)
    bot_response = bot_response + "\n" + response
    
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100, debug=True)
    
