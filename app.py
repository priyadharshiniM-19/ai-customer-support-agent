from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from werkzeug.security import generate_password_hash, check_password_hash

from database import (
    init_db,
    create_user,
    get_user_by_email,
    save_chat,
    get_chat_history
)

from ai import get_ai_response

app = Flask(__name__)

app.secret_key = "super-secret-key-change-this"

init_db()


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("chat"))

    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = get_user_by_email(email)

        if existing_user:
            return render_template(
                "register.html",
                error="Email already exists"
            )

        password_hash = generate_password_hash(password)

        create_user(
            username,
            email,
            password_hash
        )

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)

        if user and check_password_hash(
            user["password_hash"],
            password
        ):
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect(url_for("chat"))

        return render_template(
            "login.html",
            error="Invalid credentials"
        )

    return render_template("login.html")


@app.route("/chat")
def chat():

    if "user_id" not in session:
        return redirect(url_for("login"))

    chats = get_chat_history(
        session["user_id"]
    )

    return render_template(
        "chat.html",
        username=session["username"],
        chats=chats
    )


@app.route("/ask", methods=["POST"])
def ask():

    if "user_id" not in session:
        return jsonify(
            {"error": "Unauthorized"}
        ), 401

    question = request.json["question"]

    answer = get_ai_response(question)

    save_chat(
        session["user_id"],
        question,
        answer
    )

    return jsonify(
        {
            "answer": answer
        }
    )


@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


if __name__ == "__main__":
    app.run(debug=True)