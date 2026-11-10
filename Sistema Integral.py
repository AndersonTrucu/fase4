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
valores = [duracion, impuesto, descuento]

        if not all(math.isfinite(v) for v in valores):
            raise ValueError("Los valores del calculo no son validos.")

        if duracion <= 0:
            raise ValueError("La duracion debe ser mayor que cero.")

        if not 0 <= impuesto <= 100:
            raise ValueError("El impuesto debe estar entre 0 y 100.")

        if not 0 <= descuento <= 100:
            raise ValueError("El descuento debe estar entre 0 y 100.")

        subtotal = self.tarifa * duracion
        valor_impuesto = subtotal * impuesto / 100
        valor_descuento = subtotal * descuento / 100

        total = subtotal + valor_impuesto - valor_descuento

        if total < 0:
            raise ValueError("El costo calculado no puede ser negativo.")

        return round(total, 2)

    @abstractmethod
    def describir(self):
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        pass
    
# SERVICIO 1: RESERVA DE SALAS
class ReservaSala(Servicio):

    def __init__(self, codigo, nombre, tarifa, capacidad):
        super().__init__(codigo, nombre, tarifa)

        try:
            capacidad = int(capacidad)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "La capacidad debe ser un numero entero."
            ) from error

        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self.__capacidad = capacidad

    @property
    def capacidad(self):
        return self.__capacidad

    def describir(self):
        return (
            f"Reserva de sala: {self.nombre}. "
            f"Capacidad: {self.capacidad} personas."
        )

    def validar_parametros(self, duracion):
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as error:
            raise ReservaInvalidaError(
                "La duracion de la reserva debe ser numerica."
            ) from error

        if not math.isfinite(duracion) or duracion <= 0:
            raise ReservaInvalidaError(
                "La duracion de la sala debe ser mayor que cero."
            )

        return True
    
# EQUIPOS
class AlquilerEquipo(Servicio):

    def __init__(self, codigo, nombre, tarifa, unidades):
        super().__init__(codigo, nombre, tarifa)

        try:
            unidades = int(unidades)
        except (TypeError, ValueError) as error:
            raise ValueError(
                "Las unidades deben ser un numero entero."
            ) from error

        if unidades <= 0:
            raise ValueError("Las unidades deben ser mayores que cero.")

        self.__unidades = unidades

    @property
    def unidades(self):
        return self.__unidades

    def describir(self):
        return (
            f"Alquiler de equipos: {self.nombre}. "
            f"Unidades disponibles: {self.unidades}."
        )

    def validar_parametros(self, duracion):
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as error:
            raise ReservaInvalidaError(
                "La duracion del alquiler debe ser numerica."
            ) from error

        if not math.isfinite(duracion) or duracion <= 0:
            raise ReservaInvalidaError(
                "El tiempo de alquiler debe ser mayor que cero."
            )

        if duracion > 720:
            raise ReservaInvalidaError(
                "El alquiler no puede superar 720 horas."
            )

        return True

# SERVICIO 3: ASESORIAS ESPECIALIZADAS
class Asesoria(Servicio):

    def __init__(self, codigo, nombre, tarifa, especialidad):
        super().__init__(codigo, nombre, tarifa)

        if not especialidad or not especialidad.strip():
            raise DatosVaciosError(
                "Debe ingresar la especialidad de la asesoria."
            )

        self.__especialidad = especialidad.strip()

    @property
    def especialidad(self):
        return self.__especialidad

    def describir(self):
        return (
            f"Asesoria especializada: {self.nombre}. "
            f"Especialidad: {self.especialidad}."
        )
    def validar_parametros(self, duracion):
        try:
            duracion = float(duracion)
        except (TypeError, ValueError) as error:
            raise ReservaInvalidaError(
                "La duracion de la asesoria debe ser numerica."
            ) from error
        if not math.isfinite(duracion) or duracion <= 0:
            raise ReservaInvalidaError(
                "La duracion de la asesoria debe ser mayor que cero."
            )
        if duracion > 8:
            raise ReservaInvalidaError(
                "La asesoria no puede superar 8 horas."
            )

        return True

