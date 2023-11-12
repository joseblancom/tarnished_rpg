from cred import external_passwrd, external_database
from character_creator import Character, Mago, Enemy
import mysql.connector
import os
import re
import time
import datetime
import hashlib
import random


db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= external_passwrd,
    database= external_database
)

mycursor = db.cursor()
today = datetime.datetime.now()

#player = "X"
#coords = {"y": 0, "x": 0}

#dark_forest = []

#dark_forest[coords["y"]][coords["x"]] = player


def print_title():
    print("""
___ ____ ____ _  _ _ ____ _  _ ____ ___     ____ ___  ____ 
 |  |__| |__/ |\ | | [__  |__| |___ |  \    |__/ |__] | __ 
 |  |  | |  \ | \| | ___] |  | |___ |__/    |  \ |    |__] 

""")
    
def print_login_2():
    print("""
_    ____ ____ _ _  _ 
|    |  | | __ | |\ | 
|___ |__| |__] | | \| 
                
""")
    
def print_sword():
    print("""
         />_________________________________
[########[]_________________________________>
         \>
""")
    
def print_menu():
    print("""
_  _ ____ _  _ _  _ 
|\/| |___ |\ | |  | 
|  | |___ | \| |__| 
                    
""")

def hashing_256(password):
    return hashlib.sha256(password.encode())


def check_symbol(string_to_check):
    return bool(re.search("[$@_!#%^:&*(.)<>?/\|\-}{~]", string_to_check))


def check_space(string_to_check):
    return bool(re.search("\s", string_to_check))


def check_length(string_to_check, mininum, maximun):
    return len(string_to_check) >= mininum and len(string_to_check) <= maximun


def select_username(username):
    try:
        mycursor.execute(f"SELECT username FROM users WHERE username = '{username}'")
        myresult = mycursor.fetchone()
        return myresult[0]
    except:
        pass

def select_user_id(username):
    try:
        mycursor.execute(f"SELECT id FROM users WHERE username = '{username}'")
        myresult = mycursor.fetchone()
        return myresult[0]
    except:
        pass

def select_password_from_username(username):
    try:
        mycursor.execute(f"SELECT password FROM users WHERE username = '{username}'")
        myresult = mycursor.fetchone()
        return myresult[0]
    except:
        pass

def print_login():
    print("--------------------------------")
    print(f"#     __             _         #\n#    / /  ___  ___ _(_)__      #\n#   / /__/ _ \/ _ `/ / _ \\     #\n#  /____/\___/\_, /_/_//_/     #\n#            /___/             #")
    print("--------------------------------")


def is_valid_username(username, counter):
    while True:
        length = no_symbol = no_space = user_available = False
        mensaje = ""

        if username == "":
            username = input("Ingrese su nombre de usuario: ")

            if username == select_username(username):
                mensaje = "Nombre de usuario ya existe, intente con otro"
                user_available = False
            else:
                user_available = True
        
        no_symbol = not check_symbol(username)
        no_space = not check_space(username)
        length = check_length(username,4,10)

        if length & no_symbol & no_space & user_available == True:
            os.system("cls")
            return username
        else:
            username = ""
            counter += 1
            os.system("cls")
            print("PASO 1: Nombre de usuario ------------------------- Intento Nº: "+str(counter)+"\n\nEl nombre de usuario debe cumplir con lo siguiente:\n - Contener entre 4 a 10 caracteres\n - No debe contener espacios\n - No debe contener carácteres especial: $@_!#%^:&*(.)<>?/\|-}{~")
            print(f"\n{mensaje}\n----------------------------------------------------------------\n")


def is_valid_password(password, counter):
    while True:
        uppercase = length = lowercase = numbers = symbol = False
        
        if password == "":
            password = input("Crea una contraseña: ")

        lowercase = bool(re.search("[a-z]", password))
        uppercase = bool(re.search("[A-Z]", password))
        symbol = check_symbol(password)
        length = check_length(password, 8, 25)
        numbers = any(char.isdigit() for char in password)

        if numbers & length & lowercase & uppercase & symbol:
            os.system("cls")
            print(f"Usuario creado con éxito uwu")
            return password
            
        else:
            password = ""
            counter += 1
            os.system("cls")
            print("PASO 2: Contraseña ------------------------------- Intento Nº: "+str(counter)+"\n\nLa contraseña debe cumplir con lo siguiente:\n - Mínimo 8 caracteres\n - Una letra en mayúsculas: ABC...\n - Una letra en minúscula: abc...\n - Un número: 123...\n - Un carácter especial: $@_!#%^:&*(.)<>?/\|-}{~")
            print("\n----------------------------------------------------------------\n")

