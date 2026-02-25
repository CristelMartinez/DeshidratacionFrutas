from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import mysql.connector
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import send_file

# ---------------------------------------------------
# CONFIGURACIÓN DE FLASK
# ---------------------------------------------------
app = Flask(__name__)
app.secret_key = "clave_super_secreta"

# ---------------------------------------------------
# CONEXIÓN A LA BASE DE DATOS
# ---------------------------------------------------
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Guadcris2002",
        database="Deshidratacion"
    )

# ---------------------------------------------------
# DECORADORES DE SEGURIDAD
# ---------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_role") != "administrador":
            flash("Acceso no autorizado")
            return redirect(url_for("frutas"))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------------------------------
# LOGIN / LOGOUT
# ---------------------------------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "SELECT ID_Usuario, Nombre, Password, Rol FROM Usuarios WHERE Email=%s",
            (email,)
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        if user and user[2] == password:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            session["user_role"] = user[3]
            return redirect(url_for("dashboard"))
        else:
            flash("Correo o contraseña incorrectos")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Frutas")
    frutas = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("dashboard.html", frutas=frutas)


# ---------------------------------------------------
# HOME
# ---------------------------------------------------
@app.route("/")
@login_required
def home():
    return redirect("/frutas")

# =====================================================
# ================== CRUD FRUTAS ======================
# =====================================================
@app.route("/frutas")
@login_required
def frutas():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Frutas")
    datos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("frutas.html", frutas=datos)

@app.route("/frutas/agregar", methods=["POST"])
@login_required
def frutas_agregar():
    nombre = request.form["nombre"]
    tipo = request.form["tipo"]
    tiempo = request.form["tiempo"]
    temp = request.form["temperatura"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO Frutas (Nombre, Tipo, Tiempo_Deshidratacion, Temperatura_Ideal)
        VALUES (%s, %s, %s, %s)
    """, (nombre, tipo, tiempo, temp))
    db.commit()
    cursor.close()
    db.close()
    return redirect("/frutas")

@app.route("/frutas/eliminar/<int:id>")
@login_required
def frutas_eliminar(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Frutas WHERE ID_Fruta=%s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect("/frutas")

@app.route("/frutas/editar/<int:id>")
@login_required
def frutas_editar(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Frutas WHERE ID_Fruta=%s", (id,))
    fruta = cursor.fetchone()
    cursor.close()
    db.close()
    return render_template("editar_fruta.html", fruta=fruta)

@app.route("/frutas/actualizar/<int:id>", methods=["POST"])
@login_required
def frutas_actualizar(id):
    nombre = request.form["nombre"]
    tipo = request.form["tipo"]
    tiempo = request.form["tiempo"]
    temp = request.form["temperatura"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE Frutas
        SET Nombre=%s, Tipo=%s, Tiempo_Deshidratacion=%s, Temperatura_Ideal=%s
        WHERE ID_Fruta=%s
    """, (nombre, tipo, tiempo, temp, id))
    db.commit()
    cursor.close()
    db.close()
    return redirect("/frutas")

# =====================================================
# ================== CRUD USUARIOS (ADMIN) =============
# =====================================================
@app.route("/usuarios")
@login_required
@admin_required
def usuarios():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT ID_Usuario, Nombre, Email, Rol FROM Usuarios")
    datos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("usuarios.html", usuarios=datos)

@app.route("/usuarios/nuevo", methods=["GET", "POST"])
@login_required
@admin_required
def nuevo_usuario():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = request.form["password"]
        rol = request.form["rol"]

        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Usuarios (Nombre, Email, Password, Rol) VALUES (%s, %s, %s, %s)",
            (nombre, email, password, rol)
        )
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for("usuarios"))

    return render_template("nuevo_usuario.html")

