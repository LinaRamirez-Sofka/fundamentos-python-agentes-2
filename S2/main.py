# 🛠️ Taller Semana 2:  Motor de Búsqueda del Agente
# Lina María Ramírez

from datetime import date, datetime


user_credentials =  {
    "admin": {"password": "admin_pass", "rol": "admin"},
    "invitado": {"password": "user_pass", "rol": "guest"},
}
logged_user_data = {}
user_input = ""

# Historial de chats con marca de tiempo, comando usado, rol, descripcion
chat_history  = [{'timestamp': '21-03-2026 21:06:16', 'cmd': 'ping', 'rol': 'admin', 'description': 'Se envió un ping y se devuelve un pong'}]    

#Metodo para contar letras, vocales y consonantes de una palabara
def count_word(word: str) -> str:
    """
    Counts and prints the total number of letters, vowels, and consonants in
    the given word. Output is displayed in the console.
    """
    tot_letter = len(word)
    tot_vowels = 0
    tot_consts = 0

    for p in word:
        #valida si la letra es una vocal, de lo contrario es una consonante
        if p in "aeiou":
            tot_vowels +=1
        else:
            tot_consts+=1
    #Resultados del conteo
    print(f"\nPalabra ingresada: {word}")
    print(f"Total letras: {tot_letter}")
    print(f"Total vocales: {tot_vowels}")
    print(f"Total constonantes: {tot_consts}")
    return f"La palabra ingresada fue {word} con {tot_letter} letras, {tot_vowels} vocales y {tot_consts} constantes"

#Metodo para ejecutar el comando "fecha_hoy"
def get_todays_date() -> str:
    """
    Displays the current date in dd/mm/yyyy format if the logged user has
    the admin role; otherwise, prints an access denied message.
    """
    message = ""
    #Valida el rol del usuario, solo si es admin puede saber la fecha de hoy
    if logged_user_data["rol"] == "admin":
        today = date.today()
        #Se formatea la fecha a formato mas convencional de día/mes/año
        today_formatted = today.strftime("%d/%m/%Y")
        message = f"La fecha de hoy es {today_formatted}"
        print(message)
    else:
        message = "Este comando requiere privilegios de administrador."
        print("[Acceso Denegado]" + message)
    return message

#Metodo para validar la contraseña
def validate_pass(password: str)-> str:
    """
    Validates a password by checking if it has at least 8 characters
    (excluding leading/trailing spaces) and is not equal to the username.
    Prints validation results to the console.
    """
    message = ""
    valid_password = password.strip()
    #Valida la longitudo de la contraseña sin considerar espacios
    is_length_valid = len(valid_password) >= 8
    #Valida si la contraseña es igual al nombre de usuario
    is_equal_to_user_name = valid_password == user_input

    #Si incumple las dos validaciones, se indica con mensaje al usuario
    if not is_length_valid and is_equal_to_user_name: 
        message = """
    La contraseña no cumple con las validaciones:
      - La longitud no es de minimo 8 carácteres
      - La contraseña es igual al nombre de usuario
        """
    #Si incumple solo con la validacion de longitud minima
    elif not is_length_valid:
        message = "La contraseña no cumple con la longitud mínima de 8 caracteres."
    #Si incumple solo con la validacion de que no sea ingual al usuario
    elif is_equal_to_user_name:
        message = "La contraseña no puede ser igual al nombre de usuario."
    #Si cumple con la longitud y no es igual al nombre de usuario, se considera exitosa
    else:
         message = "La nueva contraseña cumple con las validaciones"
    print(message)
    return message

