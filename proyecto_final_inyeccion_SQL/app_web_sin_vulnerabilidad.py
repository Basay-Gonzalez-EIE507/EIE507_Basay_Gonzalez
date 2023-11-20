from flask import Flask, render_template, request, redirect, session, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'eie'

def get_db_connection():
    return psycopg2.connect(
        host="192.168.100.111",
        database="postgres",
        user="postgres",
        password="Admin.123"
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Uso de consultas parametrizadas
        sql_query_authentication = "SELECT * FROM users WHERE username = %s AND password = %s"
        db_conn = get_db_connection()
        cursor = db_conn.cursor()

        try:
            cursor.execute(sql_query_authentication, (username, password))
            user = cursor.fetchone()
        except psycopg2.Error as e:
            user = None
        finally:
            cursor.close()
            db_conn.close()

        if user:
            session['username'] = username
            return redirect(url_for('perfil'))
        else:
            flash('Credenciales incorrectas', 'error')

    return render_template('login.html')

@app.route('/perfil')
def perfil():
    if 'username' in session:
        username = session['username']
        db_conn = get_db_connection()
        cursor = db_conn.cursor()

        try:
            # Consulta que une la información de ambas tablas
            sql_query = """
                SELECT u.full_name, u.email, ui.direccion, ui.numero_tarjeta
                FROM users u
                INNER JOIN user_info ui ON u.user_id = ui.user_id
                WHERE u.username = %s
            """
            cursor.execute(sql_query, (username,))

            user_info = cursor.fetchone()
        except psycopg2.Error as e:
            user_info = None
        finally:
            cursor.close()
            db_conn.close()

        if user_info:
            full_name, email, direccion, numero_tarjeta = user_info
            return render_template('perfil.html', full_name=full_name, email=email, direccion=direccion, numero_tarjeta=numero_tarjeta)
        else:
            return "Información del usuario no encontrada."

    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def search():
    if 'username' in session:
        results = None
        if request.method == 'POST':
            search_term = request.form['search_term']
            db_conn = get_db_connection()
            cursor = db_conn.cursor()

            try:
                sql_query = "SELECT first_name FROM actor WHERE first_name = %s"
                cursor.execute(sql_query, (search_term,))
                results = cursor.fetchall()
            except psycopg2.Error as e:
                results = None
            finally:
                cursor.close()
                db_conn.close()

        return render_template('search.html', results=results)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
