import model
# from model import NumberModelWrapper
import sympy
import geopy.distance
# script to control operation of view
# define bot token and server
TOKEN = '1971539316:AAErYTSvg9umoTMJ5alRTtnVbb7PUEmIRlI'
NGROK = 'https://1652744a8fb3.ngrok.io'
TELEGRAM_INIT_WEBHOOK_URL = 'https://api.telegram.org/bot{}/setWebhook?url={}/message'.format(TOKEN, NGROK)


def new_user(usarname, age, pic, area):
    # int_erea = 0
    # if area == 'jerusalem':
    #     int_erea = 1
    # elif area == 'north':
    #     int_erea = 2
    # elif area == 'south':
    #     int_erea = 3
    model.new_user(usarname, age, pic, '')


def new_search(user_name, new_search):
    model.add_search(user_name, new_search)
    # return recipes


def add_recipe(msg):
    tmp = msg.split('\n')
    model.new_recipe(tmp[0], tmp[1], tmp[2])


def find_recipe(new_search, exist_search=[]):
    return_msg=''
    if isinstance(new_search, str):
        new_search=new_search.split(' ')
    if isinstance(exist_search, str):
        exist_search = exist_search.split(' ')
    if exist_search and exist_search!='' and exist_search!=['']:
          new_search=new_search+exist_search
    ans=model.find_recpi(new_search)
    if ans =='no match':
        return ans
    for title, val in model.find_recpi(new_search).items():  # convert to string
        return_msg += title + ':\n' + str(val) + '\n'
    if return_msg.find('&') != -1:
        return_msg = return_msg[:return_msg.find('&') - 1] + return_msg[return_msg.find('&') + 1:]
    return return_msg

def find_match_recipes(user_name, new_search,max_dist):
    new_search = model.list_to_str(new_search).replace('$', ' ')
    match_users = model.find_match_users(user_name,max_dist)
    suggestions = ''
    for num, user in enumerate(match_users):
        suggestions += '\n suggestion ' + str(num+1) + ' @' + user.userName + ' age: ' + user.age + '\n' + \
                       find_recipe(new_search, user.food_search[-1])+'\n'

    return suggestions


def find_user(username):
    return model.find_user(username)

def add_loc(loc, user):
    tmp = str(loc['latitude'])+' '+str(loc['longitude'])
    model.add_loc(user, tmp)

# model.retrieve_data()
# new_user('abi', 12, 'asd', 1)
# new_user('yosi', 12, 'asd', 1)
# new_search('yosi','pizza')
# new_search('abi','hamburger')
# y = find_match_recipes('abi', 'grape')
# x = 4
