# =============================================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# Empresa: Software FJ
# Curso: Programación 213023 - UNAD
# Tema: Programación Orientada a Objetos + Manejo de Excepciones
# =============================================================================

# Importamos las herramientas que necesitamos
import datetime  # Para manejar fechas y horas
import re        # Para validar formatos (como el email)
from abc import ABC, abstractmethod  # Para crear clases abstractas

# =============================================================================
# SECCIÓN 1: ARCHIVO DE LOGS
# Aquí registramos todos los errores y eventos importantes del sistema
# =============================================================================

ARCHIVO_LOG = "log_softwarefj.txt"  # Nombre del archivo donde se guardan los logs

def registrar_log(tipo, mensaje):
    """
    Función que escribe un evento o error en el archivo de logs.
    tipo: puede ser "ERROR", "INFO", "ADVERTENCIA"
    mensaje: descripción del evento
    """
    try:
        # Obtenemos la fecha y hora actual
        ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Abrimos el archivo en modo 'a' (append = agregar sin borrar lo anterior)
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            # Escribimos una línea con formato: [fecha] TIPO: mensaje
            archivo.write(f"[{ahora}] {tipo}: {mensaje}\n")
    except Exception as e:
        # Si falla el log, lo mostramos en pantalla para no perder el error
        print(f"No se pudo escribir en el log: {e}")


# =============================================================================
# SECCIÓN 2: EXCEPCIONES PERSONALIZADAS
# Creamos nuestros propios tipos de error para el sistema
# =============================================================================

class ClienteInvalidoError(Exception):
    """Error que se lanza cuando los datos de un cliente no son válidos."""
    pass

class ServicioNoDisponibleError(Exception):
    """Error que se lanza cuando un servicio no está disponible."""
    pass

class ReservaInvalidaError(Exception):
    """Error que se lanza cuando una reserva tiene datos incorrectos."""
    pass

class DuracionInvalidaError(Exception):
    """Error que se lanza cuando la duración de una reserva es incorrecta."""
    pass

class DescuentoInvalidoError(Exception):
    """Error que se lanza cuando se aplica un descuento fuera de rango."""
    pass


# =============================================================================
# SECCIÓN 3: CLASE ABSTRACTA BASE
# Toda entidad del sistema hereda de esta clase
# =============================================================================

class EntidadBase(ABC):
    """
    Clase abstracta que representa cualquier entidad del sistema.
    Obliga a las clases hijas a implementar el método 'describir'.
    """

    def __init__(self, identificador):
        # Todo objeto del sistema tiene un identificador único
        self._identificador = identificador  # El _ indica que es un atributo protegido

    @abstractmethod
    def describir(self):
        """
        Método abstracto: cada clase hija DEBE implementar su propia versión.
        """
        pass

    def obtener_id(self):
        """Retorna el identificador de la entidad."""
        return self._identificador


# =============================================================================
# SECCIÓN 4: CLASE CLIENTE
# Representa a un cliente de Software FJ con validaciones estrictas
# =============================================================================

