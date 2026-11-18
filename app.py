from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_bi'

# Almacenamiento en memoria para el estado de los 3 invernaderos
estado_invernaderos = {
    1: {"temperatura": 0.0, "humedad": 0.0, "humidificador": False, "ventilador": False, "respiradero": False},
    2: {"temperatura": 0.0, "humedad": 0.0, "humidificador": False},
    3: {"temperatura": 0.0, "humedad": 0.0, "humidificador": False}
}

# Rutas de navegación modular
@app.route('/')
def inicio():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('inicio.html')

@app.route('/proyecto')
def proyecto():
    return render_template('proyecto.html')

@app.route('/maqueta')
def maqueta():
    return render_template('maqueta.html')

@app.route('/bases_datos')
def bases_datos():
    return render_template('bases_datos.html')

@app.route('/envivo')
def envivo():
    return render_template('envivo.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/conocimientos')
def conocimientos():
    return render_template('conocimientos.html')

@app.route('/resultados')
def resultados():
    return render_template('resultados.html')

# Autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == 'admin2026':
            session['logged_in'] = True
            return redirect(url_for('inicio'))
        error = 'Credenciales inválidas. Usa admin / admin2026'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# API para Telemetría ESP32
@app.route('/api/lecturas', methods=['POST'])
def recibir_lecturas():
    data = request.json
    if not data or 'invernadero_id' not in data:
        return jsonify({"error": "Datos inválidos"}), 400
    
    inv_id = int(data['invernadero_id'])
    if inv_id in estado_invernaderos:
        estado_invernaderos[inv_id].update({
            "temperatura": float(data.get('temperatura', 0.0)),
            "humedad": float(data.get('humedad', 0.0)),
            "humidificador": bool(data.get('humidificador', False)),
            "ventilador": bool(data.get('ventilador', False)),
            "respiradero": bool(data.get('respiradero', False))
        })
    return jsonify({"status": "success"}), 200

@app.route('/api/kpis', methods=['GET'])
def obtener_kpis():
    hums = [v['humedad'] for v in estado_invernaderos.values()]
    prom_hum = sum(hums) / len(hums) if hums else 0.0
    return jsonify({
        "eficiencia_operativa": f"{prom_hum:.1f}% Prom",
        "registros_procesados": "1,000,000+",
        "alertas_activas": 0,
        "estado_sistema": f"{prom_hum:.1f}°C Prom",
        "detalle": estado_invernaderos
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)