from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome page</p>"

@app.route("/login")
def login():
    # return render_template('login.html')
    return "This is the login page"

if __name__ == '__main__':
    app.run(debug=True)