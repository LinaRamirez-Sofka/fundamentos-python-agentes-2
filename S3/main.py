# 🛠️ Taller Semana 3: Forjando las Herramientas (Refactorización y Blindaje)
# Lina María Ramírez

from datetime import date, datetime

type UserInfo = dict[str, str]
type Credentials = dict[str, UserInfo]
type Recuerdo = dict[str, str]
type MemoriaAgente = list[Recuerdo]


# Metodo para contar letras, vocales y consonantes de una palabara
def count_word(word: str) -> str:
    """
    Cuenta e imprime el número total de letras, vocales y consonantes en la
    palabra proporcionada. El resultado se muestra en la consola.
    """
    tot_letter = len(word)
    tot_vowels = 0
    tot_consts = 0

    for p in word:
        # valida si la letra es una vocal, de lo contrario es una consonante
        if p in "aeiou":
            tot_vowels += 1
        else:
            tot_consts += 1
    # Resultados del conteo
    print(f"\nPalabra ingresada: {word}")
    print(f"Total letras: {tot_letter}")
    print(f"Total vocales: {tot_vowels}")
    print(f"Total constonantes: {tot_consts}")
    return f"La palabra ingresada fue {word} con {tot_letter} letras, {tot_vowels} vocales y {tot_consts} constantes"


# Metodo para ejecutar el comando "fecha_hoy"
def get_todays_date(user_info: UserInfo) -> str:
    """
    Muestra la fecha actual en formato dd/mm/yyyy si el usuario conectado tiene
    el rol de administrador; de lo contrario, imprime un mensaje de acceso denegado.
    """
    message = ""
    # Valida el rol del usuario, solo si es admin puede saber la fecha de hoy
    if user_info["rol"] == "admin":
        today = date.today()
        # Se formatea la fecha a formato mas convencional de día/mes/año
        today_formatted = today.strftime("%d/%m/%Y")
        message = f"La fecha de hoy es {today_formatted}"
        print(message)
    else:
        message = "Este comando requiere privilegios de administrador."
        print("[Acceso Denegado]" + message)
    return message


# Metodo para validar la contraseña
def validate_pass(password: str, logged_user: str) -> str:
    """
    Valida una contraseña verificando que tenga al menos 8 caracteres y que no
    sea igual al nombre de usuario.
    Imprime los resultados de la validación en la consola.
    """
    message = ""
    valid_password = password.strip()
    # Valida la longitudo de la contraseña sin considerar espacios
    is_length_valid = len(valid_password) >= 8
    # Valida si la contraseña es igual al nombre de usuario
    is_equal_to_user_name = valid_password == logged_user

    # Si incumple las dos validaciones, se indica con mensaje al usuario
    if not is_length_valid and is_equal_to_user_name:
        message = """
    La contraseña no cumple con las validaciones:
      - La longitud no es de minimo 8 carácteres
      - La contraseña es igual al nombre de usuario
        """
    # Si incumple solo con la validacion de longitud minima
    elif not is_length_valid:
        message = "La contraseña no cumple con la longitud mínima de 8 caracteres."
    # Si incumple solo con la validacion de que no sea ingual al usuario
    elif is_equal_to_user_name:
        message = "La contraseña no puede ser igual al nombre de usuario."
    # Si cumple con la longitud y no es igual al nombre de usuario, se considera exitosa
    else:
        message = "La nueva contraseña cumple con las validaciones"
    print(message)
    return message


# Metodo que gestiona las operaciones de la calculadora
def handle_calculator_operations(
    first_number: str, operator: str, second_number: str
) -> str:
    """
    Gestiona operaciones básicas de calculadora (+, -, *, /) en dos números proporcionados
    como cadenas.
    """
    first_number_float = float(first_number)
    second_number_float = float(second_number)
    result: float = 0.0

    match operator:
        case "+":
            result = first_number_float + second_number_float
        case "-":
            result = first_number_float - second_number_float
        case "*":
            result = first_number_float * second_number_float
        case "/":
            if second_number_float == 0:
                message = "Para el operador '/' el segundo numero no puede ser 0"
                print(message)
                return message
            result = first_number_float / second_number_float
        case _:
            message = f"El operador {operator} no es válido."
            print(message)
            return message

    message = f"La operación {first_number}{operator}{second_number} da como resultado {result}"
    print(message)
    return message