class Cliente(EntidadBase):
    """
    Clase que representa un cliente del sistema.
    Hereda de EntidadBase e implementa encapsulación con validaciones.
    """

    def __init__(self, id_cliente, nombre, email, telefono):
        """
        Constructor del cliente. Valida todos los datos antes de guardarlos.
        id_cliente: número único del cliente
        nombre: nombre completo
        email: correo electrónico válido
        telefono: número de contacto
        """
        super().__init__(id_cliente)  # Llamamos al constructor de EntidadBase

        # Usamos los setters (métodos de asignación) para validar cada dato
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    # --- PROPIEDAD: nombre ---
    @property
    def nombre(self):
        """Getter: retorna el nombre del cliente."""
        return self.__nombre  # __ indica atributo privado (solo accesible desde aquí)

    @nombre.setter
    def nombre(self, valor):
        """Setter: valida que el nombre no esté vacío antes de guardarlo."""
        if not valor or not valor.strip():
            # Si el nombre está vacío, lanzamos nuestra excepción personalizada
            raise ClienteInvalidoError("El nombre del cliente no puede estar vacío.")
        if len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip()  # Guardamos sin espacios al inicio/final

    # --- PROPIEDAD: email ---
    @property
    def email(self):
        """Getter: retorna el email del cliente."""
        return self.__email

    @email.setter
    def email(self, valor):
        """Setter: valida que el email tenga formato correcto."""
        if not valor or not valor.strip():
            raise ClienteInvalidoError("El email no puede estar vacío.")
        # Usamos una expresión regular para validar el formato del email
        patron_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(patron_email, valor.strip()):
            raise ClienteInvalidoError(f"El email '{valor}' no tiene un formato válido.")
        self.__email = valor.strip()

    # --- PROPIEDAD: telefono ---
    @property
    def telefono(self):
        """Getter: retorna el teléfono del cliente."""
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        """Setter: valida que el teléfono tenga solo números y longitud correcta."""
        if not valor:
            raise ClienteInvalidoError("El teléfono no puede estar vacío.")
        # Eliminamos espacios y guiones para validar solo los dígitos
        solo_numeros = str(valor).replace(" ", "").replace("-", "")
        if not solo_numeros.isdigit():
            raise ClienteInvalidoError("El teléfono debe contener solo números.")
        if len(solo_numeros) < 7 or len(solo_numeros) > 15:
            raise ClienteInvalidoError("El teléfono debe tener entre 7 y 15 dígitos.")
        self.__telefono = valor

    def describir(self):
        """Implementación del método abstracto: muestra los datos del cliente."""
        return (f"Cliente ID={self._identificador} | "
                f"Nombre={self.__nombre} | "
                f"Email={self.__email} | "
                f"Tel={self.__telefono}")


# =============================================================================
# SECCIÓN 5: CLASE ABSTRACTA SERVICIO
# Base para todos los tipos de servicio de Software FJ
# =============================================================================

class Servicio(EntidadBase):
    """
    Clase abstracta que representa un servicio de Software FJ.
    Define la estructura común que deben seguir todos los servicios.
    """

    def __init__(self, id_servicio, nombre_servicio, precio_base, disponible=True):
        """
        Constructor base para cualquier servicio.
        precio_base: costo en pesos por hora o unidad
        disponible: indica si el servicio está activo
        """
        super().__init__(id_servicio)
        self._nombre_servicio = nombre_servicio  # Protegido para que hijas accedan
        self._precio_base = precio_base
        self._disponible = disponible

    @abstractmethod
    def calcular_costo(self, duracion):
        """
        Método abstracto: cada servicio calcula su costo de forma diferente.
        duracion: horas o unidades de uso
        """
        pass

    @abstractmethod
    def validar_parametros(self, duracion):
        """
        Método abstracto: cada servicio define sus propias reglas de validación.
        """
        pass

    def esta_disponible(self):
        """Retorna True si el servicio está disponible, False si no."""
        return self._disponible

    def activar(self):
        """Activa el servicio."""
        self._disponible = True

    def desactivar(self):
        """Desactiva el servicio."""
        self._disponible = False

    def describir(self):
        """Descripción básica del servicio."""
        estado = "Disponible" if self._disponible else "No disponible"
        return (f"Servicio ID={self._identificador} | "
                f"Nombre={self._nombre_servicio} | "
                f"Precio base=${self._precio_base:,.0f} | "
                f"Estado={estado}")


# =============================================================================
# SECCIÓN 6: TRES SERVICIOS ESPECIALIZADOS (heredan de Servicio)
# =============================================================================

