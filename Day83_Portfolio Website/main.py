from flask import Flask, render_template

app = Flask(__name__)


@app.route("/home")
def home_page():
    return "<p>Hi</p>"

@app.route("/highlights")
def highlights():
    return "<p>Hi</p>"

@app.route("/resume")
def resume():
    return "<p>Hi</p>"

@app.route("/cad-portfolio")
def portfolio():
    return "<p>Hi</p>"

@app.route("/projects")
def projects():
    return "<p>Hi</p>"

@app.route("/contact-page")
def contact():
    return "<p>Hi</p>"


if __name__ == "__main__":
    app.run(debug=True)