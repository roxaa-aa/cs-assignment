from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

SECRET_PIN = "679"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Secure Portal Login</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f0f2f5; margin: 0; }
        .card { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 300px; text-align: center; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; text-align: center; }
        button { width: 98%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        .msg { margin-top: 15px; font-weight: bold; }
        .error { color: #dc3545; }
        .success { color: #28a745; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Enter 3-Digit PIN</h2>
        <form method="POST" action="/login">
            <input type="password" name="pin" maxlength="3" placeholder="***" required />
            <button type="submit">Unlock</button>
        </form>
        {% if message %}
            <div class="msg {{ status }}">{{ message }}</div>
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/login", methods=["POST"])
def login():
    # Handle both JSON payloads and standard form submissions
    if request.is_json:
        data = request.get_json()
        pin = str(data.get("pin", ""))
    else:
        pin = str(request.form.get("pin", ""))

    if pin == SECRET_PIN:
        if request.is_json:
            return jsonify({"status": "success", "message": "Access Granted"}), 200
        return (
            render_template_string(
                HTML_TEMPLATE, message="Access Granted!", status="success"
            ),
            200,
        )
    else:
        if request.is_json:
            return jsonify({"status": "error", "message": "Access Denied"}), 401
        return (
            render_template_string(
                HTML_TEMPLATE, message="Invalid PIN", status="error"
            ),
            401,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