# --- Servicio 1: Reserva de Salas ---
class ReservaSalas(Servicio):
    """
    Servicio para reservar salas de reuniones o conferencias.
    El costo se calcula por hora con posibilidad de descuento por cantidad.
    """

    def __init__(self, id_servicio, capacidad_personas):
        """
        capacidad_personas: cuántas personas caben en la sala
        """
        super().__init__(id_servicio, "Reserva de Sala", precio_base=80000)
        self.__capacidad = capacidad_personas  # Privado: solo accesible desde esta clase

    def validar_parametros(self, duracion):
        """Valida que la duración sea entre 1 y 12 horas."""
        if not isinstance(duracion, (int, float)):
            raise DuracionInvalidaError("La duración debe ser un número.")
        if duracion < 1:
            raise DuracionInvalidaError("La duración mínima para sala es 1 hora.")
        if duracion > 12:
            raise DuracionInvalidaError("La duración máxima para sala es 12 horas.")

    def calcular_costo(self, duracion, descuento=0):
        """
        Calcula el costo de la reserva de sala.
        duracion: número de horas
        descuento: porcentaje de descuento (0 a 50)
        Método sobrecargado: acepta parámetro opcional 'descuento'
        """
        # Primero validamos los parámetros
        self.validar_parametros(duracion)

        # Validamos el descuento
        if descuento < 0 or descuento > 50:
            raise DescuentoInvalidoError(
                f"El descuento debe estar entre 0% y 50%. Se recibió: {descuento}%"
            )

        # Calculamos el costo base
        costo = self._precio_base * duracion

        # Aplicamos descuento si hay
        if descuento > 0:
            costo = costo * (1 - descuento / 100)

        return round(costo, 2)  # Redondeamos a 2 decimales

    def calcular_costo_con_impuesto(self, duracion, impuesto_porcentaje=19):
        """
        Versión del cálculo con impuesto incluido (IVA).
        Método sobrecargado con parámetro adicional de impuesto.
        """
        costo_base = self.calcular_costo(duracion)
        impuesto = costo_base * (impuesto_porcentaje / 100)
        return round(costo_base + impuesto, 2)

    def describir(self):
        """Descripción detallada de la sala."""
        base = super().describir()  # Llamamos al describir del padre
        return f"{base} | Capacidad={self.__capacidad} personas"


# --- Servicio 2: Alquiler de Equipos ---
class AlquilerEquipos(Servicio):
    """
    Servicio para alquilar equipos tecnológicos (computadores, proyectores, etc.)
    El costo varía según el tipo de equipo y la cantidad.
    """

    TIPOS_VALIDOS = ["computador", "proyector", "tablet", "camara"]  # Lista permitida

    def __init__(self, id_servicio, tipo_equipo, cantidad_disponible):
        """
        tipo_equipo: tipo de equipo a alquilar
        cantidad_disponible: cuántas unidades hay en stock
        """
        # Validamos el tipo de equipo al momento de crear el servicio
        if tipo_equipo.lower() not in self.TIPOS_VALIDOS:
            raise ServicioNoDisponibleError(
                f"Tipo de equipo '{tipo_equipo}' no válido. "
                f"Opciones: {self.TIPOS_VALIDOS}"
            )

        super().__init__(id_servicio, f"Alquiler de {tipo_equipo}", precio_base=45000)
        self.__tipo_equipo = tipo_equipo.lower()
        self.__cantidad_disponible = cantidad_disponible

    def validar_parametros(self, duracion):
        """Valida que la duración sea entre 1 y 30 días."""
        if not isinstance(duracion, (int, float)):
            raise DuracionInvalidaError("La duración debe ser un número.")
        if duracion < 1:
            raise DuracionInvalidaError("El alquiler mínimo es 1 día.")
        if duracion > 30:
            raise DuracionInvalidaError("El alquiler máximo es 30 días.")

    def calcular_costo(self, duracion, cantidad=1):
        """
        Calcula el costo del alquiler.
        duracion: número de días
        cantidad: número de equipos a alquilar (parámetro opcional)
        Método sobrecargado: acepta cantidad como parámetro adicional
        """
        self.validar_parametros(duracion)

        if cantidad < 1:
            raise ReservaInvalidaError("Debe alquilar al menos 1 equipo.")
        if cantidad > self.__cantidad_disponible:
            raise ServicioNoDisponibleError(
                f"Solo hay {self.__cantidad_disponible} unidades disponibles. "
                f"Se solicitaron: {cantidad}"
            )

        costo = self._precio_base * duracion * cantidad
        return round(costo, 2)

    def calcular_costo_con_impuesto(self, duracion, cantidad=1, impuesto_porcentaje=19):
        """Calcula el costo total incluyendo IVA."""
        costo_base = self.calcular_costo(duracion, cantidad)
        impuesto = costo_base * (impuesto_porcentaje / 100)
        return round(costo_base + impuesto, 2)

    def describir(self):
        """Descripción detallada del equipo."""
        base = super().describir()
        return f"{base} | Equipo={self.__tipo_equipo} | Stock={self.__cantidad_disponible}"


