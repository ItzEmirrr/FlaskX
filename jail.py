from flask import Flask


server = Flask(__name__)





@server.route('/')
def render_dash():
    return "Hello World"



if __name__ == '__main__':
    server.run(debug=True)

