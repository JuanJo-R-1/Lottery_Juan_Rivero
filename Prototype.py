import os
import json
import hashlib
import random
from datetime import datetime
import msvcrt

#valores por defecto de estas variables, se pueden cambiar en el menu de admin
lottery_size = 10
ticket_price = 0
lottery_prize = 10000
max_tickets = 99 
ticket_numbers = 6  
ticket_min = 1
ticket_max = 99

prizes_config = None  # Variable global para guardar la configuración de premios

def clean_term():#limpia la terminal para mayor orden
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def ask_letters(message, only_letters=True): #pide letras al usuario, no acepta numeros ni caracteres especiales
    while True:
        text = input(message).strip()
        if only_letters:
            if text.replace(" ", "").isalpha():
                if text > " " and len(text) > 20:
                    print("Error. The text must not exceed 20 characters. Try again.")
                    continue
                elif text > " " and len(text) <= 20:
                    print("Text accepted.")
                    return text
            else:
                print("Error. Only letters are allowed. Try again.")
        else:
            if text:
                return text
            else:
                print("Error, This space can't be clear.")

def ask_lottery_number(used_numbers): #pide un numero al usuario, no acepta numeros repetidos ni fuera del rango de la loteria
    while True:
        bet = input(f"Enter the number that the participant wants to bet (only numbers and {lottery_size}, is the limit): ").strip()
        if bet.isdigit():
            num = int(bet)
            if num in used_numbers:
                print("Error. That number has already been chosen by another participant. Try another one.")
            elif 1 <= num <= lottery_size:
                print("Number accepted.")
                return bet
            else:
                print(f"Error. The bet number must be between 1 and {lottery_size}, try again.")
        else:
            print("Error. The bet number must be written with numbers, try again.")

def save_config():# Guarda la configuración actual en un archivo JSON
    config = {
        "lottery_size": lottery_size,
        "lottery_prize": lottery_prize,
        "ticket_price": ticket_price,
        "max_tickets": max_tickets,
        "ticket_numbers": ticket_numbers,
        "ticket_min": ticket_min,
        "ticket_max": ticket_max
    }
    with open("config.json", "w") as f:
        json.dump(config, f)

def load_config():# Carga la configuración desde un archivo JSON
    global lottery_size, lottery_prize, ticket_price, max_tickets, ticket_numbers, ticket_min, ticket_max
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            lottery_size = config.get("lottery_size", 0)
            lottery_prize = config.get("lottery_prize", 0)
            ticket_price = config.get("ticket_price", 0)
            max_tickets = config.get("max_tickets", 99)
            ticket_numbers = config.get("ticket_numbers", 6)
            ticket_min = config.get("ticket_min", 1)
            ticket_max = config.get("ticket_max", 99)
    except (FileNotFoundError, json.JSONDecodeError):
        lottery_size = 0
        lottery_prize = 0
        ticket_price = 0
        max_tickets = 99
        ticket_numbers = 6
        ticket_min = 1
        ticket_max = 99
if __name__ == "__main__":
    try:
        with open("suerte.json", "r") as file:
            content = file.read().strip()
            if not content:
                with open("suerte.json", "w") as file:
                    json.dump([], file)
    except FileNotFoundError:
        with open("suerte.json", "w") as file:
            json.dump([], file)

def bet_size():# Asigna el tamaño de la lotería, el cual es un numero entre 1 y 1000000, si no se asigna, no se puede jugar
    global lottery_size
    clean_term()
    while True:
        try:
            size = int(input("Enter the size of the lottery : "))
            if size > 1000000:
                print("Error. The size of the lottery must be less than 1000000, try again.")
            elif size <= 1:
                print("Error. The size of the lottery must be more than 1, try again.")
            else:
                print(f"The size of the lottery is {size}, acceptable.")
                lottery_size = size
                save_config()  # <--- Guarda la configuración
                return size
        except ValueError:
            print("Error. The size of the lottery must be a number, try again.")

def Asign_lottery_prize():# Asigna el premio de la lotería, el cual es un numero entre 100000 y 1000000000, si no se asigna, no se puede jugar
    clean_term()
    global lottery_prize
    while True:
        try:
            prize = int(input("Enter the prize of the lottery (money): "))
            if prize > 1000000000:
                print("Error. The lottery prize must be less than 1000000000, try a lower prize")
            elif prize <= 100000:
                print("Error. The lottery prize must be more than 100000, try a higher prize")
            else:
                print(f"the size of the lottery is {prize}, acceptable")
                lottery_prize = prize
                save_config()  # <--- Guarda la configuración
                return prize
        except ValueError:
            print("Error. The prize of the lottery must be a number, try again")

