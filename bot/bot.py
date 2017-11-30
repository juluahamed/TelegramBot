import json
import requests
import time
import urllib
from bot import ssh_paramiko
from bot.models import Transaction
from bot.sendsms import send

TOKEN = "503272342:AAErMqu04JmlmFen9pYX9dlhmFVrq8Y7Ypg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def health_check(chat,text=None, tr_type='D'):
    command = "mpstat | grep 'all'"
    result, status = ssh_paramiko.run(command=command)
    print("Printing Result and status")
    print(result, status)
    if status == 0:
        print(result)
        result_array = result.strip().split()
        reply = "CPU Stats(in %): \nUser(Application level): " + str(result_array[3]) + \
                 "\nSystem: " + str(result_array[5]) + \
                 "\nIdle : " + str(result_array[12])
        new_tr =Transaction(status='S', chat_id=chat, text=text, response=reply, tr_type=tr_type)
        new_tr.save()
        send_message(reply, chat, custom_keyboard())
        if tr_type == 'A':
            send(reply)
    else:
        reply = "Could not fetch CPU info"
        new_tr =Transaction(status='F', chat_id=chat, text=text, response=reply, tr_type=tr_type)
        new_tr.save()
        send_message(reply, chat, custom_keyboard())

    command = "vmstat -s | awk '{print $1}'"
    result, status = ssh_paramiko.run(command=command)
    if status == 0:
        result_array = result.strip().split()
        reply = "Memory Stats(in KB)\n"  + \
                "Total: " + result_array[0] + \
                "\n Used: " + result_array[1] + \
                "\n Active: " + result_array[2] + \
                "\n Inactive: " + result_array[3] + \
                "\n Free: "+ result_array[4] + \
                "\n Buffer: " + result_array[5] + \
                "\n Swap Cache: " + result_array[6] + \
                "\n Total Swap: " + result_array[7]
        new_tr =Transaction(status='S', chat_id=chat, text=text, response=reply, tr_type=tr_type)
        new_tr.save()
        send_message(reply, chat, custom_keyboard())
        if tr_type == 'A':
            send(reply)
    else:
        reply = "Could not fetch Memory info"
        new_tr =Transaction(status='F', chat_id=chat, text=text, response=reply, tr_type=tr_type)
        new_tr.save()
        send_message(reply, chat, custom_keyboard())

def handle_update(update):
    try:
        text = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        print("chat_id")
        print(chat)
        if text == 'Health Check':
            health_check(chat,text,tr_type='D')

        elif text == 'Running Processes':
            command = "pidstat | awk '{print $10}'"
            result, status = ssh_paramiko.run(command=command)
            if status == 0:
                reply = "Active running processes are: \n" + '\n'.join(result.strip().split()[1:-1])
                new_tr =Transaction(status='S', chat_id=chat, text=text, response=reply, tr_type='D')
                new_tr.save()
                send_message(reply, chat, custom_keyboard())
            else:
                reply = "Could not fetch Running processes info"
                new_tr =Transaction(status='F', chat_id=chat, text=text, response=reply, tr_type='D')
                new_tr.save()
                send_message(reply, chat, custom_keyboard())

        elif text == 'Run Command':
            new_tr =Transaction(status='S',chat_id=chat, text=text, response="Type a command to run", tr_type='D')
            new_tr.save()
            send_message("Type a command to run", chat, None)

        elif text == '/start':
            new_tr =Transaction(status='S',chat_id=chat, text=text, response="Welcome! Lets get to work", tr_type='D')
            new_tr.save()
            send_message("Welcome! Lets get to work", chat, None)

        else:
            print("inside last tr")
            last_tr = Transaction.objects.filter(chat_id=chat).order_by('-timestamp')[0]
            print(last_tr.text)
            if last_tr.text == 'Run Command':
                print(last_tr.text)
                result, status = ssh_paramiko.run(command=text)
                if status == 0:
                    new_tr =Transaction(status='S',chat_id=chat, text=text, response=result, tr_type='D')
                    new_tr.save()
                    send_message(result, chat, custom_keyboard())
                else:
                    new_tr =Transaction(status='F',chat_id=chat, text=text, response="Could not run the command", tr_type='D')
                    new_tr.save()
                    send_message("Could not run the command", chat, custom_keyboard())
            else:
                new_tr =Transaction(status='F',chat_id=chat, text=text, response="Sorry, I cant understand that command", tr_type='D')
                new_tr.save()
                send_message("Sorry, I cant understand that command", chat, custom_keyboard())

    except KeyError:
        auto_update = update.get('auto', None)
        if auto_update:
            chat_id = 505582207
            health_check(chat_id,"Crontab Request",'A')
        else:
            pass

def custom_keyboard():
    keyboard = [['Health Check'],['Running Processes'], ['Run Command']]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def send_message(text, chat_id, reply_markup):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