@app.route("/usuarios/eliminar/<int:id>")
@login_required
@admin_required
def usuarios_eliminar(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Usuarios WHERE ID_Usuario=%s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return redirect("/usuarios")

@app.route("/usuarios/editar/<int:id>")
@login_required
@admin_required
def usuarios_editar(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE ID_Usuario=%s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    db.close()

    return render_template("editar_usuario.html", usuario=usuario)

@app.route("/usuarios/actualizar/<int:id>", methods=["POST"])
@login_required
@admin_required
def usuarios_actualizar(id):
    nombre = request.form["nombre"]
    email = request.form["email"]
    password = request.form["password"]
    rol = request.form["rol"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE Usuarios
        SET Nombre=%s,
            Email=%s,
            Password=%s,
            Rol=%s
        WHERE ID_Usuario=%s
    """, (nombre, email, password, rol, id))
    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("usuarios"))

# =====================================================
# ================== CRUD PROCESOS ====================
# =====================================================

def actualizar_procesos_automaticos():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE Procesos
        INNER JOIN Frutas ON Procesos.ID_Fruta = Frutas.ID_Fruta
        SET 
            Procesos.Fecha_Fin = NOW(),
            Procesos.Estado = 'finalizado',
            Procesos.Resultado = 'deshidratado'
        WHERE 
            Procesos.Estado = 'en progreso'
            AND DATE_ADD(Procesos.Fecha_Inicio, 
                INTERVAL Frutas.Tiempo_Deshidratacion MINUTE) <= NOW()
    """)

    db.commit()
    cursor.close()
    db.close()


@app.route("/procesos")
@login_required
def procesos():
    # 🔁 Actualiza procesos automáticamente
    actualizar_procesos_automaticos()

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT Procesos.ID_Proceso,
               Frutas.Nombre,
               Usuarios.Nombre,
               Procesos.Fecha_Inicio,
               Procesos.Fecha_Fin,
               Procesos.Estado,
               Procesos.Resultado,
               Frutas.Tiempo_Deshidratacion
        FROM Procesos
        INNER JOIN Frutas ON Procesos.ID_Fruta = Frutas.ID_Fruta
        INNER JOIN Usuarios ON Procesos.ID_Usuario = Usuarios.ID_Usuario
        ORDER BY Procesos.Fecha_Inicio DESC
    """)

    filas = cursor.fetchall()
    procesos = []

    for p in filas:
        inicio = p[3]
        tiempo = p[7]
        fin = inicio + timedelta(minutes=tiempo)
        ahora = datetime.now()

        if p[5] == "en progreso":
            restante = fin - ahora
            if restante.total_seconds() <= 0:
                restante_str = "Finalizando..."
            else:
                minutos = int(restante.total_seconds() // 60)
                segundos = int(restante.total_seconds() % 60)
                restante_str = f"{minutos}:{segundos:02d}"
        else:
            restante_str = None

        procesos.append({
            "id": p[0],
            "fruta": p[1],
            "usuario": p[2],
            "inicio": p[3],
            "fin": p[4],
            "estado": p[5],
            "resultado": p[6],
            "restante": restante_str
        })

    cursor.execute("SELECT ID_Fruta, Nombre FROM Frutas")
    frutas = cursor.fetchall()

    cursor.execute("SELECT ID_Usuario, Nombre FROM Usuarios")
    usuarios = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "procesos.html",
        procesos=procesos,
        frutas=frutas,
        usuarios=usuarios
    )


@app.route("/procesos/agregar", methods=["POST"])
@login_required
def procesos_agregar():
    fruta_id = request.form.get("fruta")
    usuario_id = request.form.get("usuario")

    if not fruta_id or not usuario_id:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for("procesos"))

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO Procesos (ID_Fruta, ID_Usuario, Fecha_Inicio, Estado)
        VALUES (%s, %s, NOW(), 'en progreso')
    """, (fruta_id, usuario_id))

    db.commit()
    cursor.close()
    db.close()

    flash("Proceso iniciado correctamente", "success")
    return redirect(url_for("procesos"))


@app.route("/procesos/cancelar/<int:id>")
@login_required
@admin_required
def procesos_cancelar(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        UPDATE Procesos
        SET Fecha_Fin = NOW(),
            Estado = 'cancelado',
            Resultado = 'cancelado'
        WHERE ID_Proceso = %s
          AND Estado = 'en progreso'
    """, (id,))

    db.commit()
    cursor.close()
    db.close()

    flash("Proceso cancelado", "warning")
    return redirect(url_for("procesos"))


@app.route("/procesos/eliminar/<int:id>")
@login_required
@admin_required
def procesos_eliminar(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM Procesos WHERE ID_Proceso=%s", (id,))
    db.commit()

    cursor.close()
    db.close()

    flash("Proceso eliminado", "danger")
    return redirect(url_for("procesos"))


# =====================================================
# ================== CRUD ALERTAS =====================
# =====================================================
@app.route("/alertas")
@login_required
def alertas():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT Alertas.ID_Alerta,
               Procesos.ID_Proceso,
               Alertas.Tipo,
               Alertas.Mensaje,
               Alertas.Fecha
        FROM Alertas
        INNER JOIN Procesos ON Alertas.ID_Proceso = Procesos.ID_Proceso
        ORDER BY Alertas.Fecha DESC
    """)
    alertas = cursor.fetchall()

    cursor.execute("SELECT ID_Proceso FROM Procesos")
    procesos = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template(
        "alertas.html",
        alertas=alertas,
        procesos=procesos
    )

@app.route("/alertas/agregar", methods=["POST"])
@login_required
@admin_required
def alertas_agregar():
    proceso = request.form["proceso"]
    tipo = request.form["tipo"]
    mensaje = request.form["mensaje"]

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO Alertas (ID_Proceso, Tipo, Mensaje, Fecha)
        VALUES (%s, %s, %s, NOW())
    """, (proceso, tipo, mensaje))
    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("alertas"))

@app.route("/alertas/eliminar/<int:id>")
@login_required
@admin_required
def alertas_eliminar(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Alertas WHERE ID_Alerta=%s", (id,))
    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for("alertas"))

# =====================================================
# ================== REPORTE FINAL ====================
# =====================================================
@app.route("/reporte")
@login_required
@admin_required
def reporte():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT 
            RF.ID_Reporte,
            RF.Fecha_Generacion,
            RF.Duracion_Minutos,
            RF.Total_Alertas,
            RF.Temperatura_Promedio,
            RF.Resultado,
            RF.Observaciones,
            P.ID_Proceso,
            F.Nombre,
            U.Nombre
        FROM Reporte_Final RF
        INNER JOIN Procesos P ON RF.ID_Proceso = P.ID_Proceso
        INNER JOIN Frutas F ON P.ID_Fruta = F.ID_Fruta
        INNER JOIN Usuarios U ON P.ID_Usuario = U.ID_Usuario
        ORDER BY RF.Fecha_Generacion DESC
    """)

    reportes = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("reporte.html", reportes=reportes)