def Asign_ticket_price():# Asigna el precio del boleto, segun la cantidad de premio y el tamaño de la lotería, si no se asigna, no se puede jugar
    clean_term()
    global ticket_price
    while True:
        ticket_price = ((lottery_prize/lottery_size)*1.2)
        print(f"the price of the tickets wiil be: {ticket_price}")
        save_config()  # <--- Guarda la configuración
        return ticket_price

def user_data(current_user=None):# Pide los datos del usuario, si es admin, tiene configuraciones acanzadas, si es usuario normal, tiene un menu común
    global lottery_size
    if lottery_size == 0:
        print("You must set the size of the lottery before adding participants.")
        return
    clean_term()
    participants = []
    used_numbers = set()
    try:
        with open("suerte.json", "r") as file:
            existing = json.load(file)
            for p in existing:
                used_numbers.add(int(p["Number"]))
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []
    if current_user:  # Usuario normal, solo puede agregarse a sí mismo
        Name = current_user
        ticket = ask_lottery_number(used_numbers)
        used_numbers.add(int(ticket))
        participants.append({"Name": Name, "Number": ticket})
        all_participants = existing + participants
        with open("suerte.json", "w") as file:
            json.dump(all_participants, file, indent=4)
            print("Data saved.")
    else:  # Admin, puede agregar cualquier nombre
        Name = ask_letters("Enter the participant Name (Only letters, max 20 chars): ").strip()
        ticket = ask_lottery_number(used_numbers)
        used_numbers.add(int(ticket))
        participants.append({"Name": Name, "Number": ticket})
        all_participants = existing + participants
        with open("suerte.json", "w") as file:
            json.dump(all_participants, file, indent=4)
            print("Data saved.")

def show_participants():#muestra a los participantes que hay en el momento
    clean_term()
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if participants:
                print("Current participants:")
                for participant in participants:
                    print(f"Name: {participant['Name']}, Numbers: {', '.join(participant['Numbers'])}")#muestra los nombres y numeros, si no hay, pide ingresar
            else:
                print("No participants found.")
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")

def edit_participants():#edita la informacion de los participantes, nombre(sin repetir) y el numero de apuesta
    clean_term()
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if not participants:
                print("No participants were found to edit.")
                return
            print("Current participants:")
            for idx, participant in enumerate(participants, 1):
                print(f"{idx}. Name: {participant['Name']}, Numbers: {', '.join(participant['Numbers'])}")
            idx_to_edit = int(input("Enter the number of the user you want to edit: ")) - 1
            if 0 <= idx_to_edit < len(participants):
                new_name = ask_letters("Enter the new name for the participant: ")
                temp_participants = participants[:idx_to_edit] + participants[idx_to_edit+1:]#Asigna el nuevo nombre y da la opcion de editar los numeros
                used_by_position = build_used_by_position(temp_participants)
                new_numbers = ask_ticket_numbers_by_position(used_by_position)
                if not new_numbers:
                    print("No se pudo editar el boleto por falta de números disponibles.")
                    return
                participants[idx_to_edit]['Name'] = new_name
                participants[idx_to_edit]['Numbers'] = new_numbers
                with open("suerte.json", "w") as file:
                    json.dump(participants, file, indent=4)
                print("Participant updated successfully.")
            else:
                print("out of range.")
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")
    except ValueError:
        print("Invalid character.")

def delete_participants():#borra a los participantes
    clean_term()
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if not participants:
                print("No participants were found to delete.")
                return
            print("Current participants:")
            for idx, participant in enumerate(participants, 1):
                print(f"{idx}. Name: {participant['Name']}, Numbers: {', '.join(participant['Numbers'])}")
            idx_to_delete = int(input("Enter the number of the ticket you want to delete: ")) - 1
            if 0 <= idx_to_delete < len(participants):
                del participants[idx_to_delete]
                with open("suerte.json", "w") as file:
                    json.dump(participants, file, indent=4)
                print("Participant deleted successfully.")
            else:
                print("Índice fuera de rango.")
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")
    except ValueError:
        print("Entrada inválida.")