# CLASE RESERVA
class Reserva(Entidad):
    def __init__(self, codigo, cliente, servicio, duracion, costo):
        super().__init__(codigo)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError(
                "Debe seleccionar un cliente valido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError(
                "Debe seleccionar un servicio valido."
            )
        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__costo = costo
        self.__estado = "Pendiente"
        self.__fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @property
    def cliente(self):
        return self.__cliente

    @property
    def servicio(self):
        return self.__servicio

    @property
    def duracion(self):
        return self.__duracion

    @property
    def costo(self):
        return self.__costo

    @property
    def estado(self):
        return self.__estado

    def confirmar(self):

        if self.__estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.__estado = "Confirmada"
        logging.info(
            "Reserva %s confirmada.", self.identificacion
        )

    def cancelar(self):

        if self.__estado == "Cancelada":
            raise OperacionNoPermitidaError(
                "La reserva ya se encuentra cancelada."
            )

        if self.__estado == "Procesada":
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva procesada."
            )

        self.__estado = "Cancelada"
        logging.info(
            "Reserva %s cancelada.", self.identificacion
        )

    def procesar(self):

        if self.__estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "La reserva debe estar confirmada para procesarse."
            )

        self.__estado = "Procesada"
        logging.info(
            "Reserva %s procesada.", self.identificacion
        )

    def mostrar_informacion(self):
        return (
            f"Codigo: {self.identificacion}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Duracion: {self.duracion}\n"
            f"Costo: ${self.costo:,.2f}\n"
            f"Estado: {self.estado}\n"
            f"Fecha: {self.__fecha}"
        )

# CLASE PARA CONTROLAR EL USUARIO Y LA CONTRASENA
class Usuario:

    def __init__(self, usuario, password):
        self.__usuario = usuario
        self.__password = password

    def validar(self, usuario_ingresado, password_ingresada):

        if not usuario_ingresado or not password_ingresada:
            raise DatosVaciosError(
                "Debe escribir el usuario y la contrasena."
            )

        return (
            usuario_ingresado == self.__usuario
            and password_ingresada == self.__password
        )
