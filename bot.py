import sys
import time
import urllib3
from amanobot import Bot
from amanobot.loop import MessageLoop
from amanobot.exception import TelegramError
from config import token, url

try:
    open("bot-disabled")
except FileNotFoundError:
    pass
else:
    print("The bot is disabled. Try removing the bot-disabled file.")
    sys.exit()


bot = Bot(token)
me = bot.getMe()


def is_admin(chat_id, user_id):
    adms = bot.getChatAdministrators(chat_id)

    adm_id = [i["user"]["id"] for i in adms]
    return user_id in adm_id


def add_chat(chat_id):
    try:
        chats = set(open("chats.txt").read().splitlines())
    except FileNotFoundError:
        open("chats.txt", "w")
        chats = set()

    chats.add(str(chat_id))
    with open("chats.txt", "w") as f:
        f.write("\n".join(chats))


def get_chats():
    try:
        chats = set(open("chats.txt").read().splitlines())
    except FileNotFoundError:
        open("chats.txt", "w")
        chats = set()
    return chats


def remove_chat(chat_id):
    try:
        chats = set(open("chats.txt").read().splitlines())
    except FileNotFoundError:
        open("chats.txt", "w")
        chats = set()

    chats.remove(str(chat_id))
    with open("chats.txt", "w") as f:
        f.write("\n".join(chats))


def handle(msg):
    if msg.get("text") == "/start" or msg.get("text") == "/start@" + me["username"]:
        if msg["chat"]["type"] == "private" or is_admin(msg["chat"]["id"], msg["from"]["id"]):
            bot.sendMessage(msg["chat"]["id"], "Hello! This is a simple bot to notify when a new Android release comes.\n"
                                               "To be notified, use the command /notify.\n\n"
                                               "Currently I'm tracking: {}.\n\n"
                                               "<a href='https://github.com/AlissonLauffer/ReleasesBot'>Source code</a>".format(url),
                            parse_mode="HTML")

    elif msg.get("text") == "/notify" or msg.get("text") == "/notify@" + me["username"]:
        if msg["chat"]["type"] == "private" or is_admin(msg["chat"]["id"], msg["from"]["id"]):
            add_chat(msg["chat"]["id"])
            bot.sendMessage(msg["chat"]["id"], "Ok. You will be notified about new Android releases on this chat.\n"
                                               "If you don't want anymore use the /do_not_notify command.")

    elif msg.get("text") == "/do_not_notify" or msg.get("text") == "/do_not_notify@" + me["username"]:
        if msg["chat"]["type"] == "private" or is_admin(msg["chat"]["id"], msg["from"]["id"]):
            remove_chat(msg["chat"]["id"])
            bot.sendMessage(msg["chat"]["id"], "Ok. I removed this chat from the list.")


MessageLoop(bot, handle).run_as_thread()

http = urllib3.PoolManager()

while True:
    try:
        r = http.request("GET", url)
    except:
        # If some error occours, try again.
        continue
    print("Status", r.status)

    # If status is 200, send broadcast messages, write the bot-disabled file and then exit.
    if r.status == 200:
        for chat in get_chats():
            try:
                bot.sendMessage(chat, url.split("/")[-1] + " is available!\n\n" + url)
            except TelegramError:
                pass
        open("bot-disabled", "w")
        sys.exit()
    time.sleep(5)