# --- Servicio 3: Asesoría Especializada ---
class AsesoriaEspecializada(Servicio):
    """
    Servicio de asesoría técnica o profesional por horas.
    El costo varía según el nivel del asesor.
    """

    NIVELES_VALIDOS = {
        "junior": 1.0,    # Factor multiplicador según nivel
        "senior": 1.5,
        "experto": 2.0
    }

    def __init__(self, id_servicio, area_especialidad, nivel_asesor):
        """
        area_especialidad: ej. "Ciberseguridad", "Desarrollo Web"
        nivel_asesor: "junior", "senior" o "experto"
        """
        if nivel_asesor.lower() not in self.NIVELES_VALIDOS:
            raise ServicioNoDisponibleError(
                f"Nivel '{nivel_asesor}' no válido. "
                f"Opciones: {list(self.NIVELES_VALIDOS.keys())}"
            )

        super().__init__(id_servicio, f"Asesoría en {area_especialidad}", precio_base=120000)
        self.__area = area_especialidad
        self.__nivel = nivel_asesor.lower()
        self.__factor = self.NIVELES_VALIDOS[self.__nivel]  # Factor de precio según nivel

    def validar_parametros(self, duracion):
        """Valida que la duración sea entre 1 y 8 horas."""
        if not isinstance(duracion, (int, float)):
            raise DuracionInvalidaError("La duración debe ser un número.")
        if duracion < 1:
            raise DuracionInvalidaError("La asesoría mínima es 1 hora.")
        if duracion > 8:
            raise DuracionInvalidaError("La asesoría máxima es 8 horas por sesión.")

    def calcular_costo(self, duracion, incluir_materiales=False):
        """
        Calcula el costo de la asesoría.
        duracion: número de horas
        incluir_materiales: True si se cobran materiales adicionales (parámetro opcional)
        Método sobrecargado con parámetro booleano adicional
        """
        self.validar_parametros(duracion)

        # El precio varía según el nivel del asesor
        costo = self._precio_base * self.__factor * duracion

        # Si incluye materiales, se agrega un 10% extra
        if incluir_materiales:
            costo = costo * 1.10

        return round(costo, 2)

    def calcular_costo_con_impuesto(self, duracion, incluir_materiales=False, impuesto_porcentaje=19):
        """Calcula el costo total con IVA."""
        costo_base = self.calcular_costo(duracion, incluir_materiales)
        impuesto = costo_base * (impuesto_porcentaje / 100)
        return round(costo_base + impuesto, 2)

    def describir(self):
        """Descripción detallada de la asesoría."""
        base = super().describir()
        return f"{base} | Área={self.__area} | Nivel={self.__nivel}"


# =============================================================================
# SECCIÓN 7: CLASE RESERVA
# Une un cliente con un servicio y gestiona el estado de la reserva
# =============================================================================

