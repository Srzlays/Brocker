import yfinance as yf
import pandas as pd
import Brocker as BROCKER
import Activo as ACTIVO 


class Portafolio:
    def __init__(self, capital):
        self.capital = capital
        self.posiciones = []
        self.brocker = BROCKER.Brocker()

    def comprar(self, cantidad, activo):
        costo = activo.precio_actual * cantidad
        total = self.brocker.aplicar_comision_compra(costo)

        if total > self.capital:
            return "Capital insuficiente"

        for pos in self.posiciones:
            if pos["activo"].nombre == activo.nombre:
                total_cant = pos["cantidad"] + cantidad
                nuevo_precio = (
                    pos["precio_promedio"] * pos["cantidad"] +
                    activo.precio_actual * cantidad
                ) / total_cant

                pos["cantidad"] = total_cant
                pos["precio_promedio"] = nuevo_precio
                pos["inversion"] += total 
                self.capital -= total
                return "Compra agregada"

        self.posiciones.append({
            "activo": activo,
            "cantidad": cantidad,
            "precio_promedio": activo.precio_actual,
            "inversion": total  
        })

        self.capital -= total
        return "Compra realizada"

    def vender(self, nombre, cantidad):
        for pos in self.posiciones:
            if pos["activo"].nombre == nombre:

                if cantidad > pos["cantidad"]:
                    return "No tienes suficientes acciones"

                activo = pos["activo"]
                ingreso_bruto = activo.precio_actual * cantidad
                ingreso_neto = self.brocker.aplicar_comision_venta(ingreso_bruto)

                costo = pos["precio_promedio"] * cantidad
                pnl = ingreso_neto - costo

                pos["cantidad"] -= cantidad

                if pos["cantidad"] == 0:
                    self.posiciones.remove(pos)

                self.capital += ingreso_neto

                return f"Venta realizada | P&L: ${pnl:.2f}"

        return "Activo no encontrado"

    def valor(self):
        return sum(
            self.brocker.aplicar_comision_venta(
                p["activo"].precio_actual * p["cantidad"]
            )
            for p in self.posiciones
        )

    def rentabilidad(self):
        inversion = sum(p["inversion"] for p in self.posiciones)
        if inversion == 0:
            return 0
        return (self.valor() / inversion) - 1