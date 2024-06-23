from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from pypdf import PdfReader
from gem import summarize_resume, model, getChatHistory

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

userChatHistory = {}

startChatTemplate = [
    {'role': 'user', 'parts': [
        'The following is a resume of mine and I would like to chat with you about it. \ncontent:\n']},
    {'role': 'model', 'parts': [
        'Sure, I\'d be happy to chat with you about it. What would you like to talk about?']}
]


@app.route('/')
def index():
    return jsonify({"message": "Hello World!"})


@app.route("/api/uploadPDF", methods=['POST'])
def uploadPDF():
    files = request.files
    uid = request.form['uid']
    print(files)

    if files:
        file = files['file']
        file.save(f"uploads/{file.filename}")

        # read the pdf file
        pdf = PdfReader(f"uploads/{file.filename}")
        page_count = len(pdf.pages)

        content = ""
        for i in range(page_count):
            page = pdf.pages[i]
            content += page.extract_text()

        print(content)

        os.remove(f"uploads/{file.filename}")

        return jsonify({"content": content})

    else:
        return jsonify({"message": "nofile"})


@app.route("/api/summarize", methods=['POST'])
def summarize():
    content = request.json['content']

    return jsonify({"summary": summarize_resume(content)})


@app.route("/api/chat", methods=['POST'])
def chat():
    uid = request.json['uid']
    message = request.json['message']
    response = userChatHistory[uid].send_message(message)
    return getChatHistory(userChatHistory[uid])


@app.route("/api/startChat", methods=['POST'])
def startChat():
    print("starting Chat")
    uid = request.json['uid']
    resume = request.json['resume']
    chatTemp = [{
        'role': 'user',
        'parts':
        [
            'The following is a resume of mine and I would like to chat with you about it. (Note: if user has not uploaded the resume and asks about it, you must tell the user that they have not uploaded a resume so you can\'t answer that.) \ncontent:\n'
        ]},
        {'role': 'model', 'parts': ['Sure, I\'d be happy to chat with you about it. What would you like to talk about?']}]
    chatTemp[0]['parts'][0] += resume
    userChatHistory[uid] = model.start_chat(history=chatTemp)
    return getChatHistory(userChatHistory[uid])


@app.route("/api/getChatHistory", methods=['POST'])
def sendChatHistory():
    uid = request.json['uid']
    if uid in userChatHistory:
        return getChatHistory(userChatHistory[uid])
    else:
        return []


@app.route("/api/clearChat", methods=['POST'])
def clearChatHistory():
    uid = request.json['uid']
    userChatHistory[uid] = model.start_chat()
    return jsonify({"message": "Chat history cleared"})


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