# Metodo para gestionar las acciones relacionadas con el historial
def gestionar_historial_all(history_records: MemoriaAgente) -> str:
    """Construye y devuelve el historial completo del chat."""
    return_message = "[PseudoAgente] Historial completo:\n"
    for entry in history_records:
        return_message += f"{entry['timestamp']} | Command: {entry['cmd']} | Rol: {entry['rol']} | Autor: {entry['author']} | Mensaje: {entry['description']}\n"
    return return_message


def gestionar_historial_clear(history_records: MemoriaAgente) -> str:
    """Borra el historial y devuelve el mensaje de confirmación."""
    history_records.clear()
    return "[PseudoAgente] Borrando el historial de la memoria del pseudoagente"


def gestionar_historial_busqueda(history_records: MemoriaAgente) -> str:
    """Busca una palabra clave en el historial y devuelve coincidencias."""
    return_message = "Se ha solicitado encontrar una palabra en el historial: "
    word_to_search = input("\nIngresa la palabra clave a buscar: ")
    # Lista de logs cuya descripcion contiene la palabra a buscar
    conincidences = []

    # Antes de la busqueda se ajusta la palabra a buscar a minuscula y se eliminan espacios finales
    word_processed = word_to_search.strip().lower()

    for log in history_records:
        # Antes de la busqueda se ajusta la descripción a minuscula y se eliminan espacios finales
        description_processed = log["description"].strip().lower()
        # Usando el comando 'in' se identifica si la palabra está en la descripcion
        if word_processed in description_processed:
            conincidences.append(log)

    if len(conincidences) == 0:
        return_message += "No encontré registros que coincidan con esa palabra."
    else:
        number_of_coincidences = len(conincidences)
        return_message += f"Se encontraron {number_of_coincidences} registros de la palabra '{word_to_search}' en el historial"
        for coincidence in conincidences:
            return_message += f"\n Autor: {coincidence['author']} | Mensaje: {coincidence['description']}"

    return return_message


def gestionar_historial(user_input_tokens: list[str], history_records: MemoriaAgente) -> str:
    """
    Gestiona las operaciones del historial de chat: muestra todas las entradas del historial,
    borra el historial, o busca una palabra clave específica en las descripciones del historial.
    """
    # El comando debe ser dos palabras separadas por espacion y la segunda debe ser all
    if len(user_input_tokens) == 2 and "all" == user_input_tokens[1]:
        return gestionar_historial_all(history_records)
    # El comando debe ser dos palabras separadas por espacion y la segunda debe ser all
    elif len(user_input_tokens) == 2 and "clear" == user_input_tokens[1]:
        return gestionar_historial_clear(history_records)
    # El comando debe coincidir exactamente con historial
    elif len(user_input_tokens) == 1 and "historial" == user_input_tokens[0]:
        return gestionar_historial_busqueda(history_records)
    else:
        return "Comando de historial no válido."


def create_log_entry(
    user_data: UserInfo, author_name: str, log_description: str, command: str
) -> Recuerdo:
    """
    Crea un diccionario de entrada de registro con marca de tiempo, comando, autor, rol y descripción.
    Se utiliza para registrar acciones del usuario en el historial de chat.
    """
    return {
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "cmd": command,
        "author": author_name,
        "rol": user_data["rol"],
        "description": log_description,
    }


print("\n-----------------Iniciando el pseudoagente estilo consola-----------------\n")

ACTIVE_SYSTEM = False
LOGIN_ATTEMPTS = 0
LOGIN_SUCCESS = False
MAX_ATTEMPTS = 3

user_credentials: Credentials = {
    "administrador": {"password": "admin_pass", "rol": "admin"},
    "invitado": {"password": "user_pass", "rol": "guest"},
}
logged_user_data: UserInfo = {}
user_input: str = ""