# =====================================================
# ============== GENERAR REPORTE ======================
# =====================================================
@app.route("/reporte/generar", methods=["GET", "POST"])
@login_required
@admin_required
def generar_reporte():
    db = get_db()
    cursor = db.cursor()

    if request.method == "POST":
        proceso_id = request.form["proceso_id"]
        observaciones = request.form["observaciones"]

        # Duración
        cursor.execute("""
            SELECT TIMESTAMPDIFF(MINUTE, Fecha_Inicio, Fecha_Fin)
            FROM Procesos
            WHERE ID_Proceso = %s
        """, (proceso_id,))
        duracion = cursor.fetchone()[0] or 0

        # Alertas
        cursor.execute("""
            SELECT COUNT(*) FROM Alertas
            WHERE ID_Proceso = %s
        """, (proceso_id,))
        alertas = cursor.fetchone()[0]

        # Temperatura desde Frutas
        cursor.execute("""
            SELECT F.Temperatura_Ideal
            FROM Procesos P
            INNER JOIN Frutas F ON P.ID_Fruta = F.ID_Fruta
            WHERE P.ID_Proceso = %s
        """, (proceso_id,))
        temp_prom = cursor.fetchone()[0]

        # Resultado
        cursor.execute("""
            SELECT Estado FROM Procesos
            WHERE ID_Proceso = %s
        """, (proceso_id,))
        resultado = cursor.fetchone()[0]

        # Insertar reporte
        cursor.execute("""
            INSERT INTO Reporte_Final
            (ID_Proceso, Fecha_Generacion, Duracion_Minutos,
             Total_Alertas, Temperatura_Promedio, Resultado, Observaciones)
            VALUES (%s, NOW(), %s, %s, %s, %s, %s)
        """, (proceso_id, duracion, alertas, temp_prom, resultado, observaciones))

        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for("reporte"))

    # Mostrar procesos no activos
    cursor.execute("""
        SELECT P.ID_Proceso, F.Nombre, P.Estado
        FROM Procesos P
        INNER JOIN Frutas F ON P.ID_Fruta = F.ID_Fruta
        WHERE P.Estado != 'activo'
    """)
    procesos = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("generar_reporte.html", procesos=procesos)

@app.route("/reporte/pdf/<int:id>")
@login_required
@admin_required
def reporte_pdf(id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT R.ID_Reporte, R.Fecha_Generacion, R.Duracion_Minutos,
               R.Total_Alertas, R.Temperatura_Promedio,
               R.Resultado, R.Observaciones,
               F.Nombre, U.Nombre
        FROM Reporte_Final R
        INNER JOIN Procesos P ON R.ID_Proceso = P.ID_Proceso
        INNER JOIN Frutas F ON P.ID_Fruta = F.ID_Fruta
        INNER JOIN Usuarios U ON P.ID_Usuario = U.ID_Usuario
        WHERE R.ID_Reporte = %s
    """, (id,))

    reporte = cursor.fetchone()
    cursor.close()
    db.close()

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "REPORTE FINAL DE DESHIDRATACIÓN")
    y -= 40

    pdf.setFont("Helvetica", 12)
    datos = [
        f"ID Reporte: {reporte[0]}",
        f"Fecha: {reporte[1]}",
        f"Duración: {reporte[2]} minutos",
        f"Total de alertas: {reporte[3]}",
        f"Temperatura promedio: {reporte[4]} °C",
        f"Resultado: {reporte[5]}",
        f"Fruta: {reporte[7]}",
        f"Operador: {reporte[8]}",
        f"Observaciones: {reporte[6]}"
    ]

    for d in datos:
        pdf.drawString(50, y, d)
        y -= 25

    pdf.showPage()
    pdf.save()

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"reporte_{id}.pdf",
        mimetype="application/pdf"
    )



# ---------------------------------------------------
# INICIAR SERVIDOR
# ---------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
