from dataclasses import dataclass
from tinydb.operations import increment
from firebase import firebase
import enum
import json
import geopy.distance
firebase = firebase.FirebaseApplication('https://telegrambot-f6ede-default-rtdb.firebaseio.com/', None)
Users = []
keys = []
result = firebase.get('/telegrambot-f6ede-default-rtdb:/Users/', '')

class Recipe:
    instructions = []
    ingredients = []
    title = ""

    def __init__(self, ins, ing, t):
        self.instructions = ins
        self.ingredients = ing
        self.title = t


def new_recipe(ins, ing, t):
    recipe = Recipe(ins, ing, t)
    dict = recipe.__dict__
    firebase.post('/telegrambot-f6ede-default-rtdb:/Recipes/', dict)

# Using enum class create enumerations
class Areas(enum.Enum):
    center = 0
    jerusalem = 1
    north = 2
    south = 3


class User:
    userName = ''
    age: int
    picture = ''
    location=''
    food_search = []

    # constructor
    # def __init__(self, userName, age, picture, area):
    #     # keys are initialized with
    #     # their respective values
    #     self.userName = userName
    #     self.age = age
    #     self.picture = picture
    #     self.area = area
    #     self.food_search = []

    def __init__(self, dict1):
         self.__dict__.update(dict1)

class Suggestion:
    userName = ''
    age: int
    recipe = ''

    def __init__(self, userName, age, recipe):
        self.userName = userName
        self.age = age
        self.recipe = recipe

def find_recpi(products):
     print(products)
     len_p = len(products)
     recpis = firebase.get('/telegrambot-f6ede-default-rtdb:/Recipes/', None)

     for elem in recpis:

         if len_p >= len(elem['ingredients']):
             count = 0
             for item in elem['ingredients']:
                 for j in range(len_p):
                    if item.find(products[j]) >= 0 :
                        count+=1
                        break
             if count == len(elem['ingredients']):
                 return elem
     return 'no match'



def new_user(userName, age, pic, area):
    # user = User(userName, age, pic, area)
    # dict = user.__dict__
    dict= {'userName': userName, 'age': age, 'picture': pic, 'location': '', 'food_search': ''}
    #  dict['food_search'] = list_to_str(user.food_search)
    firebase.post('/telegrambot-f6ede-default-rtdb:/Users/', dict)
    retrieve_data()

def add_search(username, food_search):
    char=''
    for index, user in enumerate(Users):
        if user.userName == username:
            if user.food_search and user.food_search!='' and user.food_search!=[""]:
                char = '$'
            new_food_search = list_to_str(user.food_search) +char+ list_to_str(food_search)
            path = '/telegrambot-f6ede-default-rtdb:/Users/' + keys[index]
            firebase.put(path, 'food_search', new_food_search)
            break


def dict_to_obj(dict1):
    # using json.loads method and passing json.dumps
    # method and custom object hook as arguments
    return json.loads(json.dumps(dict1), object_hook=User)


def retrieve_data():
    if result:
        for key, value in result.items():
            value = dict_to_obj(value)# convert dict to User obj
            value.food_search = value.food_search.split('$')  # convert string to list
          #  value.location = Areas(value.location)# convert int enum Area
            Users.append(value)
            keys.append(key)


def find_match_users(username,max_dist):
    matches = []
    wanted_erea = ''
    for index, user in enumerate(Users):
        if user.userName == username:
            wanted_erea = user.location
            break
    for user in Users:
        if find_dist(user.location , wanted_erea) < int(max_dist) and user.userName != username:
            matches.append(user)
    return matches

def find_dist(coords_1,coords_2):
    if coords_1!='' and coords_2!='':
        coords_1 = tuple(coords_1.split(" "))
        coords_2 = tuple(coords_2.split(" "))
        print(coords_1)
        print(geopy.distance.distance(coords_1,coords_2))
        return geopy.distance.distance(coords_1,coords_2)
    return 10000
def find_user(username):
    for user in Users:
        if user.userName == username:
            return 'user found successfully'
    return 'user was not found'
def list_to_str(lst):
    list_to_str = ''
    for search in lst:
        list_to_str += search
        if lst.index(search) < len(lst) - 1:
            list_to_str += '$'
    return list_to_str


retrieve_data()
# add_search('yosi', ' pizza')
# print(find_matches('abi'))

def add_loc(username, loc):
    for index, user in enumerate(Users):
        if user.userName == username:
            path = '/telegrambot-f6ede-default-rtdb:/Users/' + keys[index]
            firebase.put(path, 'location', loc)
            break