# CLASE PRINCIPAL DEL SISTEMA
class SistemaFJ:

    def __init__(self):

        # Listas internas para almacenar los objetos.
        self.clientes = []
        self.servicios = []
        self.reservas = []

        self.usuario = Usuario("Anderson", "1234")

        self.cargar_servicios_iniciales()
    
    # CARGAR SERVICIOS DE EJEMPLO
    def cargar_servicios_iniciales(self):

        self.servicios.append(
            ReservaSala("S001", "Sala de reuniones", 50000, 20)
        )
        self.servicios.append(
            AlquilerEquipo("S002", "Equipo de computo", 15000, 10)
        )
        self.servicios.append(
            Asesoria(
                "S003",
                "Asesoria tecnologica",
                80000,
                "Tecnologia"
            )
        )

        logging.info("Servicios iniciales cargados.")
        
    # REGISTRAR CLIENTE
    def registrar_cliente(self, identificacion, nombre, correo, telefono):

        if any(
            c.identificacion == str(identificacion).strip()
            for c in self.clientes
        ):
            raise ClienteInvalidoError(
                "Ya existe un cliente con esa identificacion."
            )

        cliente = Cliente(
            identificacion, nombre, correo, telefono
        )

        self.clientes.append(cliente)

        logging.info(
            "Cliente registrado: %s", cliente.nombre
        )

        return cliente

    # BUSCAR CLIENTE
    def buscar_cliente(self, identificacion):

        for cliente in self.clientes:
            if cliente.identificacion == str(identificacion).strip():
                return cliente

        return None
    
    # BUSCAR SERVICIO
    def buscar_servicio(self, codigo):

        for servicio in self.servicios:
            if servicio.codigo == str(codigo).strip():
                return servicio

        return None
    
    # AGREGAR SERVICIO
    def agregar_servicio(self, servicio):

        if not isinstance(servicio, Servicio):
            raise TypeError(
                "El objeto debe pertenecer a una clase de servicio."
            )

        if self.buscar_servicio(servicio.codigo):
            raise ValueError(
                "Ya existe un servicio con ese codigo."
            )

        self.servicios.append(servicio)

        logging.info(
            "Servicio agregado: %s", servicio.nombre
        )

        return servicio

    # CREAR RESERVA
    def crear_reserva(
        self, codigo, identificacion_cliente,
        codigo_servicio, duracion, impuesto=0, descuento=0
    ):
        try:

            cliente = self.buscar_cliente(identificacion_cliente)

            if cliente is None:
                raise ClienteInvalidoError(
                    "El cliente no se encuentra registrado."
                )

            servicio = self.buscar_servicio(codigo_servicio)

            if servicio is None:
                raise ServicioNoDisponibleError(
                    "El servicio seleccionado no existe."
                )

            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    "El servicio no se encuentra disponible."
                )

            if any(
                r.identificacion == str(codigo).strip()
                for r in self.reservas
            ):
                raise ReservaInvalidaError(
                    "Ya existe una reserva con ese codigo."
                )

            servicio.validar_parametros(duracion)

            costo = servicio.calcular_costo(
                duracion, impuesto, descuento
            )

            reserva = Reserva(
                codigo, cliente, servicio, float(duracion), costo
            )

            self.reservas.append(reserva)

            logging.info(
                "Reserva creada: %s", reserva.identificacion
            )

            return reserva

        except (
            ClienteInvalidoError,
            ServicioNoDisponibleError,
            ReservaInvalidaError,
            ValueError,
            DatosVaciosError
        ) as error:

            logging.error(
                "Error al crear reserva: %s", error
            )

            raise ReservaInvalidaError(
                f"No fue posible crear la reserva: {error}"
            ) from error

   # BUSCAR RESERVA
    def buscar_reserva(self, codigo):

        for reserva in self.reservas:
            if reserva.identificacion == str(codigo).strip():
                return reserva

        return None

 # REPORTE GENERAL
    def generar_reporte(self):

        resultado = "========== REPORTE SOFTWARE FJ ==========\n\n"

        resultado += "CLIENTES REGISTRADOS\n"

        if not self.clientes:
            resultado += "No hay clientes registrados.\n"

        for cliente in self.clientes:
            resultado += (
                f"{cliente.identificacion} - {cliente.nombre}\n"
            )

        resultado += "\nSERVICIOS DISPONIBLES\n"

        for servicio in self.servicios:
            estado = (
                "Disponible" if servicio.disponible
                else "No disponible"
            )

            resultado += (
                f"{servicio.codigo} - {servicio.nombre} - "
                f"${servicio.tarifa:,.2f} - {estado}\n"
            )

        resultado += "\nRESERVAS REGISTRADAS\n"

        if not self.reservas:
            resultado += "No hay reservas registradas.\n"

        for reserva in self.reservas:
            resultado += (
                f"{reserva.identificacion} - "
                f"{reserva.cliente.nombre} - "
                f"{reserva.servicio.nombre} - "
                f"${reserva.costo:,.2f} - "
                f"{reserva.estado}\n"
            )

        resultado += "\n========================================="

        return resultado

  # PRUEBAS DE FUNCIONAMIENTO

    def ejecutar_pruebas(self):

        resultados = []
        exitos = 0
        errores = 0

        def registrar_prueba(nombre, funcion):

            nonlocal exitos, errores

            try:
                funcion()
                resultados.append(
                    f"[CORRECTO] {nombre}"
                )
                exitos += 1

            except Exception as error:
                resultados.append(
                    f"[ERROR] {nombre}: {error}"
                )
                errores += 1

                logging.exception(
                    "Fallo en prueba: %s", nombre
                )

        # 1. Registro correcto de cliente.
        registrar_prueba(
            "Registrar cliente valido",
            lambda: self.registrar_cliente(
                "TEST001", "Cliente de prueba",
                "prueba@test.com", "3001234567"
            )
        )

        # 2. Buscar cliente existente.
        registrar_prueba(
            "Buscar cliente registrado",
            lambda: self._comprobar(
                self.buscar_cliente("TEST001") is not None,
                "No se encontro el cliente."
            )
        )

        # 3. Intentar registrar identificacion duplicada.
        registrar_prueba(
            "Controlar identificacion duplicada",
            lambda: self._esperar_error(
                lambda: self.registrar_cliente(
                    "TEST001", "Otro cliente",
                    "otro@test.com", "3000000000"
                ),
                ClienteInvalidoError
            )
        )

        # 4. Controlar correo invalido.
        registrar_prueba(
            "Validar correo incorrecto",
            lambda: self._esperar_error(
                lambda: Cliente(
                    "TEST002", "Cliente",
                    "correo_invalido", "3000000000"
                ),
                ClienteInvalidoError
            )
        )

        # 5. Verificar servicios iniciales.
        registrar_prueba(
            "Consultar servicios iniciales",
            lambda: self._comprobar(
                len(self.servicios) >= 3,
                "No estan cargados los tres servicios."
            )
        )

        # 6. Agregar servicio nuevo.
        registrar_prueba(
            "Agregar nuevo servicio",
            lambda: self.agregar_servicio(
                Asesoria(
                    "S004", "Asesoria de prueba",
                    50000, "Informatica"
                )
            )
        )

        # 7. Crear reserva correctamente.
        registrar_prueba(
            "Crear reserva valida",
            lambda: self.crear_reserva(
                "RTEST01", "TEST001", "S001", 2
            )
        )

        # 8. Confirmar reserva.
        registrar_prueba(
            "Confirmar reserva",
            lambda: self.buscar_reserva("RTEST01").confirmar()
        )

        # 9. Procesar reserva confirmada.
        registrar_prueba(
            "Procesar reserva",
            lambda: self.buscar_reserva("RTEST01").procesar()
        )

        # 10. Evitar reserva con cliente inexistente.
        registrar_prueba(
            "Controlar reserva con cliente inexistente",
            lambda: self._esperar_error(
                lambda: self.crear_reserva(
                    "RTEST02", "NO_EXISTE", "S001", 2
                ),
                ReservaInvalidaError
            )
        )

        # 11. Evitar duracion incorrecta.
        registrar_prueba(
            "Controlar duracion incorrecta",
            lambda: self._esperar_error(
                lambda: self.crear_reserva(
                    "RTEST03", "TEST001", "S001", -2
                ),
                ReservaInvalidaError
            )
        )

        # 12. Controlar servicio inexistente.
        registrar_prueba(
            "Controlar servicio inexistente",
            lambda: self._esperar_error(
                lambda: self.crear_reserva(
                    "RTEST04", "TEST001", "NO_EXISTE", 2
                ),
                ReservaInvalidaError
            )
        )

        return (
            "RESULTADO DE PRUEBAS \n\n"
            + "\n".join(resultados)
            + f"\n\nPruebas correctas: {exitos}"
            + f"\nPruebas con errores: {errores}"
            + f"\nTotal de operaciones: {exitos + errores}"
        )

    @staticmethod
    def _comprobar(condicion, mensaje):

        if not condicion:
            raise AssertionError(mensaje)

    @staticmethod
    def _esperar_error(funcion, tipo_error):

        try:
            funcion()

        except tipo_error:
            return True

        raise AssertionError(
            f"Se esperaba la excepcion {tipo_error.__name__}."
        )