# Historial de chats con marca de tiempo, comando usado, rol, descripcion
chat_history: MemoriaAgente = [
    {
        "timestamp": "21-03-2026 21:06:16",
        "cmd": "ping",
        "author": "admin",
        "rol": "admin",
        "description": "Se envió un ping y se devuelve un pong",
    }
]

# Bloque de autenticación
# Mientras el login no sea exitoso se consultara al usuario por el nombre y contraseña
while not LOGIN_SUCCESS:
    # Sin embargo, si el numero de intentos alcanza el máximo, el sistema se cierra y con break salimos del la estructura while
    if LOGIN_ATTEMPTS == MAX_ATTEMPTS:
        print("[Alerta] Usuario bloqueado. Cerrando sistema.")
        break

    user_input = input("\nEscriba su usuario: ").strip()
    pass_input = input("Digite su contraseña: ").strip()
    # Cada vez que el usuario digite las credenciales se cuenta como un intento de login
    LOGIN_ATTEMPTS += 1
    IS_CREDENTIAL_VALID = False

    # Comprueba que el usuario esta registrado en el diccionario evita un key error si no existe la llave con el nombre del usuario
    if user_input in user_credentials:
        logged_user_data = user_credentials[user_input]
        # La contraseña se encuentra almacenada en el value de la key "password" para el diccionario asociado al usuario
        real_pass = logged_user_data["password"]
        IS_CREDENTIAL_VALID = real_pass == pass_input

    # Si las credenciales son validas, es decir, el usuario esta registrado en el diccionario y la contraseña ingresada coincide con la registrada
    # Se define que el usuario esta loggeado y se activa el sistema del agente
    if IS_CREDENTIAL_VALID:
        LOGIN_SUCCESS = True
        ACTIVE_SYSTEM = True
        print(f"Bienvenido {user_input}. Despertando al agente.\n")
    # De lo contrario se da mensaje informativo y se reptie el bucle
    else:
        print(
            f"\n🚫 Usuario o contraseña incorrecto. Inteno No. {LOGIN_ATTEMPTS} de {MAX_ATTEMPTS}"
        )


# Bloque menu de control pseudoagente
# Estructura de control while que indica el estado de la sesión del pseudoagente y presenta el menú de acciones posibles a ejecutar
# El sistema solo se activa si las credenciales de acceso son validas
while ACTIVE_SYSTEM:
    MESSAGE: str = ""

    cmd = input("\nPseudoAgente>: ").lower().strip()

    if cmd == "salir":
        print("Finalizando la sesión")
        MESSAGE = "Se ha solicitado terminar la sesión"
        ACTIVE_SYSTEM = False
    elif cmd == "ping":
        print("pong")
        MESSAGE = "Se envió un ping y se devuelve un pong"
    elif cmd == "contar":
        input_word = input("Ingrese una palabra: ").lower()
        MESSAGE = count_word(input_word)
    elif cmd == "fecha_hoy":
        MESSAGE = get_todays_date(logged_user_data)
    elif cmd == "validar_pass":
        new_pass = input("Ingrese nueva contraseña a validar: ")
        MESSAGE = validate_pass(new_pass, logged_user_data)
    elif cmd == "calculadora":
        first = input("Ingrese el primer numero: ")
        op = input("Ingrese el operador: ")
        second = input("Ingrese el segundo numero: ")
        MESSAGE = handle_calculator_operations(first, op, second)
    elif "historial" in cmd:
        ##Se divide el input del usuario con split para validar realmente si el comando coincide completamente con historial all, no historial all clear, entre otros ejemplos
        input_split = cmd.split()
        MESSAGE = gestionar_historial(input_split, chat_history)
        print(MESSAGE)
    else:
        MESSAGE = "Comando desconocido, intente nuevamente"
        print(MESSAGE)

    chat_log: Recuerdo = create_log_entry(logged_user_data, user_input, MESSAGE, cmd)
    # Guarda el comando en el historial
    chat_history.append(chat_log)
