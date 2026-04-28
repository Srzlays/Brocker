#---¡Al-Brocker-se-le-asignó-una-comision-estandar-del-1.5%!
#---¡Esta-clase-es-usada-por-la-clase-Portafolio!
class Brocker:
    def __init__(self):
        self.comision = 1.5

    def aplicar_comision_compra(self, monto):
        return monto * (1 + self.comision / 100)

    def aplicar_comision_venta(self, monto):
        return monto * (1 - self.comision / 100)