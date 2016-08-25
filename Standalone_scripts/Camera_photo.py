#! /usr/bin/env python
# encoding: windows-1250
#
# Res Andy 

import os, re, sys, time, socket, requests
from settings import camaddr
from settings import camport
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging


def main():
    bot_initializer()


#    data = make_photo()
#    pathtophoto = re.findall('fuse_d(.+?)"', data)[0]
#    downloadphoto(pathtophoto)


def make_photo():
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.settimeout(15)
    try:
        srv.connect((camaddr, camport))
    except socket.error, exc:
        print "Caught exception socket.error : %s" % exc
    srv.send('{"msg_id":257,"token":0}')

    data = srv.recv(512)
    if "rval" in data:
        token = re.findall('"param": (.+) }', data)[0]
    else:
        data = srv.recv(512)
        if "rval" in data:
            token = re.findall('"param": (.+) }', data)[0]

    tosend = '{"msg_id":769,"token":%s}' % token
    srv.send(tosend)
    if not "DCIM" in srv.recv(512):
        time.sleep(5)
        responsedata = srv.recv(512)
    else:
        responsedata = srv.recv(512)
    return responsedata


def downloadphoto(path):
    filename = re.findall('(?:.*?\/){3}(.*)', path)[0]
    url = "http://" + camaddr + path
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open("F:\\" + filename, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(bot, update):
    if 'Hi' in update.message.text:
     bot.sendPhoto(chat_id=update.message.chat_id, photo=open('F:\YDXJ0788.jpg', 'rb'))
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Privet")


def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.sendMessage(chat_id=update.message.chat_id, text=text_caps)


def bot_initializer():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    updater = Updater("244382714:AAGzUf3SFmeogXjr85i1hPStZTRI-TG5gHw")
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler([Filters.text], echo)
    caps_handler = CommandHandler('caps', caps, pass_args=True)
    dispatcher.add_handler(caps_handler)
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(start_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()

    # http://192.168.42.1/DCIM/147MEDIA/YDXJ0775.jpg
    # 244382714:AAGzUf3SFmeogXjr85i1hPStZTRI-TG5gHw
