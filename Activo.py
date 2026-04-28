#---¡Esta-clase-es-usada-por-la-clase-portafolio!
class Activo:
    def __init__(self, nombre, data):
        self.nombre = nombre
        self.data_actual = data
        self.precio_actual = data["Close"].iloc[-1]

    def minimo(self):
        return self.data_actual["Low"].min()

    def maximo(self):
        return self.data_actual["High"].max()

    def retorno(self):
        return (self.precio_actual / self.data_actual["Close"].iloc[0]) - 1