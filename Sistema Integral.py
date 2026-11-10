# REGISTRO DE EVENTOS Y ERRORES
# ENCADENAMIENTO DE EXEPCIONES
# DATOS ERRONEOS
# CLASE CLIENTE
# EQUIPOS

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import logging
from abc import ABC, abstractmethod
from datetime import datetime
import math

# REGISTRO DE EVENTOS Y ERRORES
logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
# ENCADENAMIENTO DE EXEPCIONES
class DatosVaciosError(Exception):
    pass
class ClienteInvalidoError(Exception):
    pass
class ServicioNoDisponibleError(Exception):
    pass
class ReservaInvalidaError(Exception):
    pass
class OperacionNoPermitidaError(Exception):
    pass

# DATOS ERRONEOS
class Entidad(ABC):

    def __init__(self, identificacion):
        if not identificacion or not str(identificacion).strip():
            raise DatosVaciosError(
                "La identificacion es obligatoria."
            )

        self.__identificacion = str(identificacion).strip()

    @property
    def identificacion(self):
        return self.__identificacion

    @abstractmethod
    def mostrar_informacion(self):
        pass
    
# CLASE CLIENTE
class Cliente(Entidad):

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        if not nombre or not nombre.strip():
            raise ClienteInvalidoError(
                "El nombre del cliente es obligatorio."
            )

        if not correo or "@" not in correo or "." not in correo:
            raise ClienteInvalidoError(
                "El correo electronico no es valido."
            )

        if not telefono or not telefono.strip():
            raise ClienteInvalidoError(
                "El telefono es obligatorio."
            )

        self.__nombre = nombre.strip()
        self.__correo = correo.strip()
        self.__telefono = telefono.strip()

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def mostrar_informacion(self):
        return (
            f"Identificacion: {self.identificacion}\n"
            f"Nombre: {self.nombre}\n"
            f"Correo: {self.correo}\n"
            f"Telefono: {self.telefono}"
        )
# CLASE ABSTRACTA SERVICIO
class Servicio(ABC):

    def __init__(self, codigo, nombre, tarifa, disponible=True):

        if not codigo or not str(codigo).strip():
            raise DatosVaciosError(
                "El codigo del servicio es obligatorio."
            )

        if not nombre or not nombre.strip():
            raise DatosVaciosError(
                "El nombre del servicio es obligatorio."
            )

        try:
            tarifa = float(tarifa)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "La tarifa debe ser un numero."
            ) from error

        if not math.isfinite(tarifa) or tarifa <= 0:
            raise ValueError(
                "La tarifa debe ser mayor que cero."
            )

        self.__codigo = str(codigo).strip()
        self.__nombre = nombre.strip()
        self.__tarifa = tarifa
        self.__disponible = bool(disponible)

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nombre(self):
        return self.__nombre

    @property
    def tarifa(self):
        return self.__tarifa

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        self.__disponible = bool(valor)

    # Uso de parametros opcionales para simular sobrecarga.
    def calcular_costo(self, duracion, impuesto=0, descuento=0):

        try:
            duracion = float(duracion)
            impuesto = float(impuesto)
            descuento = float(descuento)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "Los valores del calculo deben ser numericos."
            ) from error
