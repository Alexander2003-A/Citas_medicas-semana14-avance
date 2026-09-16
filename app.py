import os
from conexion.conexion import get_connection
from flask import Flask, render_template, redirect, url_for, flash

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturaForm

from forms.login_form import LoginForm
from forms.usuario_form import UsuarioForm

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import Usuario



app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id, usuario, password FROM usuarios WHERE id = %s",
        (user_id,)
    )

    datos_usuario = cursor.fetchone()

    cursor.close()
    conn.close()

    if datos_usuario:
        return Usuario(
            datos_usuario["id"],
            datos_usuario["usuario"],
            datos_usuario["password"]
        )

    return None


# Ruta de registro de usuarios
@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = UsuarioForm()

    if form.validate_on_submit():
        usuario = form.usuario.data.strip()
        password = form.password.data

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Comprobar si el usuario ya existe
        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = %s",
            (usuario,)
        )

        usuario_existente = cursor.fetchone()

        if usuario_existente:
            cursor.close()
            conn.close()

            flash("El nombre de usuario ya está registrado.", "warning")
            return render_template("registro.html", form=form)

        # Proteger la contraseña antes de guardarla
        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
            (usuario, password_hash)
        )

        conn.commit()
        cursor.close()
        conn.close()

        flash("Usuario registrado correctamente.", "success")

        return redirect(url_for("login"))

    return render_template("registro.html", form=form)

#RUTA DE LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        usuario = form.usuario.data.strip()
        password = form.password.data

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT id, usuario, password FROM usuarios WHERE usuario = %s",
            (usuario,)
        )

        datos_usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if datos_usuario and check_password_hash(
            datos_usuario["password"],
            password
        ):
            usuario_objeto = Usuario(
                datos_usuario["id"],
                datos_usuario["usuario"],
                datos_usuario["password"]
            )

            login_user(usuario_objeto)

            flash("Inicio de sesión correcto.", "success")

            return redirect(url_for("dashboard"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html", form=form)

#RUTA PARA CERRAR SECION
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "success")
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")



# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta de clientes
@app.route("/clientes")
@login_required
def clientes():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_cliente, nombre, cedula, telefono, correo FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("clientes.html", clientes=clientes)

# Ruta de proveedores
@app.route("/proveedores")
@login_required
def proveedores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_proveedor, nombre, telefono, correo FROM proveedores")
    proveedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("proveedores.html", proveedores=proveedores)

# Ruta de facturación
@app.route("/facturacion")
@login_required
def facturacion():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT f.id_factura, f.id_cliente, c.nombre AS cliente, f.fecha, f.total
        FROM facturas f
        INNER JOIN clientes c ON f.id_cliente = c.id_cliente
    """)
    facturas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("facturacion.html", facturas=facturas)

@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Obtener el producto
    cursor.execute(
        "SELECT * FROM productos WHERE id_producto = %s",
        (id,)
    )
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        conn.close()
        return "Producto no encontrado"

    # Obtener proveedores
    cursor.execute(
        "SELECT id_proveedor, nombre FROM proveedores"
    )
    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    # Cargar datos actuales del producto
    form = ProductoForm(data={
        "nombre": producto["nombre"],
        "precio": producto["precio"],
        "stock": producto["stock"],
        "proveedor": producto["id_proveedor"]
    })

    # Cargar proveedores en el selector
    form.proveedor.choices = [
        (p["id_proveedor"], p["nombre"])
        for p in proveedores
    ]

    if form.validate_on_submit():

        nombre = form.nombre.data
        precio = form.precio.data
        stock = form.stock.data
        id_proveedor = form.proveedor.data

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET nombre = %s,
                precio = %s,
                stock = %s,
                id_proveedor = %s
            WHERE id_producto = %s
            """,
            (
                nombre,
                precio,
                stock,
                id_proveedor,
                id
            )
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("productos"))

    return render_template(
        "editar_producto.html",
        form=form,
        producto=producto
    )

