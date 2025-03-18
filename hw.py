from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/homepage')
def home_page():
    return 'Hello, homepage!'

@app.route('/homepage/post', methods=['POST'])
def post():
    requests_json = request.json
    name = requests_json['user_name']
    return f"Hello, {name}!"

@app.route('/homepage/postform', methods=['POST'])
def postform():
    name = request.form['user_name']
    age = request.form['age']
    return f"Hello, {name}, you age is {age}!"



if __name__ == '__main__':
    app.run(debug=True)