class Reserva(EntidadBase):
    """
    Clase que representa una reserva dentro del sistema.
    Integra: cliente + servicio + duración + estado
    """

    # Estados posibles de una reserva
    ESTADO_PENDIENTE   = "PENDIENTE"
    ESTADO_CONFIRMADA  = "CONFIRMADA"
    ESTADO_CANCELADA   = "CANCELADA"
    ESTADO_COMPLETADA  = "COMPLETADA"

    def __init__(self, id_reserva, cliente, servicio, duracion):
        """
        id_reserva: número único de la reserva
        cliente: objeto de tipo Cliente
        servicio: objeto de tipo Servicio (o subclase)
        duracion: horas o días según el tipo de servicio
        """
        super().__init__(id_reserva)

        # Validamos que el cliente sea un objeto válido
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente no es un objeto válido de tipo Cliente.")

        # Validamos que el servicio sea válido
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio no es un objeto válido de tipo Servicio.")

        # Verificamos disponibilidad del servicio
        if not servicio.esta_disponible():
            raise ServicioNoDisponibleError(
                f"El servicio '{servicio._nombre_servicio}' no está disponible actualmente."
            )

        self.__cliente = cliente    # Privado: encapsulamos el cliente
        self.__servicio = servicio  # Privado: encapsulamos el servicio
        self.__duracion = duracion
        self.__estado = self.ESTADO_PENDIENTE  # Toda reserva inicia como PENDIENTE
        self.__costo_total = 0
        self.__fecha_creacion = datetime.datetime.now()  # Guardamos la fecha de creación

    def confirmar(self):
        """
        Confirma la reserva: calcula el costo y cambia el estado.
        Usa try/except/else para mostrar éxito solo si no hubo error.
        """
        try:
            # Intentamos calcular el costo
            self.__costo_total = self.__servicio.calcular_costo(self.__duracion)

        except (DuracionInvalidaError, ServicioNoDisponibleError, DescuentoInvalidoError) as e:
            # Si hay error en el cálculo, lo registramos y relanzamos
            mensaje = f"Error al confirmar reserva ID={self._identificador}: {e}"
            registrar_log("ERROR", mensaje)
            # Encadenamos la excepción para dar más contexto
            raise ReservaInvalidaError(mensaje) from e

        except Exception as e:
            # Capturamos cualquier otro error inesperado
            mensaje = f"Error inesperado al confirmar reserva ID={self._identificador}: {e}"
            registrar_log("ERROR", mensaje)
            raise

        else:
            # Este bloque SOLO se ejecuta si NO hubo excepción
            self.__estado = self.ESTADO_CONFIRMADA
            mensaje_ok = (f"Reserva ID={self._identificador} CONFIRMADA. "
                         f"Costo=${self.__costo_total:,.0f}")
            registrar_log("INFO", mensaje_ok)
            print(f"  ✔ {mensaje_ok}")

        finally:
            # Este bloque se ejecuta SIEMPRE (haya o no error)
            print(f"  [LOG] Proceso de confirmación finalizado para reserva ID={self._identificador}")

    def cancelar(self, motivo="Sin motivo especificado"):
        """
        Cancela la reserva si está en estado PENDIENTE o CONFIRMADA.
        motivo: razón de la cancelación
        """
        try:
            if self.__estado == self.ESTADO_CANCELADA:
                raise ReservaInvalidaError(
                    f"La reserva ID={self._identificador} ya estaba cancelada."
                )
            if self.__estado == self.ESTADO_COMPLETADA:
                raise ReservaInvalidaError(
                    f"No se puede cancelar una reserva completada (ID={self._identificador})."
                )

        except ReservaInvalidaError as e:
            registrar_log("ADVERTENCIA", str(e))
            raise  # Relanzamos para que el llamador también la reciba

        else:
            # Solo llegamos aquí si no hubo error
            self.__estado = self.ESTADO_CANCELADA
            mensaje = f"Reserva ID={self._identificador} CANCELADA. Motivo: {motivo}"
            registrar_log("INFO", mensaje)
            print(f"  ✘ {mensaje}")

        finally:
            print(f"  [LOG] Proceso de cancelación finalizado para reserva ID={self._identificador}")

    def completar(self):
        """Marca la reserva como completada (servicio ya prestado)."""
        if self.__estado != self.ESTADO_CONFIRMADA:
            raise ReservaInvalidaError(
                f"Solo se pueden completar reservas CONFIRMADAS. "
                f"Estado actual: {self.__estado}"
            )
        self.__estado = self.ESTADO_COMPLETADA
        registrar_log("INFO", f"Reserva ID={self._identificador} COMPLETADA.")
        print(f"  ★ Reserva ID={self._identificador} marcada como COMPLETADA.")

    def describir(self):
        """Descripción completa de la reserva."""
        return (f"Reserva ID={self._identificador} | "
                f"Cliente={self.__cliente.nombre} | "
                f"Servicio={self.__servicio._nombre_servicio} | "
                f"Duración={self.__duracion} | "
                f"Estado={self.__estado} | "
                f"Costo=${self.__costo_total:,.0f}")

    # Getters para acceder a datos internos de forma controlada
    def obtener_estado(self):
        return self.__estado

    def obtener_costo(self):
        return self.__costo_total


# =============================================================================
# SECCIÓN 8: SISTEMA PRINCIPAL
# Clase que administra todo: listas de clientes, servicios y reservas
# =============================================================================

