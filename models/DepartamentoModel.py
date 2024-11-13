from app import db

class Departamento(db.Model):
    __tablename__ = 'departamentos'

    id = db.Column(db.Integer, primary_key=True) 
    numero = db.Column(db.String(10), nullable=False, unique=True)  
    ubicacion = db.Column(db.String(100), nullable=False) 
    tamaño = db.Column(db.String(50), nullable=False) 
    estado_ocupacion = db.Column(db.String(20), nullable=False)  # Estado de ocupación: 'ocupado' o 'vacío'

    # Relación con los Gastos Comunes
    gastos_comunes = db.relationship('GastoComun', back_populates='departamento')

    def serialize(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'ubicacion': self.ubicacion,
            'tamaño': self.tamaño,
            'estado_ocupacion': self.estado_ocupacion,
            'gastos_comunes': [gasto.serialize() for gasto in self.gastos_comunes]
        }