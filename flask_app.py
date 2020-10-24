from flask import Flask, escape, request, render_template

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def hello():
    # name = request.args.get("name", "World")
    return render_template("main.html")