class SistemaGestion:
    """
    Clase principal que administra el sistema completo de Software FJ.
    Mantiene listas internas de clientes, servicios y reservas.
    """

    def __init__(self):
        """Inicializa las listas vacías del sistema."""
        self.__clientes  = []   # Lista de objetos Cliente
        self.__servicios = []   # Lista de objetos Servicio
        self.__reservas  = []   # Lista de objetos Reserva
        registrar_log("INFO", "Sistema Software FJ iniciado correctamente.")
        print("=" * 65)
        print("   SISTEMA DE GESTIÓN SOFTWARE FJ - Iniciando...")
        print("=" * 65)

    def registrar_cliente(self, id_cliente, nombre, email, telefono):
        """
        Registra un nuevo cliente en el sistema.
        Usa try/except/finally para manejo seguro de errores.
        """
        print(f"\n→ Registrando cliente: {nombre}")
        try:
            # Intentamos crear el cliente (puede lanzar ClienteInvalidoError)
            nuevo_cliente = Cliente(id_cliente, nombre, email, telefono)
            self.__clientes.append(nuevo_cliente)  # Lo agregamos a la lista

        except ClienteInvalidoError as e:
            # Error específico de datos de cliente inválidos
            registrar_log("ERROR", f"Cliente inválido (ID={id_cliente}): {e}")
            print(f"  ✖ Error de cliente: {e}")

        except Exception as e:
            # Cualquier otro error inesperado
            registrar_log("ERROR", f"Error inesperado al registrar cliente: {e}")
            print(f"  ✖ Error inesperado: {e}")

        else:
            # Solo si NO hubo error
            registrar_log("INFO", f"Cliente registrado: {nuevo_cliente.describir()}")
            print(f"  ✔ Cliente registrado exitosamente.")
            print(f"     {nuevo_cliente.describir()}")

        finally:
            # Siempre se ejecuta
            print(f"  [LOG] Proceso de registro de cliente finalizado.")

    def agregar_servicio(self, servicio):
        """
        Agrega un servicio al catálogo del sistema.
        El objeto servicio ya viene creado desde afuera.
        """
        print(f"\n→ Agregando servicio: {servicio._nombre_servicio}")
        try:
            if not isinstance(servicio, Servicio):
                raise ServicioNoDisponibleError("El objeto no es un servicio válido.")
            self.__servicios.append(servicio)

        except ServicioNoDisponibleError as e:
            registrar_log("ERROR", f"Servicio inválido: {e}")
            print(f"  ✖ Error: {e}")

        else:
            registrar_log("INFO", f"Servicio agregado: {servicio.describir()}")
            print(f"  ✔ Servicio agregado exitosamente.")
            print(f"     {servicio.describir()}")

        finally:
            print(f"  [LOG] Proceso de agregar servicio finalizado.")

    def crear_reserva(self, id_reserva, id_cliente, id_servicio, duracion):
        """
        Crea una nueva reserva buscando el cliente y servicio por su ID.
        """
        print(f"\n→ Creando reserva ID={id_reserva}...")
        try:
            # Buscamos el cliente en la lista
            cliente = next((c for c in self.__clientes
                           if c.obtener_id() == id_cliente), None)
            if not cliente:
                raise ReservaInvalidaError(
                    f"No se encontró cliente con ID={id_cliente}."
                )

            # Buscamos el servicio en la lista
            servicio = next((s for s in self.__servicios
                            if s.obtener_id() == id_servicio), None)
            if not servicio:
                raise ReservaInvalidaError(
                    f"No se encontró servicio con ID={id_servicio}."
                )

            # Creamos la reserva
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion)
            self.__reservas.append(nueva_reserva)

        except (ReservaInvalidaError, ServicioNoDisponibleError) as e:
            registrar_log("ERROR", f"Error al crear reserva ID={id_reserva}: {e}")
            print(f"  ✖ Error: {e}")
            return None  # Retornamos None para indicar fallo

        except Exception as e:
            registrar_log("ERROR", f"Error inesperado en reserva ID={id_reserva}: {e}")
            print(f"  ✖ Error inesperado: {e}")
            return None

        else:
            registrar_log("INFO", f"Reserva ID={id_reserva} creada en estado PENDIENTE.")
            print(f"  ✔ Reserva creada en estado PENDIENTE.")
            return nueva_reserva  # Retornamos la reserva creada

        finally:
            print(f"  [LOG] Proceso de creación de reserva finalizado.")

    def confirmar_reserva(self, id_reserva):
        """Busca una reserva por ID y la confirma."""
        print(f"\n→ Confirmando reserva ID={id_reserva}...")
        try:
            reserva = next((r for r in self.__reservas
                           if r.obtener_id() == id_reserva), None)
            if not reserva:
                raise ReservaInvalidaError(
                    f"No existe reserva con ID={id_reserva}."
                )
            reserva.confirmar()

        except ReservaInvalidaError as e:
            registrar_log("ERROR", str(e))
            print(f"  ✖ Error: {e}")

    def cancelar_reserva(self, id_reserva, motivo="Sin motivo"):
        """Busca una reserva por ID y la cancela."""
        print(f"\n→ Cancelando reserva ID={id_reserva}...")
        try:
            reserva = next((r for r in self.__reservas
                           if r.obtener_id() == id_reserva), None)
            if not reserva:
                raise ReservaInvalidaError(
                    f"No existe reserva con ID={id_reserva}."
                )
            reserva.cancelar(motivo)

        except ReservaInvalidaError as e:
            registrar_log("ERROR", str(e))
            print(f"  ✖ Error: {e}")

    def mostrar_resumen(self):
        """Muestra un resumen completo del estado del sistema."""
        print("\n" + "=" * 65)
        print("   RESUMEN DEL SISTEMA SOFTWARE FJ")
        print("=" * 65)

        print(f"\n📋 CLIENTES REGISTRADOS ({len(self.__clientes)}):")
        for c in self.__clientes:
            print(f"   • {c.describir()}")

        print(f"\n🛠️  SERVICIOS DISPONIBLES ({len(self.__servicios)}):")
        for s in self.__servicios:
            print(f"   • {s.describir()}")

        print(f"\n📅 RESERVAS ({len(self.__reservas)}):")
        for r in self.__reservas:
            print(f"   • {r.describir()}")

        print("\n" + "=" * 65)


