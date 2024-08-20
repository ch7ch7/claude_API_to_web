from flask import Flask, request, jsonify, render_template
import requests
import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

logging.basicConfig(level=logging.DEBUG)

@app.route('/api/ask-claude', methods=['POST'])
def ask_claude():
    question = request.json['question']
    
    headers = {
        "Content-Type": "application/json",
        "x-api-key": os.getenv('CLAUDE_API_KEY'),
        "anthropic-version": "2023-06-01"  # 添加 API 版本頭
    }
    
    data = {
        "model": "claude-3-sonnet-20240229",
        "messages": [{"role": "user", "content": question}],
        "max_tokens": 1000
    }
    
    try:
        response = requests.post('https://api.anthropic.com/v1/messages', json=data, headers=headers)
        response.raise_for_status()
        return jsonify({"answer": response.json()['content'][0]['text']})
    except requests.exceptions.RequestException as e:
        logging.error(f"API 請求錯誤: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logging.error(f"API 錯誤響應內容: {e.response.text}")
        return jsonify({"error": "處理您的請求時發生錯誤"}), 500

def check_api_key():
       if not os.getenv('CLAUDE_API_KEY'):
           print("錯誤：CLAUDE_API_KEY 未設置。請確保在 .env 文件中設置了正確的 API 密鑰。")
           sys.exit(1)

if __name__ == '__main__':
    check_api_key()
    app.run(debug=True)