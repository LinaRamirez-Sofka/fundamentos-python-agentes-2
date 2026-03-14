# 🛠️ Taller Semana 1: El Núcleo del Agente y Control de Acceso
# Lina María Ramírez

print("\n-----------------Iniciando el pseudoagente estilo consola-----------------\n")

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
        if p in "aeiou":
            tot_vowels +=1
        else:
            tot_consts+=1
    #Resultados del conteo
    print(f"\nPalabra ingresada: {word}")
    print(f"Total letras: {tot_letter}")
    print(f"Total vocales: {tot_vowels}")
    print(f"Total constonantes: {tot_consts}\n")

ACTIVE_SYSTEM = False

user_credentials =  {
    "admin": {"password": "admin_pass", "rol": "admin"},
    "invitado": {"password": "user_pass", "rol": "guest"},
}
logged_user_data = {}
LOGIN_ATTEMPTS = 0
LOGIN_SUCCESS = False


while not LOGIN_SUCCESS:

    if LOGIN_ATTEMPTS == 3:
        print("[Alerta] Usuario bloqueado. Cerrando sistema.")
        break

    user_input = input("\nEscriba su usuario: ")
    pass_input = input("Digite su contraseña: ")
    LOGIN_ATTEMPTS += 1
    user_data = user_credentials[user_input]
    real_pass = user_data["password"]

    if real_pass == pass_input:
        LOGIN_SUCCESS = True
        ACTIVE_SYSTEM = True
        logged_user = logged_user_data
    else:
        print("\nContraseña incorrecta")







#Estructura de control while que indica el estado de la sesión y presenta el menú de acciones posibles a ejecutar
while ACTIVE_SYSTEM:

    cmd = input("\n\nPseudoAgente>: ").lower().strip()

    if cmd == "salir" :
        print("Finalizando la sesión")
        ACTIVE_SYSTEM = False
    elif cmd == "ping":
        print("pong")
    elif cmd == "contar":
        input_word = input("Ingrese una palabra: ").lower()
        count_word(input_word)
    else:
        print("Comando desconocido, intente nuevamente")

