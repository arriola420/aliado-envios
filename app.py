import unicodedata

from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
app.json.ensure_ascii = False

MONEDA = 'COP'
TARIFAS = [
    {'ciudad': 'Medellín', 'costo': 8000, 'dias': 1},
    {'ciudad': 'Bogotá', 'costo': 12000, 'dias': 2},
    {'ciudad': 'Cali', 'costo': 12000, 'dias': 2},
    {'ciudad': 'Barranquilla', 'costo': 15000, 'dias': 3},
    {'ciudad': 'Cartagena', 'costo': 15000, 'dias': 3},
    {'ciudad': 'Bucaramanga', 'costo': 13000, 'dias': 2},
]


def _normalizar(texto):
    sin_tildes = unicodedata.normalize('NFD', texto)
    sin_tildes = ''.join(c for c in sin_tildes if unicodedata.category(c) != 'Mn')
    return sin_tildes.strip().casefold()


@app.get('/api/v2/envios/tarifas')
def tarifas():
    """Sin parámetros lista todas las tarifas; con ?ciudad= cotiza una sola."""
    ciudad = request.args.get('ciudad', '').strip()
    resultado = TARIFAS
    if ciudad:
        resultado = [t for t in TARIFAS if _normalizar(t['ciudad']) == _normalizar(ciudad)]
        if not resultado:
            return jsonify({'error': f'No hay cobertura para "{ciudad}".'}), 404
    return jsonify({
        'servicio': 'Servicio Aliado de Envíos (v2)',
        'moneda': MONEDA,
        'tarifas': resultado,
    })


@app.errorhandler(Exception)
def manejar_error(error):
    if isinstance(error, HTTPException):
        return jsonify({'error': error.description}), error.code
    app.logger.exception('Error no controlado en el servicio de envíos')
    return jsonify({'error': 'Error interno del servicio de envíos.'}), 500