def login():
    mensaje = ""
    while True:
        os.system("cls")
        
        print(mensaje)
        print_login_2()

        username = input(f"Nombre de Usuario: ")
        password = input(f"Password: ")
        password_hashed = hashing_256(password).hexdigest()

        if username == select_username(username) and select_password_from_username(username) == password_hashed:
            print("Logeado con éxito")
            return select_username(username)
        else:
            mensaje = "Usuario o contraseña incorrecta, intente nuevamente"


def login_or_registry():
    while True:
        mensaje = ""
        os.system("cls")
        print_title()
        answer = input(" 1. Login\n 2. Registrarse\n 3. Salir\n\nEscriba su opción: ")
        if answer == "1":
            username = login()
            return username
        elif answer == "2":
            username = is_valid_username("x", 0)
            password = is_valid_password("x", 0)
            password_hashed = hashing_256(password).hexdigest()

            mycursor.execute(f"INSERT INTO users (username, password, created) VALUES (%s, %s, %s)", (username, password_hashed, today));
            db.commit()

            for i in range(3,0,-1):
                os.system("cls")
                print(f"Usuario creado con éxito.\n\nSerás devuelto al menú en {i} segundos...")
                time.sleep(1)

        elif answer == "3":
            os.system("cls")
            print("!Hasta luego!")
            break


    
def character_creator():
    while True:
        os.system("cls")
        character_name = input("Ingrese el nombre de su personaje: ")

        os.system("cls")
        race = input("Razas:\n\n 1. Humano\n 2. Elfo\n\nEscriba su opción: ")
        if race == str(1):
            race = "Humano"
        elif race == str(2):
            race = "Elfo"

        os.system("cls")
        class_name = input("Clases:\n\n 1. Mago\n\nEscriba su opción: ")
        if class_name == str(1):
            class_name = "Mago"
            return Mago(character_name, class_name, race)
        
