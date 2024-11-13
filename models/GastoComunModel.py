from app import db
from datetime import datetime

class GastoComun(db.Model):
    __tablename__ = 'gastos_comunes'

    gasto_id = db.Column(db.Integer, primary_key=True)  
    monto = db.Column(db.Float, nullable=False) 
    fecha = db.Column(db.Date, nullable=False)  # Fecha de creación del gasto
    fecha_pago = db.Column(db.Date, nullable=True)  
    periodo = db.Column(db.String(7), nullable=False)  # Periodo del gasto (por ejemplo: '2024-10')
    estado = db.Column(db.String(20), default='pendiente')  # Estado del gasto ('pendiente', 'pagado')

    departamento_id = db.Column(db.Integer, db.ForeignKey('departamentos.id'), nullable=False)  
    departamento = db.relationship('Departamento', back_populates='gastos_comunes') 

    def serialize(self):
        return {
            'gasto_id': self.gasto_id,
            'monto': self.monto,
            'fecha': self.fecha.isoformat(),
            'fecha_pago': self.fecha_pago.isoformat() if self.fecha_pago else None, 
            'periodo': self.periodo,
            'estado': self.estado,
            'departamento_id': self.departamento_id,   
            'departamento': self.departamento.numero 
        }