from services.GastoService import GastoService

class GastoController:
    @staticmethod
    def create_gasto_comun_controller(monto, periodo, fecha, departamento_id):
        return GastoService.create_gasto_comun(monto, periodo, fecha, departamento_id)
    
    ##http://127.0.0.1:5000/gastos/create
    # Usar Postman con metodo POST
    #{
    #"monto": 100.0,
    #"periodo": "2024-10",
    #"fecha": "2024-10-03",
    #"departamento_id": 101
    #}
    ##


    @staticmethod
    def getListadoMoroso_controller(periodo):
        return GastoService.getListadoMoroso(periodo)
    
    ##http://127.0.0.1:5000/gastos/morosos?periodo=2024-12
    # Usar Postman con metodo GET o usar navegador
    ##


    @staticmethod
    def getPagado_controller(departamento_id, periodo, fecha):
        return GastoService.getPagado(departamento_id, periodo, fecha)
    
    ## http://127.0.0.1:5000/gastos/pagar?departamento_id=101&periodo=2024-02