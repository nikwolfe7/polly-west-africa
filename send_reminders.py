# coding=utf-8
import remote_monitor
import defines as d
from collections import Counter
import time

#message = "Ici c'est Polly encore. Nous nous excusons pour le retard hier. Composez 657104235 et raccrocher pour envoyer un message gratuitement a vos amis! Merci!"
message = 'Bipez à tout moment le 654 308 874 pour écouter des messages de santé important sur Ebola et envoyez-les gratuitement à vos amis'

def send_message_to_reminder_list():
    rlist = [l.strip() for l in open(d.reminder_list).readlines()]
    rlist = Counter(rlist)
    for reminder in rlist.keys():
        reminder = reminder.replace(" ","").strip()
        print("Sending SMS to "+reminder+"...")
        print(message)
        remote_monitor.tropo_remote_sms(reminder, str(message))
        time.sleep(1)

if __name__ == '__main__':
    print(str(len(message)) + " chars")
    send_message_to_reminder_list()