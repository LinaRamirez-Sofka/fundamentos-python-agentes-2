# 🛠️ Taller Semana 1: El Núcleo del Agente y Control de Acceso
# Lina María Ramírez

from datetime import date


user_credentials =  {
    "admin": {"password": "admin_pass", "rol": "admin"},
    "invitado": {"password": "user_pass", "rol": "guest"},
}
logged_user_data = {}
user_input = ""

#Metodo para contar letras, vocales y consonantes de una palabara
def count_word(word: str) -> None:
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

#Metodo para ejecutar el comando "fecha_hoy"
def get_todays_date():
    """
    Displays the current date in dd/mm/yyyy format if the logged user has
    the admin role; otherwise, prints an access denied message.
    """
    #Valida el rol del usuario, solo si es admin puede saber la fecha de hoy
    if logged_user_data["rol"] == "admin":
        today = date.today()
        #Se formatea la fecha a formato mas convencional de día/mes/año
        today_formatted = today.strftime("%d/%m/%Y")
        print(f"La fecha de hoy es {today_formatted}")
    else:
        print("[Acceso Denegado] Este comando requiere privilegios de administrador.")

#Metodo para validar la contraseña
def validate_pass(password: str)-> None:
    """
    Validates a password by checking if it has at least 8 characters
    (excluding leading/trailing spaces) and is not equal to the username.
    Prints validation results to the console.
    """
    valid_password = password.strip()
    #Valida la longitudo de la contraseña sin considerar espacios
    is_length_valid = len(valid_password) >= 8
    #Valida si la contraseña es igual al nombre de usuario
    is_equal_to_user_name = valid_password == user_input

    #Si incumple las dos validaciones, se indica con mensaje al usuario
    if not is_length_valid and is_equal_to_user_name:
        print("""
    La contraseña no cumple con las validaciones:
      - La longitud no es de minimo 8 carácteres
      - La contraseña es igual al nombre de usuario
        """)
    #Si incumple solo con la validacion de longitud minima
    elif not is_length_valid:
        print("La contraseña no cumple con la longitud mínima de 8 caracteres.")
    #Si incumple solo con la validacion de que no sea ingual al usuario
    elif is_equal_to_user_name:
        print("La contraseña no puede ser igual al nombre de usuario.")
    #Si cumple con la longitud y no es igual al nombre de usuario, se considera exitosa
    else:
         print("La nueva contraseña cumple con las validaciones")

#Metodo que gestiona las operaciones de la calculadora
def handle_calculator_operations(first_number:str,
                                 operator:str,
                                 second_number:str)-> None:
    """
    Handles basic calculator operations (+, -, *, /) on two numbers provided
    as strings, prints the result, and validates input and division by zero.
    """
    #Caseto de string que recibe el input a float para permitir operaciones matemáticas con decimales.
    # El no castear a tipo numerico haria que operaciones como -, * y / tiren un error y  que la suma sea una concatenación de strings y no una operación matemática
    first_number_float = float(first_number)
    second_number_float = float(second_number)
    result:float = 0.0

    #Omitir el caseto haria que los dos input first_number y second_number se concatenen como string
    if operator == "+":
        result = first_number_float + second_number_float
    #Operaciones como  -, * y / no son validas para string por lo que omitir el casteo a float lanzaria un error del tipo TypeError
    elif operator == "-":
        result = first_number_float - second_number_float
    elif operator == "*":
        result = first_number_float * second_number_float
    elif operator == "/":
        #Se valida que el divisor no sea 0, de ser así se lanza un error: ZeroDivisionError: float division by zero que para la ejecución del programa
        if second_number_float == float(0):
            print("Para el operador '/' el segundo numero no puede ser 0")
            return
        result = first_number_float/second_number_float
    else:
        print(f"El operador {operator} no es válido.")
        return
    print(f"La operación {first_number}{operator}{second_number} da como resultado {result}")



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

    cmd = input("\nPseudoAgente>: ").lower().strip()

    match cmd:
        case "salir":
            print("Finalizando la sesión")
            ACTIVE_SYSTEM = False
        case "ping":
            print("pong")
        case "contar":
            input_word = input("Ingrese una palabra: ").lower()
            count_word(input_word)
        case "fecha_hoy":
            get_todays_date()
        case "validar_pass":
            new_pass = input("Ingrese nueva contraseña a validar: ")
            validate_pass(new_pass)
        case "calculadora":
            first = input("Ingrese el primer numero: ")
            op = input("Ingrese el operador: ")
            second = input("Ingrese el segundo numero: ")
            handle_calculator_operations(first, op, second)
        case _:
           print("Comando desconocido, intente nuevamente")
