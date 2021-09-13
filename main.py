from view import *

if __name__ == '__main__':
    requests.get(controller.TELEGRAM_INIT_WEBHOOK_URL)
    app.run(port=5002, debug=True)

