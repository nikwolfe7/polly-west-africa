# coding=utf-8
import remote_monitor
import defines as d
from collections import Counter
import time

#message = "Ici c'est Polly encore. Nous nous excusons pour le retard hier. Composez 657104235 et raccrocher pour envoyer un message gratuitement a vos amis! Merci!"
#message = 'Bipez à tout moment le 654 308 874 pour écouter des messages de santé important sur Ebola et envoyez-les gratuitement à vos amis'
#message = "PollySanté: Nous excusons pour le retard. Bipez le 654308874 pour écouter un message sur Ébola en Soussou, en Peul, en d'autres langues et l’envoyer à vos amis!"
message = "Svp, bipez 654 308 874. A cause des problèmes d'Internet, Polly Santé ne pouvait pas vous rappelé plus tôt. Désolé. Mais ça marche bien maintenant. Merci!"

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