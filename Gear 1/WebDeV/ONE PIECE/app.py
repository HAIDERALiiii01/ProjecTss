from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/crew")
def crew():
    return render_template("crew.html")
   
if __name__ == "__main__":
    app.run(debug=True)

    # templates\crew.html