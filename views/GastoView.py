from datetime import datetime
from flask import Blueprint, request, jsonify
from controllers.GastoController import GastoController

gastos_comunes_blueprint = Blueprint('gastos_comunes_blueprint', __name__)

class GastoView:
    # Crear gasto común
    @staticmethod
    @gastos_comunes_blueprint.route('/gastos/create', methods=['POST'])
    def create_gasto_comun():
        data = request.get_json()
        monto = data.get('monto')
        periodo = data.get('periodo')
        fecha = data.get('fecha')
        departamento_id = data.get('departamento_id')

        new_gasto, error = GastoController.create_gasto_comun_controller(monto, periodo, fecha, departamento_id)
        if error:
            return jsonify({"mensaje": error}), 400
        return jsonify({"mensaje": "Gasto comun creado", "gasto": new_gasto.serialize()}), 201


    # Listado de gastos morosos
    @staticmethod
    @gastos_comunes_blueprint.route('/gastos/morosos', methods=['GET'])
    def getListadoMoroso():
        
        periodo = request.args.get('periodo') 
        
        # Validación de fecha
        if periodo:
            try:
                periodo = datetime.strptime(periodo, '%Y-%m').date()
            except ValueError:
                return jsonify({"mensaje": "Formato de fecha invalido, debe ser YYYY-MM"}), 400
        else:
            periodo = None  # Si no se pasa fecha, dejarla como None

        # Obtener el listado de gastos morosos
        gastos = GastoController.getListadoMoroso_controller(periodo)
        gastos_list = [gasto.serialize() for gasto in gastos]

        if not gastos_list:
            return jsonify({"mensaje": "Sin montos pendientes"}), 404

        return jsonify({"gastos": gastos_list}), 2000

    # Marcar un gasto como pagado
    @staticmethod
    @gastos_comunes_blueprint.route('/gastos/pagar', methods=['PATCH'])
    def getPagado():
        departamento_id = request.args.get('departamento_id')
        periodo = request.args.get('periodo')
        fecha = datetime.now().date()

        gasto = GastoController.getPagado_controller(departamento_id, periodo, fecha)

        if gasto:
            return jsonify({
            "mensaje": gasto["mensaje"],
            "gasto": gasto["gasto"]
        }), 200
        else:
            return jsonify({"mensaje": "Gasto no encontrado o departamento no existe"}), 404
