
from flask import Flask, render_template, redirect, url_for, flash, session
from forms import IngresoForm, RegistroForm
from flask_bootstrap import Bootstrap
import csv

app = Flask(__name__)
bootstrap = Bootstrap(app)

app.config['SECRET_KEY'] = 'Hola'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/ingreso', methods=['GET', 'POST'])
def ingreso():
    form = IngresoForm()
    if form.validate_on_submit():
        with open('usuarios') as archivo:
            archivo_csv = csv.reader(archivo)
            registro = next(archivo_csv)
            while registro:
                if registro[0] == form.usuario.data and registro[1] == form.contrasenia.data:
                    session['usuario'] = registro[0]
                    archivo.close()
                    flash('Bienvenido')
                    return redirect(url_for('ingreso'))
                registro = next(archivo_csv, None)
        archivo.close()
    return render_template('ingreso.html', formulario = form)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    registerForm = RegistroForm()
    if registerForm.validate_on_submit():
        if registerForm.contrasenia.data == registerForm.confirmContrasenia.data:
            with open('usuarios', 'a', newline='') as archivo:
                archivo_csv = csv.writer(archivo)
                reg = [registerForm.usuario.data,registerForm.contrasenia.data]
                archivo_csv.writerow(reg)
            return redirect(url_for('index'))
        else:
            flash('Las contraseñas no coinciden.')
    return render_template('registro.html', formulario = registerForm)

@app.route('/listado')
def listado():
    if 'usuario' in session:
        rows = []
        with open('clientes.csv', encoding='utf8') as archivo:
            archivo_csv = csv.reader(archivo)
            headers = next(archivo_csv)
            registro = next(archivo_csv, None)
            while registro:
                rows.append(registro)
                registro = next(archivo_csv, None)
            archivo.close()
            return render_template('listado.html', rows = rows, headers = headers)
    return redirect(url_for('ingreso'))
    
@app.route('/cerrarsesion')
def cerrarSesion():
    if 'usuario' in session:
        session.pop('usuario')
    return redirect(url_for('ingreso'))

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.errorhandler(404)
def recursoNoEncontrado(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def errorInterno(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)