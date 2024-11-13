from models.GastoComunModel import db, GastoComun
from models.DepartamentoModel import Departamento
from datetime import datetime,timedelta,date
import re

class GastoService:
    @staticmethod
    def create_gasto_comun(monto, periodo, fecha, departamento_id):
        # Validación del formato del periodo (YYYY-MM)
        if not periodo or not re.match(r'^\d{4}-\d{2}$', periodo):
            return None, "El formato del periodo es inválido. Debe ser en formato 'YYYY-MM'."

        # Validar que el mes sea un valor entre 01 y 12
        año, mes = periodo.split('-')
        if not (1 <= int(mes) <= 12):
            return None, "El mes del periodo debe estar entre 01 y 12."
        
        # Si la fecha no es proporcionada, usamos la fecha actual
        if not fecha:
            fecha = datetime.now().strftime('%Y-%m-%d')
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()

        gasto_existente = GastoComun.query.filter_by(departamento_id=departamento_id, periodo=periodo).first()

        if gasto_existente:
            return None, "Ya existe un gasto comun para este departamento en el periodo indicado."

        departamento_existe = Departamento.query.filter_by(id=departamento_id).first()
        if not departamento_existe:
            return None, "El Departamento indicado no existe."
        
        if departamento_existe.estado_ocupacion == 'vacio':
            return None, "El Departamento esta vacio"


        gasto_comun = GastoComun(monto=monto, periodo=periodo, fecha=fecha_obj, departamento_id=departamento_id)
        db.session.add(gasto_comun)
        db.session.commit()
        return gasto_comun, None

    @staticmethod
    def getListadoMoroso(periodo):
        # Si 'fecha' no es None, la convertimos a un objeto datetime
        if periodo and isinstance(periodo, str):  
            periodo = datetime.strptime(periodo, '%Y-%m').date() 

        if periodo:
            gastos = GastoComun.query.filter(
                GastoComun.periodo <= periodo,
                GastoComun.estado == 'pendiente'
            ).all()
        else:
            gastos = GastoComun.query.filter(
                GastoComun.estado == 'pendiente'
            ).all()
            
        return gastos

    @staticmethod
    def getPagado(departamento_id, periodo, fecha):

        
        gasto = GastoComun.query.filter_by(departamento_id=departamento_id, periodo=periodo).first()
        
        if not gasto:
            return None  
        
        if gasto.estado == 'pagado':
            return {
                "gasto": gasto.serialize(),
                "mensaje": "Pago duplicado"
            }    

        # Asegurar que ambas fechas son de tipo date para la comparación
        fecha_limite = gasto.periodo
        if isinstance(fecha, datetime):
            fecha_formateada = fecha.strftime('%Y-%m')
        elif isinstance(fecha, date):
            fecha_formateada = fecha.strftime('%Y-%m')
        elif isinstance(fecha, str):
            fecha_formateada = datetime.strptime(fecha, '%Y-%m-%d').strftime('%Y-%m')
        else:
            raise ValueError("Formato de fecha no válido")
        
        # Comparar la fecha formateada con el periodo
        if fecha_formateada <= fecha_limite:
            mensaje_estado = "Pago exitoso dentro del plazo"
        else:
            mensaje_estado = "Pago exitoso fuera de plazo"
        
        gasto.estado = 'pagado'
        gasto.fecha_pago = fecha
        db.session.commit()
        return {
            "gasto": gasto.serialize(),
            "mensaje": mensaje_estado
        }
 