def play_lottery():
    global prizes_config
    clean_term()
    try:
        with open("suerte.json", "r") as file:
            participants = json.load(file)
            if not participants:
                print("No participants found. Please add participants first.")
                return
    except FileNotFoundError:
        print("No participants data found. Please add participants first.")
        return

    # Usa la configuración de premios si ya existe, si no, pide al admin configurarla
    if not prizes_config:
        prizes = configure_prizes()
    else:
        prizes = prizes_config

    winner_ticket = Make_winner_ticket()
    print(f"\nWinner ticket: {' '.join(winner_ticket)}\n")
    results = []
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_tickets = len(participants)
    total_money = ticket_price * total_tickets
    investment = total_money - lottery_prize
    for ticket in participants:
        successes = len(set(ticket["Numbers"]) & set(winner_ticket))
        prize = prizes.get(successes, "No prize")
        # Puedes ajustar el cálculo de Revenue según el premio
        Revenue = 0
        if prize == "Biggest prize":
            Revenue = lottery_prize/2 - ticket_price
        elif prize == "Medium prize":
            Revenue = lottery_prize/3 - ticket_price
        elif prize == "Small prize":
            Revenue = lottery_prize/6 - ticket_price
        else:
            Revenue = -ticket_price
        results.append({
            "Date": date,
            "Name": ticket["Name"],
            "Ticket": ticket["Numbers"],
            "successes": successes,
            "Prize": prize,
            "Revenue": Revenue
        })
    for r in results:    # Mostrar resultados
        print(f"{r['Date']} | {r['Name']} | Ticket: {' '.join(r['Ticket'])} | successes: {r['successes']} | {r['Prize']} | Revenue: {r['Revenue']}")
    print(f"\nTotal money got: {total_money}")
    print(f"total prize: {lottery_prize}")
    print(f"Extra Revenue for the admin: {investment}")
    try:    # Guardar historial
        with open("w_history.json", "r") as hfile:
            history = json.load(hfile)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    history.append({
        "Date": date,
        "Winner_ticket": winner_ticket,
        "results": results,
        "total_money": total_money,
        "investment": investment
    })
    with open("w_history.json", "w") as hfile:
        json.dump(history, hfile, indent=4)
    print("\nResults saved in the record.")

def press_ent():#presionar Enter para continuar
    input('Press Enter to continue')

def menu():# Muestra el menu del administrador, donde puede editar los participantes, los boletos, jugar la lotería, ver los ganadores y salir
    while True:
        clean_term() # Muestra los participantes antes del menu del admin
        print(""" The Admin menu

1. )   lottery options
2. )   Users options
3. )   Ticket options
4. )   Play the lottery      
5. )   Winner record and other
6. )   Configure prizes
7. )   Exit

""")
        try:
            option = int(input("select one of the options: \n"))
        except ValueError:
            print("Enter a valid option (only numbers).")
            press_ent()
            continue
        if option == 1:
            lottery_options()
            press_ent()
        elif option == 2:
            user_options()
            press_ent()
        elif option == 3:
            ticket_options()
            press_ent()
        elif option == 4:
            play_lottery()
            press_ent()
        elif option == 5:
            winner_options()
            press_ent()
        elif option == 6:
            configure_prizes()
            press_ent()
        elif option == 7:
            return start()
        else:
            print('Enter a valid option')
            press_ent()

def winner_options():# Muestra las opciones de ganadores, donde se pueden ver los ganadores de la lotería, los ganadores de premios grandes y regresar al menu del admin
    while True:
        clean_term()
        print("""Options to select:

1. )   Winners history
2. )   Big prize winners
3. )   Delete winners history
4. )   Delete all tickets/participants
5. )   Return to Admin menu

""")
        try:
            option = int(input("Select one of the options: \n"))
        except ValueError:
            print("Enter a valid option (only numbers).")
            press_ent()
            continue
        if option == 1:
            show_winners()
            press_ent()
        elif option == 2:
            show_big_prize_winners()
            press_ent()
        elif option == 3:
            clear_winners_history()
        elif option == 4:
            clear_participants_history()
        elif option == 5:
            return menu()
        else:
            print('Enter a valid option')
            press_ent()

def lottery_options():# Muestra las opciones de la lotería, donde se pueden editar los aspectos de la lotería, como el tamaño, el premio, el precio del boleto, los modos predeterminados y ver la configuración actual de la lotería
    while True:
        clean_term()
        print("""Tools to manage de lottery characteristics:

1. )   Enter the size of the lottery
2. )   Enter the lottery prize
3. )   Enter the ticket price
4. )   Predeterminated lottery modes
5. )   See current lottery configuration
6. )   Return to Admin menu

""")
        try:
            option = int(input("select one of the options: \n"))
        except ValueError:
            print("Enter a valid option (only numbers).")
            press_ent()
            continue
        if option == 1:
            bet_size()
            press_ent()
        elif option == 2:
            Asign_lottery_prize()
            press_ent()
        elif option == 3:
            Asign_ticket_price()
            press_ent()
        elif option == 4:
            Lottery_modes()
            press_ent()
        elif option == 5:
            lottery_config()
            press_ent()
        elif option == 6:
            return menu()
        else:
            print('Enter a valid option')
            press_ent()