def create_or_play_menu(user_id):
    while True:
        os.system("cls")
        option = input("\n 1. Crear Personaje\n 2. Jugar\n\nEscriba su opción: ")
        if option == str(1):
            new_character = character_creator()
            mycursor.execute(f"INSERT INTO characters (user_id, character_name, character_class, race, lvl, exp) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, new_character.character_name, new_character.class_name, new_character.race, new_character.lvl, new_character.exp));
            db.commit()

            for i in range(3,0,-1):
                os.system("cls")
                print(f"Personaje creado con éxito.\n\nSerás devuelto al menú en {i} segundos...")
                time.sleep(1)
            
        if option == str(2):
            return play(user_id)


def select_character_info(option, characters_account):
    mycursor.execute(f"SELECT * from characters where character_name = '{characters_account[int(option)-1]}'")
    character_selected = mycursor.fetchall()
    return list(character_selected[0])


def play(user_id):
    mycursor.execute(f"SELECT character_name from characters where user_id = {user_id}")
    myresult = mycursor.fetchall()
    characters_account = [character[0] for character in myresult]

    print("Selecciona tu personaje: \n")

    for index, character in enumerate(characters_account, start=1):
        print(f"{index}. {character}")
    
    valid_options = [str(i) for i in range(1, len(characters_account) +1)]
    option = input("\nEscriba su opción: ")

    if option in valid_options:
        character_selected = select_character_info(option, characters_account)
        print(f"Has seleccionado a {character_selected[2]} ({character_selected[3]} - lvl {character_selected[5]})")
        return character_selected
    else:
        print("Opción inválida")



def main_menu():
    while True:
        os.system("cls")
        print_menu()
        option = input(" 1. Explorar\n\nEscriba su opción: ")

        if option == str(1):
            return explorar_menu()

def explorar_menu():
    os.system("cls")
    print("¿Que zona del mapa desea explorar?")
    zone = input("\n 1. Dark Forest\n\nEscriba su opción: ")

    if zone == str(1):
        zone = "Dark Forest"
        return zone

def battle(mob, player_hp):
    enemy_damage = your_damage = ""
    total_your_damage = total_enemy_damage = 0
    #player_hp = loaded_character.hp
    while player_hp > 0 or mob.hp > 0:
        os.system("cls")
        print(f"{loaded_character.character_name} HP:{player_hp}  (-{enemy_damage})   |     {mob.enemy_name} HP:{mob.hp}  (-{your_damage})")
        print(f"\n\n 1. Magic attack\n")

        action = input("Ingrese su opción: ")

        if player_hp > 0:
            if action == "1":
                your_damage = random.choice([*range(round(loaded_character.intelligence/2), loaded_character.intelligence)]) 
                mob.hp = mob.hp - your_damage
                total_your_damage = total_your_damage + your_damage
                
                if mob.hp > 0:
                    enemy_damage = random.choice(mob.attack)
                    player_hp = player_hp - enemy_damage
                    total_enemy_damage = total_enemy_damage + enemy_damage
                elif mob.hp <= 0:
                    exp_gained = random.choice(mob.EXP)
                    return total_enemy_damage, exp_gained
                
        if player_hp <= 0:
            return "Defeated"

def movement(move, map_name, coords, player):
    if move == "w":
        if map_name[coords["y"]-1][coords["x"]] == ".":
            coords["y"] = coords["y"] - 1
            map_name[coords["y"]][coords["x"]] = player
            map_name[coords["y"]+1][coords["x"]] = "."
        elif map_name[coords["y"]-1][coords["x"]] == "?":
            coords["y"] = coords["y"] - 1
            map_name[coords["y"]][coords["x"]] = player
            map_name[coords["y"]+1][coords["x"]] = "."
            return True

    elif move == "s":
        if map_name[coords["y"]+1][coords["x"]] == ".":
            coords["y"] = coords["y"] + 1
            map_name[coords["y"]][coords["x"]] = player
            map_name[coords["y"]-1][coords["x"]] = "."
        elif map_name[coords["y"]+1][coords["x"]] == "?":
            coords["y"] = coords["y"] + 1
            map_name[coords["y"]][coords["x"]] = player
            map_name[coords["y"]-1][coords["x"]] = "."
            return True
        
    elif move == "a":
        if map_name[coords["y"]][coords["x"]-1] == ".":
            coords["x"] = coords["x"] - 1
            map_name[coords["y"]][coords["x"]] = player
            map_name[coords["y"]][coords["x"]+1] = "."
        elif map_name[coords["y"]][coords["x"]-1] == "?":
            coords["x"] = coords["x"] - 1
            map_name[coords["y"]][coords["x"]] = player
            map_name[coords["y"]][coords["x"]+1] = "."
            return True
        
    elif move == "d":
        if map_name[coords["y"]][coords["x"]+1] == ".":
            coords["x"] = coords["x"] + 1
            map_name[coords["y"]][coords["x"]] = player
            map_name[coords["y"]][coords["x"]-1] = "."
        elif map_name[coords["y"]][coords["x"]+1] == "?":
            coords["x"] = coords["x"] + 1
            map_name[coords["y"]][coords["x"]] = player
            map_name[coords["y"]][coords["x"]-1] = "."
            return True


#mago = Mago("Paksigue", "Mago", "Elfo")

def loaded_character(character_selected):
    if character_selected[3] == "Mago":
        return Mago(character_selected[2], character_selected[3], character_selected[4])
    else:
        return "No soy mago"
    
def map_result(exp):
    os.system("cls")
    print(f"Has ganado un total de {exp} experiencia")
    input("\nPresiona Enter para continuar...")

def character_lvl(character_name):
    mycursor.execute(f"SELECT lvl from characters where character_name = '{character_name}'")
    myresult = mycursor.fetchone()
    return myresult[0]

def character_exp(character_name):
    mycursor.execute(f"SELECT exp from characters where character_name = '{character_name}'")
    myresult = mycursor.fetchone()
    return myresult[0]

checking_map = []
def map_completed(checking_map):
    if "?" not in checking_map:
        return True
    
def dark_forest_function(main_option):
    exp_gained = 0
    player_hp = loaded_character.vigor
    player = "X"
    coords = {"y": 3, "x": 1}

    dark_forest = [
        ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"],
        ["#","#","?",".",".",".",".",".",".",".",".","#",".",".",".",".",".",".",".","#"],
        ["#","#","#","#","#",".","#","#","#",".",".",".",".","#",".",".",".",".",".","#"],
        ["#",".",".",".","#",".","#","#","#",".",".",".",".",".",".",".",".","#","#","#"],
        ["#",".",".",".",".",".",".",".","#","#",".",".","#",".",".",".","#","#","#","#"],
        ["#",".","#",".",".",".",".",".",".",".","#",".",".",".",".","?","#","#","#","#"],
        ["#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#","#"]
    ]

    dark_forest[coords["y"]][coords["x"]] = player

    if main_option == "Dark Forest":
        imp = Enemy("Imp", [*range(1,2)], 15, [*range(20,25)])
        troll = Enemy("Troll", [*range(1,2)], 20, [*range(35,50)])

        while True:
            checking_map.clear()
            mob = battle_result = ""
            os.system("cls")
            print(coords)
            print("\n")

            for row in dark_forest:
                for i in row:
                    print(i, end=" ")
                    checking_map.append(i)
                print()
            
            if map_completed(checking_map) == True:
                os.system("cls")
                print(f"Victoria! Has eliminado a todos los mobs del mapa")
                input("\nPresiona Enter para continuar...")
                map_result(exp_gained)
                exp_to_db(loaded_character.character_name, exp_gained)
                leveling_up(loaded_character.character_name)
                break

            print("\n")
            print(f"current HP: {player_hp}   |   Exp gained: {exp_gained}")
            print("\n")
            move = input("Escriba una dirección (w/a/s/d): ")
            mob = movement(move, dark_forest, coords, player)
            if mob == True and coords["y"] == 1 and coords["x"] == 2:
                battle_result = battle(imp, player_hp)
                player_hp = player_hp - battle_result[0]
                exp_gained = exp_gained + battle_result[1]
            elif mob == True and coords["y"] == 5 and coords["x"] == 15:
                battle_result = battle(troll, player_hp)
                player_hp = player_hp - battle_result[0]
                exp_gained = exp_gained + battle_result[1]

            if battle_result == "Defeated":
                print(f"Has sido derrotado")
                input("\nPresiona Enter para continuar...")
                break

def leveling_up(character_name):
    if character_exp(character_name) >= 100:
        mycursor.execute(f"UPDATE characters set lvl = '2' where character_name = '{character_name}'")
        db.commit()

        lvl = character_lvl(character_name)

        print(f"Avanzaste a lvl {lvl}")

def exp_to_db(character_name, exp_gained):
    total_exp = character_exp(character_name)
    total_exp = total_exp + exp_gained

    mycursor.execute(f"UPDATE characters set exp = '{total_exp}' where character_name = '{character_name}'")
    db.commit()

login_username = login_or_registry()
user_id = select_user_id(login_username)
character_selected = (create_or_play_menu(user_id))
loaded_character = loaded_character(character_selected)

print(f"Esto vale loaded_character: {loaded_character.character_name}")
input("wait")


while True:
    main_option = main_menu()
    if main_option == "Dark Forest":
        map_1 = dark_forest_function(main_option)
        #a = [*range(round(loaded_character.intelligence/2), loaded_character.intelligence)]
        #print(f"a vale lo siguiente: {a}")
        #input("test")















""" print(character_selected)
        print(loaded_character)
        print(loaded_character.character_name)
        print(loaded_character.class_name)
        print(loaded_character.race)
        print(loaded_character.lvl)
        print(loaded_character.basic_attack)
        print(loaded_character.hp)
        
        print(golem.enemy_name)
        print(golem.attack)
        print(golem.hp)
        print(golem.lvl) """



#def main_menu():
#    while True:
#        os.system("cls")
#        answer = input("\n 1. Crear personaje\n 2. Continuar juego\n 3. Salir\n\nEscriba su opción: ")



#staff = [*range(1,6)]
#damage = random.choice(staff)
#print(damage)


 
#print(new_character.__dict__)
#print(new_character.__dict__["character_name"])
#print(new_character.__dict__["class_name"])
#print(new_character.__dict__["race"])
#print(new_character.__dict__["lvl"])


#mago = Mago("Paksigue", "Mago", "Elfo")
'''
print(mago.character_name)
print(mago.class_name)
print(mago.race)
print(mago.lvl)
print(mago.magic_attack)
print(mago.hp)
'''


#golem = Enemy("Golem", [*range(1,2)], 25, [*range(20,26)])
'''
print(golem.enemy_name)
print(golem.attack)
print(golem.hp)
print(golem.lvl)
'''


'''
enemy_damage = your_damage = ""
total_your_damage = total_enemy_damage = 0

while mago.hp > 0 or golem.hp > 0:
    os.system("cls")
    print(f"{mago.character_name} HP:{mago.hp}  (-{enemy_damage})   |     {golem.enemy_name} HP:{golem.hp}  (-{your_damage})")
    print(f"\n\n 1. Magic attack\n")

    action = input("Ingrese su opción: ")

    if mago.hp > 0:
        if action == "1":
            your_damage = random.choice(mago.basic_attack)
            golem.hp = golem.hp - your_damage
            total_your_damage = total_your_damage + your_damage
            
            if golem.hp > 0:
                enemy_damage = random.choice(golem.attack)
                mago.hp = mago.hp - enemy_damage
                total_enemy_damage = total_enemy_damage + enemy_damage
            elif golem.hp <= 0:
                os.system("cls")
                print(f"Victoria")
                break
    elif mago.hp <= 0:
        print(f"Derrota")
        break
'''
       

