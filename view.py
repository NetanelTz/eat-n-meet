from urllib import request
import requests
from flask import Flask, Response, request
import controller



app = Flask(__name__)

welcome_msg = 'welcome to eat and meet bot !!'\
               " if you're a new user pls write " \
              " /newuser usarname age and share your location " \
              " else write /user username"



user_name=''
last_search = ''


@app.route('/sanity')
def sanity():
    return "Server is running"

def send_pic():
    try:
        pic='https://c.ndtvimg.com/2020-05/tpj5o4f8_cooking-_625x300_02_May_20.jpg'
        pic_data = requests.get(pic)
        chat_id = request.get_json()['message']['chat']['id']
        requests.post("https://api.telegram.org/bot{}/sendPhoto?chat_id={}"
                     .format(controller.TOKEN, chat_id), files={'photo': pic_data.content})
    except Exception as e:
        print("Error " + str(e))


@app.route('/message', methods=["POST"])
def handle_msg():
    try:
        """
        handle all messages from bot
        :return:
        """
        print("got message")
        global user_name
        global last_search
        return_msg = "unknown command"
        if 'location' in request.get_json()['message'].keys():
            print(user_name)
            controller.add_loc(request.get_json()['message']['location'], user_name)
            return Response("success")
        msg = (request.get_json()['message']['text']).split(" ")
        cmd = msg[0]
        if len(msg) == 2:
            parameter = msg[1]
            if msg[1].isnumeric():
                'NumberController.create(parameter)'
        try:
            if cmd == '/newuser':
                controller.new_user(msg[1], msg[2], '', '')
                return_msg = 'registered successfully'
                return_msg += ' enter /recipe your ingredients  '
                user_name = (msg[1])
            elif cmd == '/recipe':
                # controller.new_search(user_name,msg[1:])
                s=controller.find_recipe(msg[1:])
                return_msg = ' '.join([str(elem) for elem in s])
                return_msg += '\n if you want to eat with friends in your area enter /findfriends ' \
                              'and the dist you willing to go in km'
                last_search=msg[1:]
                send_pic()
            elif cmd == '/start':
                return_msg = welcome_msg
                send_pic()
            elif cmd == '/findfriends':
                print(user_name)
                print(last_search)
                return_msg = controller.find_match_recipes(user_name, last_search,msg[1])
                return_msg+='\n thanks for using eating with friends'
                send_pic()
            elif cmd == '/user':
                return_msg = controller.find_user(msg[1])
                if return_msg == 'user found successfully':
                    user_name = (msg[1])
                    return_msg += ' enter /recipe your ingredients  '

            elif '/newRecipe' in request.get_json()['message']['text']:
                    controller.add_recipe(request.get_json()['message']['text'][11:])
                    return_msg='added successfully'
        except Exception as e:
            return_msg = e
        chat_id = request.get_json()['message']['chat']['id']
        requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}"
                     .format(controller.TOKEN, chat_id, return_msg))
    except Exception as e:
        print("Error " + str(e))
    return Response("success")
