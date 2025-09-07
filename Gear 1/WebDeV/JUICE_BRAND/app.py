from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        user_name = request.form.get("name")
        user_email = request.form.get("email")

        print(user_name)
        print(user_email)

        # Pass as query parameters
        return redirect(url_for("bio", user=user_name, email=user_email))
    return render_template("text.html")

@app.route("/bio")
def bio():
    user = request.args.get("user")
    email = request.args.get("email")
    return render_template("red.html", user=user, email=email)

if __name__ == "__main__":
    app.run(debug=True)