@app.route("/eliminar_producto/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id_producto = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("productos"))

@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
@login_required
def editar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id_cliente = %s", (id,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()

    if not cliente:
        return "Cliente no encontrado"

    form = ClienteForm(data=cliente)
    if form.validate_on_submit():
        nombre = form.nombre.data
        cedula = form.cedula.data
        telefono = form.telefono.data
        correo = form.correo.data

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE clientes 
            SET nombre=%s, cedula=%s, telefono=%s, correo=%s 
            WHERE id_cliente=%s
        """, (nombre, cedula, telefono, correo, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("clientes"))

    return render_template("editar_cliente.html", form=form, cliente=cliente)

@app.route("/eliminar_cliente/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id_cliente = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("clientes"))


# Formulario de productos
@app.route("/formulario_producto", methods=["GET", "POST"])
@login_required
def formulario_producto():

    form = ProductoForm()

    # Obtener proveedores desde MySQL
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT id_proveedor, nombre FROM proveedores"
    )

    proveedores = cursor.fetchall()

    cursor.close()
    conn.close()

    # Cargar proveedores en el SelectField
    form.proveedor.choices = [
        (p["id_proveedor"], p["nombre"])
        for p in proveedores
    ]

    if form.validate_on_submit():

        nombre = form.nombre.data
        precio = form.precio.data
        stock = form.stock.data
        id_proveedor = form.proveedor.data

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO productos
            (nombre, precio, stock, id_proveedor)
            VALUES (%s, %s, %s, %s)
            """,
            (nombre, precio, stock, id_proveedor)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )

# Formulario de clientes
@app.route("/formulario_cliente", methods=["GET", "POST"])
@login_required
def formulario_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        cedula = form.cedula.data
        telefono = form.telefono.data
        correo = form.correo.data
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO clientes (nombre, cedula, telefono, correo) VALUES (%s, %s, %s, %s)",
                       (nombre, cedula, telefono, correo))
        conn.commit()
        conn.close()
        return redirect(url_for("clientes"))
    return render_template("formulario_cliente.html", form=form)

# Formulario de proveedores
@app.route("/formulario_proveedor", methods=["GET", "POST"])
@login_required
def formulario_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        nombre = form.nombre.data
        telefono = form.telefono.data
        correo = form.correo.data
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO proveedores (nombre, telefono, correo) VALUES (%s, %s, %s)",
                       (nombre, telefono, correo))
        conn.commit()
        conn.close()
        return redirect(url_for("proveedores"))
    return render_template("formulario_proveedor.html", form=form)


@app.route("/editar_proveedor/<int:id>", methods=["GET", "POST"])
@login_required
def editar_proveedor(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM proveedores WHERE id_proveedor = %s",
        (id,)
    )

    proveedor = cursor.fetchone()

    cursor.close()
    conn.close()

    if not proveedor:
        return "Proveedor no encontrado"

    form = ProveedorForm(data=proveedor)

    if form.validate_on_submit():
        nombre = form.nombre.data
        telefono = form.telefono.data
        correo = form.correo.data

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE proveedores
            SET nombre = %s,
                telefono = %s,
                correo = %s
            WHERE id_proveedor = %s
            """,
            (nombre, telefono, correo, id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("proveedores"))

    return render_template(
        "editar_proveedor.html",
        form=form,
        proveedor=proveedor
    )


@app.route("/eliminar_proveedor/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):
    conn = get_connection()
    cursor = conn.cursor()

    # Comprobar si el proveedor tiene productos asociados
    cursor.execute(
        "SELECT COUNT(*) FROM productos WHERE id_proveedor = %s",
        (id,)
    )

    cantidad_productos = cursor.fetchone()[0]

    if cantidad_productos > 0:
        cursor.close()
        conn.close()

        flash(
            "No se puede eliminar este proveedor porque tiene productos asociados.",
            "warning"
        )

        return redirect(url_for("proveedores"))

    # Si no tiene productos, se puede eliminar
    cursor.execute(
        "DELETE FROM proveedores WHERE id_proveedor = %s",
        (id,)
    )

    conn.commit()
    cursor.close()
    conn.close()

    flash("Proveedor eliminado correctamente.", "success")

    return redirect(url_for("proveedores"))

# Formulario de facturación
@app.route("/formulario_facturacion", methods=["GET", "POST"])
@login_required
def formulario_facturacion():
    form = FacturaForm()
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_cliente, nombre FROM clientes")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    form.cliente.choices = [(c["id_cliente"], c["nombre"]) for c in clientes]
    if form.validate_on_submit():
        cliente = form.cliente.data
        total = form.total.data
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO facturas (id_cliente, fecha, total) VALUES (%s, CURDATE(), %s)",
                       (cliente, total))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("facturacion"))
    return render_template("formulario_facturacion.html", form=form)

# Ruta de productos
@app.route("/productos")
@login_required
def productos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_producto, nombre, precio, stock FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("productos.html", productos=productos)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)

