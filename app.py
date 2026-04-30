# app.py — AyamKu Modern (Flask, Clean UI, 2026 Ready)

from flask import Flask, request, redirect, url_for, session, flash, render_template_string
from datetime import datetime

app = Flask(__name__)
app.secret_key = "ayamku-secure-2026"

# ─────────────────────────────
# SIMPLE DATABASE (memory)
# ─────────────────────────────
kandang_db = []
pengiriman_db = []

USERS = {
    "admin": {"password": "admin123", "role": "admin", "name": "Admin Bos"},
    "karyawan": {"password": "karya123", "role": "karyawan", "name": "Karyawan"}
}

# ─────────────────────────────
# TEMPLATE (ALL-IN-ONE, CLEAN UI)
# ─────────────────────────────
BASE_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset='UTF-8'>
<title>AyamKu 2026</title>
<style>
body { font-family: Arial; background:#0d1117; color:#e6edf3; padding:20px }
.card { background:#161b22; padding:20px; border-radius:10px; margin-bottom:20px }
input,select { padding:8px; width:100%; margin-top:5px; margin-bottom:10px }
button { padding:10px; background:#f0a500; border:none; cursor:pointer }
table { width:100%; border-collapse:collapse }
th,td { padding:10px; border-bottom:1px solid #30363d }
h2 { color:#f0a500 }
.nav { margin-bottom:20px }
a { color:#58a6ff; text-decoration:none; margin-right:10px }
</style>
</head>
<body>
<div class='nav'>
<a href='/'>Home</a>
{% if session.user %}
<a href='/logout'>Logout</a>
{% endif %}
</div>

{% with messages = get_flashed_messages() %}
  {% if messages %}
    <div class='card'>{{ messages[0] }}</div>
  {% endif %}
{% endwith %}

{{ content }}
</body>
</html>
"""

# ─────────────────────────────
# ROUTES
# ─────────────────────────────
@app.route("/")
def home():
    return render_template_string(BASE_HTML, content="""
    <div class='card'>
    <h2>Login AyamKu</h2>
    <form method='post' action='/login'>
    Username:<input name='username'>
    Password:<input name='password' type='password'>
    Role:
    <select name='role'>
      <option value='admin'>Admin</option>
      <option value='karyawan'>Karyawan</option>
    </select>
    <button>Login</button>
    </form>
    </div>
    """)

@app.route("/login", methods=["POST"])
def login():
    u = request.form.get("username")
    p = request.form.get("password")
    r = request.form.get("role")

    user = USERS.get(u)
    if not user or user["password"] != p or user["role"] != r:
        flash("Login gagal!")
        return redirect(url_for("home"))

    session["user"] = user

    return redirect(url_for("admin" if r == "admin" else "karyawan"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ─────────────────────────────
# ADMIN
# ─────────────────────────────
@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect("/")

    stats = {
        "hidup": kandang_db[-1]["hidup"] if kandang_db else 0,
        "mati": sum(x["mati"] for x in kandang_db),
        "sakit": sum(x["sakit"] for x in kandang_db),
        "kirim": sum(x["jumlah"] for x in pengiriman_db)
    }

    return render_template_string(BASE_HTML, content=f"""
    <div class='card'>
    <h2>Dashboard Admin</h2>
    Hidup: {stats['hidup']}<br>
    Mati: {stats['mati']}<br>
    Sakit: {stats['sakit']}<br>
    Dikirim: {stats['kirim']}
    </div>

    <div class='card'>
    <h3>Data Kandang</h3>
    <table>
    <tr><th>Tanggal</th><th>Hidup</th><th>Mati</th></tr>
    {''.join([f"<tr><td>{x['tanggal']}</td><td>{x['hidup']}</td><td>{x['mati']}</td></tr>" for x in kandang_db])}
    </table>
    </div>
    """)

# ─────────────────────────────
# KARYAWAN
# ─────────────────────────────
@app.route("/karyawan")
def karyawan():
    if "user" not in session:
        return redirect("/")

    return render_template_string(BASE_HTML, content="""
    <div class='card'>
    <h2>Input Kandang</h2>
    <form method='post' action='/kandang'>
    Tanggal:<input type='date' name='tanggal'>
    Hidup:<input type='number' name='hidup'>
    Mati:<input type='number' name='mati'>
    Sakit:<input type='number' name='sakit'>
    <button>Simpan</button>
    </form>
    </div>

    <div class='card'>
    <h2>Input Pengiriman</h2>
    <form method='post' action='/pengiriman'>
    Tanggal:<input type='date' name='tanggal'>
    Tujuan:<input name='tujuan'>
    Jumlah:<input type='number' name='jumlah'>
    <button>Simpan</button>
    </form>
    </div>
    """)

@app.route("/kandang", methods=["POST"])
def kandang():
    kandang_db.append({
        "tanggal": request.form.get("tanggal"),
        "hidup": int(request.form.get("hidup") or 0),
        "mati": int(request.form.get("mati") or 0),
        "sakit": int(request.form.get("sakit") or 0),
        "time": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    flash("Data kandang tersimpan!")
    return redirect("/karyawan")

@app.route("/pengiriman", methods=["POST"])
def pengiriman():
    pengiriman_db.append({
        "tanggal": request.form.get("tanggal"),
        "tujuan": request.form.get("tujuan"),
        "jumlah": int(request.form.get("jumlah") or 0)
    })

    flash("Data pengiriman tersimpan!")
    return redirect("/karyawan")

# ─────────────────────────────
# RUN
# ─────────────────────────────
if __name__ == "__main__":
    app.run(debug=True)
