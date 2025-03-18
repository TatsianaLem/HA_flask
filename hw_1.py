from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def get_hello():
    return f"Hello, Flask!"

@app.route('/user/', defaults={"name":"alice"})
@app.route('/user/<string:name>')
def get_user(name):
    return f"Hello, {name}"

if __name__ == '__main__':
    app.run(debug=True)