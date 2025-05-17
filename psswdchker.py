from flask import Flask, request, render_template_string, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Password Complexity Checker</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f5f7fa;
        }
        .card {
            margin-top: 80px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .strength {
            margin-top: 10px;
        }
        .valid {
            color: green;
        }
        .invalid {
            color: red;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card p-4">
                    <h3 class="text-center mb-4">🔐 Password Complexity Checker</h3>
                    <form method="POST" novalidate>
                        <div class="mb-3">
                            <label class="form-label">Username:</label>
                            <input type="text" name="username" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Password:</label>
                            <input type="password" id="password" name="password" class="form-control" required>
                            <div id="feedback" class="form-text strength"></div>
                        </div>
                        <button type="submit" class="btn btn-success w-100">Login</button>
                    </form>

                    {% with messages = get_flashed_messages(with_categories=true) %}
                        {% if messages %}
                            <ul class="mt-3 list-group">
                                {% for category, message in messages %}
                                    <li class="list-group-item list-group-item-{{ 'success' if category == 'success' else 'danger' }}">
                                        {{ message }}
                                    </li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    {% endwith %}
                </div>
            </div>
        </div>
    </div>

<script>
document.getElementById("password").addEventListener("input", function() {
    let pwd = this.value;
    let feedback = [];

    if (pwd.length < 8) {
        feedback.push("❌ Minimum 8 characters");
    } else {
        feedback.push("✅ Minimum 8 characters");
    }

    if (/[A-Z]/.test(pwd)) {
        feedback.push("✅ At least one uppercase letter");
    } else {
        feedback.push("❌ At least one uppercase letter");
    }

    if (/[a-z]/.test(pwd)) {
        feedback.push("✅ At least one lowercase letter");
    } else {
        feedback.push("❌ At least one lowercase letter");
    }

    if (/[0-9]/.test(pwd)) {
        feedback.push("✅ At least one number");
    } else {
        feedback.push("❌ At least one number");
    }

    if (/[!@#$%^&*(),.?\":{}|<>]/.test(pwd)) {
        feedback.push("✅ At least one special character");
    } else {
        feedback.push("❌ At least one special character");
    }

    document.getElementById("feedback").innerHTML = feedback.join("<br>");
});
</script>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        errors = check_password_strength(password)

        if errors:
            for error in errors:
                flash(error, "error")
        else:
            flash(f"Welcome, {username}! ✅ Password is strong.", "success")
            return redirect(url_for("login"))

    return render_template_string(HTML_TEMPLATE)

def check_password_strength(password):
    import re
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain at least one lowercase letter.")
    if not re.search(r"\d", password):
        errors.append("Password must contain at least one digit.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        errors.append("Password must contain at least one special character.")

    return errors

if __name__ == "__main__":
    app.run(debug=True)