# =============================================================================
# SECCIÓN 9: SIMULACIÓN DE 10 OPERACIONES
# Aquí demostramos que el sistema funciona con casos válidos e inválidos
# =============================================================================

def ejecutar_simulacion():
    """
    Simula 10 operaciones del sistema, incluyendo casos válidos e inválidos.
    El sistema continúa funcionando aunque ocurran errores.
    """

    # Creamos el sistema
    sistema = SistemaGestion()

    print("\n" + "╔" + "═"*63 + "╗")
    print("║" + " INICIO DE SIMULACIÓN - 10 OPERACIONES ".center(63) + "║")
    print("╚" + "═"*63 + "╝")

    # ------------------------------------------------------------------
    # OPERACIÓN 1: Registro de cliente VÁLIDO
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 1】 Registrar cliente válido")
    sistema.registrar_cliente(1, "Ana García", "ana.garcia@email.com", "3001234567")

    # ------------------------------------------------------------------
    # OPERACIÓN 2: Registro de cliente INVÁLIDO (email malo)
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 2】 Registrar cliente con email inválido")
    sistema.registrar_cliente(2, "Juan Pérez", "correo_sin_arroba", "3009876543")

    # ------------------------------------------------------------------
    # OPERACIÓN 3: Registro de cliente INVÁLIDO (nombre vacío)
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 3】 Registrar cliente con nombre vacío")
    sistema.registrar_cliente(3, "", "maria@email.com", "3101112233")

    # ------------------------------------------------------------------
    # OPERACIÓN 4: Registro de cliente VÁLIDO (segundo cliente)
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 4】 Registrar segundo cliente válido")
    sistema.registrar_cliente(4, "Carlos Ruiz", "carlos.ruiz@empresa.com", "3154445566")

    # ------------------------------------------------------------------
    # OPERACIÓN 5: Crear servicios (sala, equipo, asesoría)
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 5】 Crear servicios del catálogo")

    try:
        sala1 = ReservaSalas(id_servicio=101, capacidad_personas=10)
        sistema.agregar_servicio(sala1)
    except Exception as e:
        registrar_log("ERROR", f"Error creando sala: {e}")
        print(f"  ✖ No se pudo crear sala: {e}")

    try:
        equipo1 = AlquilerEquipos(id_servicio=102, tipo_equipo="proyector",
                                   cantidad_disponible=5)
        sistema.agregar_servicio(equipo1)
    except Exception as e:
        registrar_log("ERROR", f"Error creando equipo: {e}")
        print(f"  ✖ No se pudo crear equipo: {e}")

    try:
        asesoria1 = AsesoriaEspecializada(id_servicio=103,
                                           area_especialidad="Ciberseguridad",
                                           nivel_asesor="senior")
        sistema.agregar_servicio(asesoria1)
    except Exception as e:
        registrar_log("ERROR", f"Error creando asesoría: {e}")
        print(f"  ✖ No se pudo crear asesoría: {e}")

    # ------------------------------------------------------------------
    # OPERACIÓN 6: Crear servicio INVÁLIDO (tipo de equipo no existe)
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 6】 Crear equipo con tipo inválido")
    try:
        equipo_malo = AlquilerEquipos(id_servicio=104,
                                      tipo_equipo="dron",  # Tipo no permitido
                                      cantidad_disponible=2)
        sistema.agregar_servicio(equipo_malo)
    except ServicioNoDisponibleError as e:
        registrar_log("ERROR", f"Tipo de equipo inválido: {e}")
        print(f"  ✖ Error esperado capturado: {e}")

    # ------------------------------------------------------------------
    # OPERACIÓN 7: Reserva VÁLIDA (cliente 1 reserva sala)
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 7】 Crear y confirmar reserva válida")
    reserva_ok = sistema.crear_reserva(
        id_reserva=1001,
        id_cliente=1,      # Ana García
        id_servicio=101,   # Sala de reuniones
        duracion=3         # 3 horas
    )
    if reserva_ok:
        sistema.confirmar_reserva(1001)

    # ------------------------------------------------------------------
    # OPERACIÓN 8: Reserva con duración INVÁLIDA (sala máx 12 horas)
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 8】 Crear reserva con duración inválida")
    reserva_mala = sistema.crear_reserva(
        id_reserva=1002,
        id_cliente=4,      # Carlos Ruiz
        id_servicio=101,   # Sala de reuniones
        duracion=20        # 20 horas: excede el límite de 12
    )
    if reserva_mala:
        sistema.confirmar_reserva(1002)  # Fallará al confirmar

    # ------------------------------------------------------------------
    # OPERACIÓN 9: Cancelar una reserva existente
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 9】 Cancelar reserva existente")
    sistema.cancelar_reserva(1001, motivo="Cliente solicitó cambio de fecha")

    # Intentar cancelar de nuevo (ya está cancelada → debe dar error controlado)
    print("\n   → Intentar cancelar la misma reserva nuevamente:")
    sistema.cancelar_reserva(1001, motivo="Segundo intento")

    # ------------------------------------------------------------------
    # OPERACIÓN 10: Reserva VÁLIDA de asesoría con costo con impuesto
    # ------------------------------------------------------------------
    print("\n【OPERACIÓN 10】 Reservar asesoría y calcular costo con IVA")
    reserva_asesoria = sistema.crear_reserva(
        id_reserva=1003,
        id_cliente=4,      # Carlos Ruiz
        id_servicio=103,   # Asesoría en Ciberseguridad
        duracion=2         # 2 horas
    )
    if reserva_asesoria:
        sistema.confirmar_reserva(1003)

        # Calculamos también el costo con IVA de forma directa
        try:
            costo_iva = asesoria1.calcular_costo_con_impuesto(
                duracion=2,
                incluir_materiales=True,
                impuesto_porcentaje=19
            )
            print(f"\n  💰 Costo con materiales + IVA 19%: ${costo_iva:,.0f}")
            registrar_log("INFO", f"Costo asesoría con IVA calculado: ${costo_iva:,.0f}")
        except Exception as e:
            registrar_log("ERROR", f"Error calculando costo con IVA: {e}")
            print(f"  ✖ Error en cálculo: {e}")

    # ------------------------------------------------------------------
    # RESUMEN FINAL
    # ------------------------------------------------------------------
    sistema.mostrar_resumen()
    print(f"\n📁 Todos los eventos y errores fueron guardados en: '{ARCHIVO_LOG}'")
    print("\n✅ Simulación completada. El sistema se mantuvo estable ante todos los errores.\n")


# =============================================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# =============================================================================

if __name__ == "__main__":
    # Este bloque solo se ejecuta cuando corres el archivo directamente
    ejecutar_simulacion()
