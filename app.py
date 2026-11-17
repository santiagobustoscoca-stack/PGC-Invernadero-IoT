from flask import Flask, render_template, jsonify, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'clave_secreta_super_segura_bi'

# Almacenamiento en memoria para el estado de los 3 invernaderos
estado_invernaderos = {
    1: {"temperatura": 0.0, "humedad": 0.0, "humidificador": False, "ventilador": False, "respiradero": False},
    2: {"temperatura": 0.0, "humedad": 0.0, "humidificador": False},
    3: {"temperatura": 0.0, "humedad": 0.0, "humidificador": False}
}

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        if user == 'admin' and password == 'admin2026':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Credenciales incorrectas. Intenta de nuevo.'
    
    return '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Acceso al PGC</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-950 text-white flex items-center justify-center h-screen">
        <div class="bg-slate-900 border border-slate-800 p-8 rounded-2xl shadow-xl w-full max-w-md">
            <h2 class="text-2xl font-bold text-emerald-500 mb-2">Portal Documental PGC</h2>
            <p class="text-xs text-slate-400 mb-6">Inicia sesión para acceder a la documentación del proyecto.</p>
            ''' + (f'<div class="bg-red-500/10 border border-red-500 text-red-400 text-xs p-3 rounded-lg mb-4">{error}</div>' if error else '') + '''
            <form method="POST" class="space-y-4">
                <div>
                    <label class="block text-xs font-medium text-slate-300 mb-1">Usuario</label>
                    <input type="text" name="username" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-emerald-500">
                </div>
                <div>
                    <label class="block text-xs font-medium text-slate-300 mb-1">Contraseña</label>
                    <input type="password" name="password" required class="w-full bg-slate-950 border border-slate-800 rounded-lg px-4 py-2 text-sm focus:outline-none focus:border-emerald-500">
                </div>
                <button type="submit" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2 rounded-lg text-sm transition mt-2">
                    Visualizar Proyecto
                </button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/api/lecturas', methods=['POST'])
def recibir_lecturas():
    data = request.get_json()
    if data and 'invernadero_id' in data:
        inv_id = int(data['invernadero_id'])
        if inv_id in estado_invernaderos:
            estado_invernaderos[inv_id] = data
            return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Datos inválidos"}), 400

@app.route('/api/eventos', methods=['POST'])
def recibir_eventos():
    return jsonify({"status": "success"}), 200

@app.route('/api/kpis')
def api_kpis():
    if not session.get('logged_in'):
        return jsonify({"error": "No autorizado"}), 401
    
    t1, h1 = estado_invernaderos[1].get("temperatura", 0.0), estado_invernaderos[1].get("humedad", 0.0)
    t2, h2 = estado_invernaderos[2].get("temperatura", 0.0), estado_invernaderos[2].get("humedad", 0.0)
    t3, h3 = estado_invernaderos[3].get("temperatura", 0.0), estado_invernaderos[3].get("humedad", 0.0)
    
    prom_temp = round((t1 + t2 + t3) / 3, 1)
    prom_hum = round((h1 + h2 + h3) / 3, 1)
    
    return jsonify({
        "registros_procesados": "142,850",
        "eficiencia_operativa": f"{prom_hum}% Prom",
        "alertas_activas": 0 if prom_temp < 35 else 1,
        "estado_sistema": f"Online ({prom_temp}°C Prom)",
        "detalle": estado_invernaderos
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)