#Metodo que gestiona las operaciones de la calculadora
def handle_calculator_operations(first_number: str, operator: str, second_number: str) -> str:
    """
    Handles basic calculator operations (+, -, *, /) on two numbers provided
    as strings, prints the result, and validates input and division by zero.
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

#Metodo para gestionar las acciones relacionadas con el historial
def handle_history_chat(cmd)-> str : 
    input_split = cmd.split()
    return_message = ""
    if "all" ==  input_split[1]:
        output = "Historial completo:\n"
        for entry in chat_history:
            output += f"{entry['timestamp']} - {entry['cmd']} - {entry['rol']} - {entry['description']}\n"
        return_message = "Se ha solicitado consultar el historial completo"
        print(output)
    elif "clear" ==  input_split[1]:
        return_message = "Se ha solicitado borrar el historial completo"
        print("Borrando el historial de la memoria del pseudoagente")
        chat_history.clear()
    elif cmd == "historial":
         word_to_search = input("Ingresa la palabra clave a buscar: ")
         conincidences = []
         word_processed = word_to_search.strip().lower()
        
         for log in chat_history:
            description_processed = log["description"].strip().lower()

            if word_processed in description_processed:
                conincidences.append(log)
        #TODO falta el puno 4 del taller 
    else:
        return_message = "Comando de historial no válido. Use: historial all"
        print(return_message)

    return return_message

print("\n-----------------Iniciando el pseudoagente estilo consola-----------------\n")

ACTIVE_SYSTEM = False
LOGIN_ATTEMPTS = 0
LOGIN_SUCCESS = False
MAX_ATTEMPTS = 3

#Bloque de autenticación
#Mientras el login no sea exitoso se consultara al usuario por el nombre y contraseña
while not LOGIN_SUCCESS:

    #Sin embargo, si el numero de intentos alcanza el máximo, el sistema se cierra y con break salimos del la estructura while
    if LOGIN_ATTEMPTS == MAX_ATTEMPTS:
        print("[Alerta] Usuario bloqueado. Cerrando sistema.")
        break

    user_input = input("\nEscriba su usuario: ").strip()
    pass_input = input("Digite su contraseña: ").strip()
    #Cada vez que el usuario digite las credenciales se cuenta como un intento de login
    LOGIN_ATTEMPTS += 1
    IS_CREDENTIAL_VALID = False

#Comprueba que el usuario esta registrado en el diccionario evita un key error si no existe la llave con el nombre del usuario
    if user_input in user_credentials:
        logged_user_data = user_credentials[user_input]
        #La contraseña se encuentra almacenada en el value de la key "password" para el diccionario asociado al usuario
        real_pass = logged_user_data["password"]
        IS_CREDENTIAL_VALID = real_pass == pass_input

    #Si las credenciales son validas, es decir, el usuario esta registrado en el diccionario y la contraseña ingresada coincide con la registrada
    # Se define que el usuario esta loggeado y se activa el sistema del agente
    if  IS_CREDENTIAL_VALID:
        LOGIN_SUCCESS = True
        ACTIVE_SYSTEM = True
        print(f"Bienvenido {user_input}. Despertando al agente.\n")
# De lo contrario se da mensaje informativo y se reptie el bucle
    else:
        print(f"\n🚫 Usuario o contraseña incorrecto. Inteno No. {LOGIN_ATTEMPTS} de {MAX_ATTEMPTS}")


#Bloque menu de control pseudoagente
#Estructura de control while que indica el estado de la sesión del pseudoagente y presenta el menú de acciones posibles a ejecutar
#El sistema solo se activa si las credenciales de acceso son validas
while ACTIVE_SYSTEM:
    
    MESSAGE = ""

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
        MESSAGE = get_todays_date()
    elif cmd == "validar_pass":
        new_pass = input("Ingrese nueva contraseña a validar: ")
        MESSAGE = validate_pass(new_pass)
    elif cmd == "calculadora":
        first = input("Ingrese el primer numero: ")
        op = input("Ingrese el operador: ")
        second = input("Ingrese el segundo numero: ")
        MESSAGE = handle_calculator_operations(first, op, second)
    elif "historial" in cmd:
        MESSAGE = handle_history_chat(cmd)
    else:
        MESSAGE = "Comando desconocido, intente nuevamente"
        print(MESSAGE)

    chat_log = {
        "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "cmd": cmd,
        "rol": logged_user_data["rol"],
        "description": MESSAGE
    }

    chat_history.append(chat_log)
    print("\n ----------------HISTORIAL CHAT ---------------- \n\n", chat_history, "\n-----------------------------------------------------------\n")
