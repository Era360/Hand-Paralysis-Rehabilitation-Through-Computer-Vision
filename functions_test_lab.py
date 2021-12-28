import json, os

db_name = 'udb.db'

def check_db(name = db_name):
    if not os.path.isfile(name):
        print('no db \n creating.....')
        udb = open(db_name,'w')
        udb.close()

def read_db():
    try:
        udb = open(db_name, "r")
    except:
        check_db()
        read_db()
    try:
        dicT = json.load(udb)
        udb.close()
        return dicT
    except:
        return {}    

def update_db(newdata, clear=False):
    data = read_db()
    if clear:
        data.clear()
        udb = open(db_name, 'w')
        json.dump(data, udb)
        udb.close()
    else:
        data.update(newdata)
        # wdb = dict(data.items() + newdata.items())    
        udb = open(db_name, 'w')
        json.dump(data, udb)
        udb.close()

def clear_patient(patient):
    whole = read_db()
    whole.pop(patient)
    udb = open(db_name, 'w')
    json.dump(whole, udb)
    udb.close()

def adduser():
    print('add user:')
    name = input('name > ')
    score = int(input('score > '))
    age = int(input('age > '))
    update_db({name:{'score':score, 'age':age}})
    print('successfully added '+ name)

##########################################
user = {
        'Elia': {'score': [2, 4, 2, 10, 11, 21],
                'age': 24},

        'Martha': {'score': [0, 1, 10, 13, 12, 18],
                'age': 35}
        }

cats = {
        'Amina': {'score': [2, 1, 12, 13, 12, 20],
                'age': 45},

        'Simbo': {'score': [23, 20, 12, 26, 30, 31],
                'age': 18}
        }
###########################################

p = [30]
print(sum(p)//len(p))













# import pygame_textinput
# import pygame
# pygame.init()

# # Create TextInput-object
# textinput = pygame_textinput.TextInput()

# screen = pygame.display.set_mode((1000, 200))
# clock = pygame.time.Clock()

# while True:
#     screen.fill((0, 0, 0))

#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.QUIT:
#             exit()
#         # if event.type == pygame.KEYDOWN:
#         #     if event.key == pygame.K_RETURN:
#         #         print(textinput.get_text())
#         #         exit()

#     # Feed it with events every frame
#     textinput.update(events)
#     # Blit its surface onto the screen
#     screen.blit(textinput.get_surface(), (10, 10))

#     pygame.display.update()
#     clock.tick(30)