def user_options():# Muestra las opciones de los usuarios, donde se pueden ver los participantes actuales, editar los participantes, eliminar participantes, gestionar cuentas de usuarios (nombre o contraseña) y regresar al menú del administrador
    while True:
        clean_term()
        print("""Tools to manage users and participants:

1. )   Show the current participants
2. )   Edit the participants
3. )   Delete participants
4. )   Manage Users accounts (Name or Password)
5. )   Return to Admin menu

""")
        try:
            option = int(input("select one of the options: \n"))
        except ValueError:
            print("Enter a valid option (only numbers).")
            press_ent()
            continue
        if option == 1:
            show_participants()
            press_ent()
        elif option == 2:
            edit_participants()
            press_ent()
        elif option == 3:
            delete_participants()
            press_ent()
        elif option == 4:
            Users_control()
            press_ent()
        elif option == 5:
            return menu()
        else:
            print('Enter a valid option')
            press_ent()    

def ticket_options():# Muestra las opciones de los boletos, donde se pueden seleccionar la cantidad de boletos, cambiar el número de boletos (2-6), poner un límite de números (1-99) y regresar al menú del administrador
    while True:
        clean_term()
        print("""Tools for the management of tickets:

1. )   Select the ticket quantity
2. )   Change number quantity on the ticket (2-6)
3. )   Put number limit (1-99)
4. )   Return to Admin menu

        """)
        try:
            option = int(input("select one of the options: \n"))
        except ValueError:
            print("Enter a valid option (only numbers).")
            press_ent()
            continue
        if option == 1:
            ticket_limit()
            press_ent()
        elif option == 2:
            ticket_numb_limit()
            press_ent()
        elif option == 3:
            ticket_chance()
            press_ent()
        elif option == 4:
            return menu()
        else:
            print('Enter a valid option')
            press_ent()

def hash_password(password):# Codifica la contraseña del administrador para mayor seguridad DESACTIVADA POR AHORA
    #para codificar la contraseña, se usa:
    #def hash_password(password):
    #return hashlib.sha256(password.encode()).hexdigest()
    return password

def generate_unique_code(users):#Se encarga de generar el codigo de 4 digitos para los usuarios, el admin elige su propio codigo
    while True:
        code = "{:04d}".format(random.randint(0, 9999))
        if not any(u.get("code") == code for u in users.values()):
            return code

def register_user():# Se encarga de registrar un usuario, ya sea administrador o normal, y evita que se repitan los nombres de usuario
    clean_term()
    username = input("Choose a username: ").strip()#opcion del usuario a ingresar el nombre de su cuenta
    try:
        with open("Users.json", "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        users = {}
    if username in users:
        print("That username is already taken.")#Evita que los usuarios tenga un nombre identico, ejemplo David y David, pero se permite David y David S, etc.desde que no sea identico.
        return False
    if users and any(u["role"] == "admin" and username == admin for admin, u in users.items()):#Evita que un usuario normal use el nombre del admin
        print("You cannot use the admin's username.")
        return False
    if not users:
        clean_term()
        password = input("Choose a password: ").strip()#Se crea un usuario de administrador, único
        while True:
            code = input("Enter a 4-digit admin code (e.g. 1234): ").strip()#el admin elige su propio codigo de 4 digitos
            if code.isdigit() and len(code) == 4:
                break
            print("Code must be exactly 4 digits.")
        role = "admin"#Se crea el usuario de administrador
        users[username] = {
            "password": hash_password(password),
            "role": role,
            "code": code
        }
        print(f"Admin registered with code: {code}")
        press_ent()
    else:
        clean_term()
        code = generate_unique_code(users)#Se crea uno de multiples usuarios normales
        role = "user"
        users[username] = {
            "role": role,
            "code": code
        }
        print(f"User registered. Your access code is: {code}")
        press_ent()
    with open("users.json", "w") as f:
        json.dump(users, f, indent=4)
    print(f"User registered successfully as {role}.")
    return start()

def login_user(): #Se usa ingresar el nombre del usuario en la pagina a menos que no se encuentre el usuario, lo regresa al menu principal
    clean_term()
    username = input("Username: ").strip()
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No users registered.")
        return start()
    if username in users:#si el usuario existe, le ejecuta lo siguiente
        user = users[username]
        if user["role"] == "admin":#si elige admin, le pide el usuario, la contraseña y el codigo
            password = input("Password: ").strip()
            code = input_hidden_code("Admin code (4 digits): ", 4)
            if user.get("password") == hash_password(password) and user.get("code") == code:
                print("Login successful as admin.")#si es correcto ingresa como admin
                return username, "admin"
            else:
                print("Invalid password or code.")
                return start()
        else:
            code = input_hidden_code("Enter your 4-digit code: ", 4)#ejecuta la entrada de un usuario normal con su codigo y nombre
            if user.get("code") == code:
                print("Login successful as user.")
                return username, "user"
            else:
                print("Invalid code.")
                return start()
    else:
        clean_term()
        print("User not found. If you are new, please register first.") #si el usuario no existe lo regresa a la pagina principal para que se registre o ingrese de forma correcta el nombre, quien sabe
        return start()

def start():#Genera la pagina principal, el menu,
    clean_term()
    while True:
        try:
            with open("Users.json", "r") as f:
                users = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}
        if users:
            print("""
[̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]  [̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]  [̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]

████████████████████████████████████████████
██▄ ▄███ ▄▄ █ ▄ ▄ █ ▄ ▄ █▄ ▄▄ █▄ ▄▄▀█▄ █ ▄██
███ ██▀█ ██ ███ █████ ████ ▄█▀██ ▄ ▄██▄ ▄███
█▀▄▄▄▄▄▀▄▄▄▄▀▀▄▄▄▀▀▀▄▄▄▀▀▄▄▄▄▄▀▄▄▀▄▄▀▀▄▄▄▀▀█

███████████████████████████████████
████▄ ▀█▀ ▄█▄ ▄▄ █▄ ▀█▄ ▄█▄ ██ ▄███
█████ █▄█ ███ ▄█▀██ █▄▀ ███ ██ ████
██▀▀▄▄▄▀▄▄▄▀▄▄▄▄▄▀▄▄▄▀▀▄▄▀▀▄▄▄▄▀▀██

[̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]  [̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]  [̲̅$̲̅( ͡• ‿ ͡•)̲̅$̲̅]
                
                1. Login
                2. Register
                3. Exit
                
                """)#Da las opciones para que el usuario realize
            choice = input("Choose an option: ")
            if choice == "1":
                clean_term()
                username, role = login_user()
                if username:
                    if role == "admin":#muestra el menu editable para el administrador
                        menu()
                    else:
                        user_menu(username)#Muestra el menu para usuario normales sin posibilidad de editar aspectos, solo su desicion de participar o no
                    break
            elif choice == "2":#Creacion de usuarios
                clean_term()
                register_user()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        else:
            print("No admin registered. Please register the admin user.")#el admin es el primer usuario en ser creado, ademas de ser unico, si no existe, se pide
            register_user()

