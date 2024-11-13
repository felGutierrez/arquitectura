from app import create_app
from views.GastoView import gastos_comunes_blueprint

app = create_app()
app.register_blueprint(gastos_comunes_blueprint)

if __name__ == '__main__':
    app.run(debug=True)