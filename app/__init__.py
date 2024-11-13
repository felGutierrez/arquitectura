from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class SingletonDB:
    _instance = None

    def __new__(cls, app=None):
        if cls._instance is None:
            cls._instance = super(SingletonDB, cls).__new__(cls)
            cls._instance.init_app(app)
        return cls._instance

    def init_app(self, app):
        if app is not None:
            db.init_app(app)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    SingletonDB(app)  # Singleton instance of DB

    with app.app_context():
        from models import GastoComunModel,DepartamentoModel
        from models.DepartamentoModel import Departamento  
        db.create_all()
        # Verificar si hay departamentos en la base de datos, si no, insertarlos
        if Departamento.query.count() == 0:  
            departamentos = [
                Departamento(id='101', numero='101', ubicacion='Piso 1, Bloque A', tamaño='50m', estado_ocupacion='ocupado'),
                Departamento(id='102', numero='102', ubicacion='Piso 1, Bloque B', tamaño='60m', estado_ocupacion='vacio'),
                Departamento(id='201', numero='201', ubicacion='Piso 2, Bloque A', tamaño='70m', estado_ocupacion='ocupado'),
                Departamento(id='202', numero='202', ubicacion='Piso 2, Bloque B', tamaño='80m', estado_ocupacion='vacio'),
            ]

            db.session.add_all(departamentos)
            db.session.commit()

    return app