def user_menu(current_user): #presenta el menu con las respectivas opciones que el usuario normal puede elegir
    while True:
        clean_term()
        print(f"Welcome, {current_user}.\n")
        print("1. see current lottery configuration")
        print("2. See current participants")
        print("3. buy tickets")
        print("4. See winners history")
        print("5. Exit to main menu")
        option = input("Select one option: ")
        if option == "1":
            lottery_config()
            press_ent()
        elif option == "2":
            show_participants()
            press_ent()
        elif option == "3":
            buy_tickets(current_user)
            press_ent()
        elif option == "4":
            press_ent()
        elif option == "5":
            return start() #vuelve a la pagina principal
        else:
            print("Invalid option. Please try again.")
            press_ent()

def build_used_by_position(participants):# Crea una lista de conjuntos para cada posición del boleto, donde cada conjunto contiene los números usados en esa posición por todos los participantes
    used_by_position = [set() for _ in range(ticket_numbers)]
    for boleto in participants:
        for idx, num in enumerate(boleto["Numbers"]):
            if idx < ticket_numbers:
                used_by_position[idx].add(num)
    return used_by_position

def buy_tickets(current_user):# Permite a los usuarios comprar boletos para la lotería, asegurando que no se repitan números en un boleto o entre boletos
    global lottery_size, ticket_price, max_tickets
    if lottery_size == 0 or ticket_price == 0:
        print("The lottery isn't available for now. Please wait.")
        return
    try:
        with open("suerte.json", "r") as file:
            existing = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing = []
    current_count = len(existing)
    available_tickets = max_tickets - current_count
    if available_tickets <= 0:
        print("The maximum number of tickets for this lottery has been reached.")
        return
    while True:    #Se le pide al usuario ingresar una cantidad de dinero para comprar boletos
        try:
            money = float(input("¿How much money do you want to spend?: "))
            if money < ticket_price:
                print("You don't have enough money to buy a ticket.")
                return
            break
        except ValueError:
            print("Enter a valid quantity of money.")
    used_by_position = build_used_by_position(existing)
    max_possible_tickets = min(99 - len(pos) for pos in build_used_by_position(existing))
    max_tickets_to_buy = min(available_tickets, max_possible_tickets, int(money // ticket_price))
    if max_tickets_to_buy == 0:
        print("No tickets can be bought at this time.")
        return
    print(f"You can buy up to {max_tickets_to_buy} tickets.")
    while True:
        try:
            num_tickets = int(input(f"¿How many tickets do you want to buy? (1-{max_tickets_to_buy}): "))
            if 1 <= num_tickets <= max_tickets_to_buy:
                break
            else:
                print("Quantity out of range")
        except ValueError:
            print("Enter a valid number.")
    tickets = []
    for i in range(num_tickets):
        print(f"\nEnter the 6 numbers for the ticket #{i+1} (between 01 and 99, no repeat in this ticket or in other tickets):")
        ticket = ask_ticket_numbers_by_position(used_by_position)
        if not ticket:
            print("The ticket can't be generated due to lack of available numbers.")
            break
        tickets.append({"Name": current_user, "Numbers": ticket})
        for idx, num in enumerate(ticket):
            used_by_position[idx].add(num)
    all_participants = existing + tickets
    with open("suerte.json", "w") as file:
        json.dump(all_participants, file, indent=4)
    order_suerte_json()
    print(f"¡You have bought {len(tickets)} tickets!")

def Make_winner_ticket(): #Genera un boleto ganador aleatorio con 6 numeros del 01 al 99, para que los usuarios que mas se parezcan ganen premios
    return sorted([str(random.randint(ticket_min, ticket_max)).zfill(2) for _ in range(ticket_numbers)])

def order_suerte_json():  # Ordena el archivo suerte.json por nombre de usuario
    try:
        with open("suerte.json", "r") as file:
            data = json.load(file)
        data.sort(key=lambda x: x["Name"])
        with open("suerte.json", "w") as file:
            json.dump(data, file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def ask_ticket_numbers_by_position(used_by_position):# Pide al usuario ingresar números para cada posición del boleto, asegurando que no se repitan en esa posición o entre posiciones
    while True:
        choice = input("Do you wanna enter the numbers Manual(M) or Automatic(A): ").strip().upper()
        if choice in ("M", "A"):
            break
        print("Opción inválida. Escribe 'M' o 'A'.")
    numbers = []
    for pos in range(ticket_numbers):
        disponibles = [
            str(i).zfill(2)
            for i in range(ticket_min, ticket_max + 1)
            if str(i).zfill(2) not in used_by_position[pos]
        ]
        if not disponibles:
            print(f"There aren't enough available numbers for position {pos+1}. Cancelling this ticket.")
            return []
        if choice == "M":
            while True:
                num = input(f"Put numbers for position {pos+1} (between {str(ticket_min).zfill(2)} and {str(ticket_max).zfill(2)}): ").zfill(2)
                if num in disponibles:
                    numbers.append(num)
                    break
                else:
                    print("Número inválido o ya usado en esta posición. Elige otro.")
        else:  # Aleatorio
            num = random.choice(disponibles)
            print(f"Número aleatorio para la posición {pos+1}: {num}")
            numbers.append(num)
    return numbers

def show_winners():# Muestra el historial de ganadores, filtrando por aquellos que han ganado algún premio (4, 5 o 6 aciertos)
    clean_term()
    try:
        with open("w_history.json", "r") as file:
            history = json.load(file)
            if not history:
                print("There are no winners yet.")
                press_ent()
                return
            print("=== Winners History ===\n")
            found_any = False
            for idx, draw in enumerate(history, 1):
                # El máximo de aciertos es igual a ticket_numbers
                max_success = ticket_numbers
                # Puedes ajustar los premios aquí si quieres
                winners = [result for result in draw["results"] if result["successes"] == max_success]
                if winners:
                    found_any = True
                    print(f"Lottery #{idx} - Date: {draw['Date']}")
                    print(f"Winner ticket: {' '.join(draw['Winner_ticket'])}")
                    print("Winners:")
                    for result in winners:
                        print(f"  {result['Name']} | Ticket: {' '.join(result['Ticket'])} | Prize: {result['Prize']} | Successes: {result['successes']}")
                    print("-" * 40)
            if not found_any:
                print("No winners for any prize in the history.")
            press_ent()
    except (FileNotFoundError, json.JSONDecodeError):
        print("There is no lottery records registered")
        press_ent()

def show_big_prize_winners():# Muestra el historial de ganadores del premio mayor (6 aciertos), filtrando por aquellos que han ganado el premio mayor
    clean_term()
    try:
        with open("w_history.json", "r") as file:
            history = json.load(file)
            if not history:
                print("No big prize winners yet.")
                press_ent()
                return
            print("=== Big Prize Winners (6 matches) ===\n")
            found_any = False
            for idx, draw in enumerate(history, 1):
                big_winners = [result for result in draw["results"] if result["successes"] == 6]
                if big_winners:
                    found_any = True
                    print(f"Lottery #{idx} - Date: {draw['Date']}")
                    print(f"Winner ticket: {' '.join(draw['Winner_ticket'])}")
                    print("Big Prize Winners:")
                    for result in big_winners:
                        print(f"  {result['Name']} | Ticket: {' '.join(result['Ticket'])} | Prize: {result['Prize']} | Successes: {result['successes']}")
                    print("-" * 40)
            if not found_any:
                print("No big prize winners in the history.")
            press_ent()
    except (FileNotFoundError, json.JSONDecodeError):
        print("There is no lottery records registered")
        press_ent()

def Users_control():# Permite al administrador gestionar usuarios, incluyendo ver usuarios registrados, editar contraseñas y agregar nuevos usuarios
    clean_term()
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No users registered.")
        return

    username = input("Enter the username to manage: ").strip()
    if username not in users:
        print("User not found.")
        return

    user = users[username]
    if "password" in user:
        print(f"Current password for {username}: {user['password']}")
    else:
        print("This user does not have a password set.")

    change = input("Do you want to change the password? (Y/N): ").strip().upper()
    if change == "Y":
        new_password = input("Enter the new password: ").strip()
        user["password"] = hash_password(new_password)
        users[username] = user
        with open("users.json", "w") as f:
            json.dump(users, f, indent=4)
        print("Password updated successfully.")
    else:
        print("No changes made.")
    press_ent()

def clear_winners_history():# Permite al administrador borrar todo el historial de ganadores, asegurando que se confirme la acción antes de proceder
    clean_term()
    confirm = input("Are you sure you want to delete the entire winners history? (Y/N): ").strip().upper()
    if confirm == "Y":
        with open("w_history.json", "w") as f:
            json.dump([], f, indent=4)
        print("Winners history deleted successfully.")
    else:
        print("Operation cancelled.")
    press_ent()

def clear_participants_history():# Permite al administrador borrar todo el historial de participantes y boletos, asegurando que se confirme la acción antes de proceder
    clean_term()
    confirm = input("Are you sure you want to delete all tickets/participants? (Y/N): ").strip().upper()
    if confirm == "Y":
        with open("suerte.json", "w") as f:
            json.dump([], f, indent=4)
        print("Participants/tickets history deleted successfully.")
    else:
        print("Operation cancelled.")
    press_ent()

def ticket_limit():# Permite al administrador establecer el límite máximo de boletos que se pueden comprar en la lotería
    global max_tickets
    clean_term()
    print(f"Current ticket limit: {max_tickets}")
    while True:
        try:
            new_limit = int(input("Enter the new maximum number of tickets for the lottery: "))
            if new_limit < 1:
                print("The limit must be at least 1.")
            else:
                max_tickets = new_limit
                save_config()
                print(f"Ticket limit updated to {max_tickets}.")
                break
        except ValueError:
            print("Enter a valid number.")

def ticket_numb_limit():# Permite al administrador cambiar el número de números por boleto, asegurando que esté entre 2 y 6
    global ticket_numbers
    clean_term()
    print(f"Current number of numbers per ticket: {ticket_numbers}")
    while True:
        try:
            new_n = int(input("Enter the new number of numbers per ticket (2-6): "))
            if 2 <= new_n <= 6:
                ticket_numbers = new_n
                save_config()
                print(f"Number of numbers per ticket updated to {ticket_numbers}.")
                break
            else:
                print("The number must be between 2 and 6.")
        except ValueError:
            print("Enter a valid number.")

def ticket_chance():# Permite al administrador establecer un límite de números para los boletos, asegurando que el mínimo sea 1 y el máximo sea 99, y que el mínimo sea menor que el máximo
    global ticket_min, ticket_max
    clean_term()
    print(f"Current minimum value for ticket numbers: {ticket_min}")
    print(f"Current maximum value for ticket numbers: {ticket_max}")
    while True:
        try:
            new_min = int(input("Enter the new minimum value for ticket numbers (1-98): "))
            new_max = int(input("Enter the new maximum value for ticket numbers (2-99): "))
            if 1 <= new_min < new_max <= 99:
                ticket_min = new_min
                ticket_max = new_max
                save_config()
                print(f"Ticket number limits updated: min={ticket_min}, max={ticket_max}")
                break
            else:
                print("Minimum must be at least 1 and less than maximum. Maximum must be at most 99 and greater than minimum.")
        except ValueError:
            print("Enter valid numbers.")

def Lottery_modes():# Permite al administrador seleccionar entre configuraciones rápidas predefinidas para la lotería, como lotería sencilla, media o grande
    global lottery_size, max_tickets, lottery_prize, ticket_numbers, ticket_min, ticket_max, ticket_price
    clean_term()
    print("""Quick Lottery Modes:

1. )   Lotería sencilla
2. )   Lotería media
3. )   Lotería grande
4. )   Return to previous menu

""")
    try:
        option = int(input("Select a quick configuration: "))
    except ValueError:
        print("Enter a valid option (only numbers).")
        press_ent()
        return

    if option == 1:
        # Lotería sencilla
        print("""
You have selected: Lotería sencilla

- Tamaño para 20 personas
- 30 boletos máximo
- Premio: 100000
- Cada boleto con 2 números (del 1 al 20)

""")
        confirm = input("Do you want to activate this configuration? (Y/N): ").strip().upper()
        if confirm == "Y":
            lottery_size = 20
            max_tickets = 30
            lottery_prize = 100000
            ticket_numbers = 2
            ticket_min = 1
            ticket_max = 20
            ticket_price = ((lottery_prize/lottery_size)*1.2)
            save_config()
            print("Lotería sencilla configurada exitosamente.")
        else:
            print("Configuración cancelada.")
        press_ent()

    elif option == 2:
        # Lotería media
        print("""
You have selected: Lotería media

- Tamaño para 50 personas
- 80 boletos máximo
- Premio: 500000
- Cada boleto con 4 números (del 1 al 50)

""")
        confirm = input("Do you want to activate this configuration? (Y/N): ").strip().upper()
        if confirm == "Y":
            lottery_size = 50
            max_tickets = 80
            lottery_prize = 500000
            ticket_numbers = 4
            ticket_min = 1
            ticket_max = 50
            ticket_price = ((lottery_prize/lottery_size)*1.2)
            save_config()
            print("Lotería media configurada exitosamente.")
        else:
            print("Configuración cancelada.")
        press_ent()

    elif option == 3:
        # Lotería grande
        print("""
You have selected: Lotería grande

- Tamaño para 99 personas
- 150 boletos máximo
- Premio: 2000000
- Cada boleto con 6 números (del 1 al 99)

""")
        confirm = input("Do you want to activate this configuration? (Y/N): ").strip().upper()
        if confirm == "Y":
            lottery_size = 99
            max_tickets = 150
            lottery_prize = 2000000
            ticket_numbers = 6
            ticket_min = 1
            ticket_max = 99
            ticket_price = ((lottery_prize/lottery_size)*1.2)
            save_config()
            print("Lotería grande configurada exitosamente.")
        else:
            print("Configuración cancelada.")
        press_ent()

    elif option == 4:
        return
    else:
        print("Enter a valid option.")
        press_ent()

def lottery_config():# Muestra la configuración actual de la lotería, incluyendo el tamaño, el número máximo de boletos, el premio, el precio del boleto, los números por boleto y los límites de números
    clean_term()
    print("=== Current Lottery Configuration ===\n")
    print(f"Lottery size (number of participants): {lottery_size}")
    print(f"Maximum tickets: {max_tickets}")
    print(f"Lottery prize: {lottery_prize}")
    print(f"Ticket price: {ticket_price}")
    print(f"Numbers per ticket: {ticket_numbers}")
    print(f"Minimum value for ticket numbers: {ticket_min}")
    print(f"Maximum value for ticket numbers: {ticket_max}")
    print("\n=====================================")

def input_hidden_code(prompt="Enter code: ", length=4):
    print(prompt, end='', flush=True)
    code = ""
    while len(code) < length:
        ch = msvcrt.getch()
        if ch in (b'\r', b'\n'):
            break
        if ch == b'\x08':  # Backspace
            if code:
                code = code[:-1]
                print('\b \b', end='', flush=True)
        elif ch.isdigit() and len(code) < length:
            code += ch.decode()
            print('·', end='', flush=True)
    print()
    return code

def configure_prizes():
    global prizes_config
    clean_term()
    print("Configure the number of matches required for each prize.")
    try:
        big = int(input(f"How many matches for the BIG prize? (default: {ticket_numbers}): ") or ticket_numbers)
        medium = int(input(f"How many matches for the MEDIUM prize? (default: {ticket_numbers-1}): ") or (ticket_numbers-1))
        small = int(input(f"How many matches for the SMALL prize? (default: {ticket_numbers-2}): ") or (ticket_numbers-2))
    except ValueError:
        print("Invalid input. Using defaults.")
        big, medium, small = ticket_numbers, ticket_numbers-1, ticket_numbers-2
    prizes_config = {
        big: "Biggest prize",
        medium: "Medium prize",
        small: "Small prize"
    }
    print("Prize configuration saved.")
    press_ent()
    return prizes_config

load_config()
start()