# CLASE PRINCIPAL DE LA APLICACION GRAFICA

class AplicacionSoftwareFJ:

    def __init__(self, ventana):

        self.ventana = ventana
        self.sistema = SistemaFJ()

        # Se conserva el usuario y contrasena originales.
        self.usuario = Usuario("Anderson", "1234")

        self.ventana.title(
            "Software FJ - Inicio de sesion"
        )
        self.ventana.geometry("500x420")
        self.ventana.resizable(False, False)

        self.mostrar_login()

    # FUNCIONES GENERALES

    def limpiar_ventana(self):

        for elemento in self.ventana.winfo_children():
            elemento.destroy()

    def crear_titulo(self, texto):

        tk.Label(
            self.ventana,
            text=texto,
            font=("Arial", 19, "bold")
        ).pack(pady=15)

    def mostrar_texto(self, titulo, contenido):

        ventana_texto = tk.Toplevel(self.ventana)
        ventana_texto.title(titulo)
        ventana_texto.geometry("700x500")

        marco = tk.Frame(ventana_texto)
        marco.pack(fill="both", expand=True, padx=10, pady=10)

        barra = tk.Scrollbar(marco)
        barra.pack(side="right", fill="y")

        area = tk.Text(
            marco,
            wrap="word",
            yscrollcommand=barra.set
        )
        area.pack(fill="both", expand=True)

        barra.config(command=area.yview)

        area.insert("1.0", contenido)
        area.config(state="disabled")

    def pedir_dato(self, titulo, mensaje):

        return simpledialog.askstring(
            titulo, mensaje, parent=self.ventana
        )

    def pedir_numero(self, titulo, mensaje):

        return simpledialog.askfloat(
            titulo, mensaje, parent=self.ventana
        )

    # PANTALLA DE INICIO DE SESION

    def mostrar_login(self):

        self.limpiar_ventana()

        self.ventana.title(
            "Software FJ - Inicio de sesion"
        )
        self.ventana.geometry("450x350")

        tk.Label(
            self.ventana,
            text="SOFTWARE FJ",
            font=("Arial", 22, "bold")
        ).pack(pady=25)

        tk.Label(
            self.ventana,
            text="Sistema Integral de Gestion",
            font=("Arial", 11)
        ).pack(pady=5)

        tk.Label(
            self.ventana,
            text="Usuario"
        ).pack()

        self.campo_usuario = tk.Entry(
            self.ventana, width=30
        )
        self.campo_usuario.pack(pady=5)

        tk.Label(
            self.ventana,
            text="Contrasena"
        ).pack()

        self.campo_password = tk.Entry(
            self.ventana, width=30, show="*"
        )
        self.campo_password.pack(pady=5)

        tk.Button(
            self.ventana,
            text="Ingresar",
            width=20,
            command=self.iniciar_sesion
        ).pack(pady=20)

        self.campo_usuario.focus()

    # VALIDAR INICIO DE SESION

    def iniciar_sesion(self):

        usuario = self.campo_usuario.get().strip()
        password = self.campo_password.get()

        try:

            acceso = self.usuario.validar(
                usuario, password
            )

        except DatosVaciosError as error:

            logging.warning(
                "Datos vacios en el inicio de sesion."
            )

            messagebox.showwarning(
                "Datos incompletos", str(error)
            )

            return

        except Exception:

            logging.exception(
                "Error inesperado al iniciar sesion."
            )

            messagebox.showerror(
                "Error",
                "Ocurrio un problema al ingresar al sistema."
            )

            return

        else:

            if acceso:

                logging.info(
                    "Inicio de sesion correcto."
                )

                messagebox.showinfo(
                    "Acceso", "Bienvenido a Software FJ."
                )

                self.mostrar_menu()

            else:

                logging.warning(
                    "Intento de acceso denegado."
                )

                messagebox.showerror(
                    "Acceso", "Usuario o contrasena incorrectos."
                )

                self.campo_password.delete(0, tk.END)

        finally:

            logging.info(
                "Finalizo la validacion del usuario."
            )

   # MENU PRINCIPAL

    def mostrar_menu(self):

        self.limpiar_ventana()

        self.ventana.title(
            "Software FJ - Menu principal"
        )
        self.ventana.geometry("550x600")

        self.crear_titulo("MENU PRINCIPAL")

        tk.Label(
            self.ventana,
            text="Sistema de clientes, servicios y reservas",
            font=("Arial", 11)
        ).pack(pady=5)

        botones = [
            ("Gestionar clientes", self.menu_clientes),
            ("Gestionar servicios", self.menu_servicios),
            ("Gestionar reservas", self.menu_reservas),
            ("Consultar reporte general", self.ver_reporte),
            ("Ejecutar pruebas del sistema", self.ver_pruebas),
            ("Cerrar sesion", self.mostrar_login),
            ("Salir", self.ventana.destroy)
        ]

        for texto, comando in botones:

            tk.Button(
                self.ventana,
                text=texto,
                width=32,
                height=2,
                command=comando
            ).pack(pady=7)

    # MODULO DE CLIENTES

    def menu_clientes(self):

        ventana = tk.Toplevel(self.ventana)
        ventana.title("Gestion de clientes")
        ventana.geometry("450x350")

        tk.Label(
            ventana,
            text="GESTION DE CLIENTES",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Button(
            ventana,
            text="Registrar cliente",
            width=25,
            command=self.registrar_cliente
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Consultar clientes",
            width=25,
            command=self.consultar_clientes
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Buscar cliente",
            width=25,
            command=self.consultar_cliente
        ).pack(pady=10)

    def registrar_cliente(self):

        identificacion = self.pedir_dato(
            "Registro", "Ingrese la identificacion:"
        )

        if identificacion is None:
            return

        nombre = self.pedir_dato(
            "Registro", "Ingrese el nombre:"
        )

        if nombre is None:
            return

        correo = self.pedir_dato(
            "Registro", "Ingrese el correo:"
        )

        if correo is None:
            return

        telefono = self.pedir_dato(
            "Registro", "Ingrese el telefono:"
        )

        if telefono is None:
            return

        try:

            cliente = self.sistema.registrar_cliente(
                identificacion, nombre, correo, telefono
            )

        except (DatosVaciosError, ClienteInvalidoError) as error:

            logging.error(
                "Error en registro de cliente: %s", error
            )

            messagebox.showerror(
                "Error de registro", str(error)
            )

        except Exception:

            logging.exception(
                "Error inesperado al registrar cliente."
            )

            messagebox.showerror(
                "Error", "No fue posible registrar el cliente."
            )

        else:

            messagebox.showinfo(
                "Registro correcto",
                f"Cliente {cliente.nombre} registrado correctamente."
            )

        finally:

            logging.info(
                "Finalizo el proceso de registro de cliente."
            )

    def consultar_clientes(self):

        if not self.sistema.clientes:

            messagebox.showinfo(
                "Clientes", "No hay clientes registrados."
            )
            return

        texto = "LISTADO DE CLIENTES\n\n"

        for cliente in self.sistema.clientes:

            texto += (
                f"Identificacion: {cliente.identificacion}\n"
                f"Nombre: {cliente.nombre}\n"
                f"Correo: {cliente.correo}\n"
                f"Telefono: {cliente.telefono}\n"
                "\n"
            )

        self.mostrar_texto(
            "Listado de clientes", texto
        )

    def consultar_cliente(self):

        identificacion = self.pedir_dato(
            "Buscar cliente", "Ingrese la identificacion:"
        )

        if identificacion is None:
            return

        cliente = self.sistema.buscar_cliente(identificacion)

        if cliente:

            self.mostrar_texto(
                "Informacion del cliente",
                cliente.mostrar_informacion()
            )

        else:

            messagebox.showwarning(
                "Busqueda", "No se encontro el cliente."
            )
 # MODULO DE SERVICIOS

    def menu_servicios(self):

        ventana = tk.Toplevel(self.ventana)
        ventana.title("Gestion de servicios")
        ventana.geometry("450x400")

        tk.Label(
            ventana,
            text="GESTION DE SERVICIOS",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Button(
            ventana,
            text="Consultar servicios",
            width=28,
            command=self.consultar_servicios
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Agregar reserva de sala",
            width=28,
            command=lambda: self.agregar_servicio("sala")
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Agregar alquiler de equipo",
            width=28,
            command=lambda: self.agregar_servicio("equipo")
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Agregar asesoria",
            width=28,
            command=lambda: self.agregar_servicio("asesoria")
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Cambiar disponibilidad",
            width=28,
            command=self.cambiar_disponibilidad
        ).pack(pady=10)

    def consultar_servicios(self):

        texto = "LISTADO DE SERVICIOS\n\n"

        for servicio in self.sistema.servicios:

            estado = (
                "Disponible" if servicio.disponible
                else "No disponible"
            )

            texto += (
                f"Codigo: {servicio.codigo}\n"
                f"Nombre: {servicio.nombre}\n"
                f"Tarifa: ${servicio.tarifa:,.2f}\n"
                f"Estado: {estado}\n"
                f"Descripcion: {servicio.describir()}\n"
                "----------------------------------\n"
            )

        self.mostrar_texto(
            "Servicios registrados", texto
        )

    def agregar_servicio(self, tipo):

        codigo = self.pedir_dato(
            "Nuevo servicio", "Ingrese el codigo:"
        )

        if codigo is None:
            return

        nombre = self.pedir_dato(
            "Nuevo servicio", "Ingrese el nombre:"
        )

        if nombre is None:
            return

        tarifa = self.pedir_numero(
            "Nuevo servicio", "Ingrese la tarifa:"
        )

        if tarifa is None:
            return

        try:

            if tipo == "sala":

                capacidad = self.pedir_numero(
                    "Reserva de sala",
                    "Ingrese la capacidad de personas:"
                )

                if capacidad is None:
                    return

                servicio = ReservaSala(
                    codigo, nombre, tarifa, capacidad
                )

            elif tipo == "equipo":

                unidades = self.pedir_numero(
                    "Alquiler de equipo",
                    "Ingrese las unidades disponibles:"
                )

                if unidades is None:
                    return

                servicio = AlquilerEquipo(
                    codigo, nombre, tarifa, unidades
                )

            else:

                especialidad = self.pedir_dato(
                    "Asesoria",
                    "Ingrese la especialidad:"
                )

                if especialidad is None:
                    return

                servicio = Asesoria(
                    codigo, nombre, tarifa, especialidad
                )

            self.sistema.agregar_servicio(servicio)

            messagebox.showinfo(
                "Servicio",
                "El servicio fue agregado correctamente."
            )

        except Exception as error:

            logging.exception(
                "Error al agregar servicio."
            )

            messagebox.showerror(
                "Error", str(error)
            )

    def cambiar_disponibilidad(self):

        codigo = self.pedir_dato(
            "Disponibilidad",
            "Ingrese el codigo del servicio:"
        )

        if codigo is None:
            return

        servicio = self.sistema.buscar_servicio(codigo)

        if servicio is None:

            messagebox.showwarning(
                "Servicio", "No se encontro el servicio."
            )
            return

        servicio.disponible = not servicio.disponible

        estado = (
            "Disponible" if servicio.disponible
            else "No disponible"
        )

        logging.info(
            "Disponibilidad del servicio %s: %s",
            codigo, estado
        )

        messagebox.showinfo(
            "Disponibilidad",
            f"El servicio ahora esta: {estado}"
        )
 # MODULO DE RESERVAS

    def menu_reservas(self):

        ventana = tk.Toplevel(self.ventana)
        ventana.title("Gestion de reservas")
        ventana.geometry("450x400")

        tk.Label(
            ventana,
            text="GESTION DE RESERVAS",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Button(
            ventana,
            text="Crear reserva",
            width=28,
            command=self.crear_reserva
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Consultar reservas",
            width=28,
            command=self.consultar_reservas
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Confirmar reserva",
            width=28,
            command=lambda: self.cambiar_estado_reserva("confirmar")
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Cancelar reserva",
            width=28,
            command=lambda: self.cambiar_estado_reserva("cancelar")
        ).pack(pady=10)

        tk.Button(
            ventana,
            text="Procesar reserva",
            width=28,
            command=lambda: self.cambiar_estado_reserva("procesar")
        ).pack(pady=10)

    def crear_reserva(self):

        codigo = self.pedir_dato(
            "Crear reserva", "Codigo de la reserva:"
        )

        if codigo is None:
            return

        identificacion = self.pedir_dato(
            "Crear reserva",
            "Identificacion del cliente:"
        )

        if identificacion is None:
            return

        codigo_servicio = self.pedir_dato(
            "Crear reserva", "Codigo del servicio:"
        )

        if codigo_servicio is None:
            return

        duracion = self.pedir_numero(
            "Crear reserva",
            "Ingrese la duracion (horas o unidades de servicio):"
        )

        if duracion is None:
            return

        try:

            reserva = self.sistema.crear_reserva(
                codigo,
                identificacion,
                codigo_servicio,
                duracion
            )

            messagebox.showinfo(
                "Reserva creada",
                f"Reserva creada correctamente.\n"
                f"Codigo: {reserva.identificacion}\n"
                f"Costo: ${reserva.costo:,.2f}\n"
                f"Estado: {reserva.estado}"
            )

        except Exception as error:

            logging.exception(
                "Error al crear reserva desde la interfaz."
            )

            messagebox.showerror(
                "Error de reserva", str(error)
            )

    def consultar_reservas(self):

        if not self.sistema.reservas:

            messagebox.showinfo(
                "Reservas", "No hay reservas registradas."
            )
            return

        texto = "LISTADO DE RESERVAS\n\n"

        for reserva in self.sistema.reservas:

            texto += (
                f"Codigo: {reserva.identificacion}\n"
                f"Cliente: {reserva.cliente.nombre}\n"
                f"Servicio: {reserva.servicio.nombre}\n"
                f"Duracion: {reserva.duracion}\n"
                f"Costo: ${reserva.costo:,.2f}\n"
                f"Estado: {reserva.estado}\n"
                "\n"
            )

        self.mostrar_texto(
            "Reservas registradas", texto
        )

    def cambiar_estado_reserva(self, operacion):

        codigo = self.pedir_dato(
            "Gestion de reserva",
            "Ingrese el codigo de la reserva:"
        )

        if codigo is None:
            return

        reserva = self.sistema.buscar_reserva(codigo)

        if reserva is None:

            messagebox.showwarning(
                "Reserva", "No se encontro la reserva."
            )
            return

        try:

            if operacion == "confirmar":
                reserva.confirmar()
                mensaje = "La reserva fue confirmada."

            elif operacion == "cancelar":
                reserva.cancelar()
                mensaje = "La reserva fue cancelada."

            else:
                reserva.procesar()
                mensaje = "La reserva fue procesada."

            messagebox.showinfo(
                "Operacion correcta", mensaje
            )

        except OperacionNoPermitidaError as error:

            logging.warning(
                "Operacion no permitida: %s", error
            )

            messagebox.showwarning(
                "Operacion no permitida", str(error)
            )

        except Exception:

            logging.exception(
                "Error al modificar estado de reserva."
            )

            messagebox.showerror(
                "Error", "No fue posible realizar la operacion."
            )

    # REPORTES Y PRUEBAS

    def ver_reporte(self):

        reporte = self.sistema.generar_reporte()

        self.mostrar_texto(
            "Reporte general Software FJ", reporte
        )

    def ver_pruebas(self):

        resultado = self.sistema.ejecutar_pruebas()

        self.mostrar_texto(
            "Pruebas del sistema", resultado
        )
# INICIAR EL PROGRAMA
if __name__ == "__main__":

    try:

        ventana = tk.Tk()

        aplicacion = AplicacionSoftwareFJ(ventana)

        logging.info(
            "Aplicacion Software FJ iniciada correctamente."
        )

        ventana.mainloop()

    except Exception as error:

        logging.exception(
            "No se pudo iniciar el programa."
        )

        try:
            messagebox.showerror(
                "Error",
                f"No fue posible iniciar el sistema.\n{error}"
            )
        except Exception:
            print("No fue posible iniciar Software FJ.")
