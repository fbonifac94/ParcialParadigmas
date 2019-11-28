
from flask import Flask, render_template, redirect, url_for, flash, session, request
from forms import IngresoForm, RegistroForm, ConsultaPaisForm
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

@app.route('/consultas/pais')
def consultaPorPais():
    if 'usuario' in session:
        pais = request.args.get("pais")
        if pais:
            rows = []
            with open("clientes.csv", encoding="utf-8") as archivo:
                archivo_csv = csv.reader(archivo)
                headers = next(archivo_csv)
                registro = next(archivo_csv, None)
                paisarg = str(pais).lower()
                while registro:
                    reg = str(registro[3]).lower()
                    if paisarg in reg:
                        rows.append(registro)
                    registro = next(archivo_csv, None)
                if len(rows) < 1:
                    flash('No se encontraron registros relacionados a la búsqueda.')
                return render_template("consultapais.html", headers = headers, rows = rows)
        return render_template("consultapais.html")
    return redirect(url_for('ingreso'))

@app.route('/consultasDos/pais')
def consultaPorPaisDos():
    if 'usuario' in session:
        pais = request.args.get("pais")
        if pais:
            with open("clientes.csv", encoding="utf-8") as archivo:
                archivo_csv = csv.reader(archivo)
                registro = next(archivo_csv)
                paisarg = str(pais).lower()
                paises = []
                while registro:
                    reg = str(registro[3]).lower()
                    if paisarg in reg and registro[3] not in paises:
                        paises.append(registro[3])
                    registro = next(archivo_csv, None)
                if len(paises) < 1:
                    flash('No se encontraron registros relacionados a la búsqueda.')
                return render_template("consultapaisdos.html", paises = paises)
        return render_template("consultapaisdos.html")
    return redirect(url_for('ingreso'))

@app.route('/consultasTres/pais', methods = ['GET', 'POST'])
def consultaPorPaisTres():
    if 'usuario' in session:
        paisForm = ConsultaPaisForm()
        if paisForm.validate_on_submit():
            arg = str(paisForm.pais.data).lower()
            with open("clientes.csv", encoding="utf-8") as archivo:
                archivo_csv = csv.reader(archivo)
                registro = next(archivo_csv)
                paises = []
                while registro:
                    reg = str(registro[3]).lower()
                    if arg in reg and registro[3] not in paises:
                        paises.append(registro[3])
                    registro = next(archivo_csv, None)
                return render_template('consultapaistres.html', formulario = paisForm, paises = paises, dosubmit = paisForm.validate_on_submit())
        return render_template('consultapaistres.html', formulario = paisForm)
    return redirect(url_for('ingreso'))

@app.route('/consultasDos/pais/<pais>')
def consultaPorPaisDosLista(pais):
    if 'usuario' in session:
        if pais:
            with open("clientes.csv", encoding="utf-8") as archivo:
                archivo_csv = csv.reader(archivo)
                header = next(archivo_csv)
                registro = next(archivo_csv, None)
                paisArg = str(pais).lower()
                rows = []
                while registro:
                    reg = str(registro[3]).lower()
                    if paisArg in reg:
                        rows.append(registro)
                    registro = next(archivo_csv, None)
                return render_template("listado.html", rows = rows, headers = header)
        return render_template("consultapaisdos.html")
    return redirect(url_for('ingreso'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)