# coding=utf-8
import remote_monitor

message = "Ici, c'est Polly encore. Composez 657104235 et raccrochez n'impote quand pour faire des effets marrants avec voix et les envoyer a vos amis gratuitement"

def send_message_to_reminder_list():
    rlist = [l.strip() for l in open("reminder_list.txt").readlines()]
    for reminder in rlist:
        reminder = reminder.replace(" ","").strip()
        print("Sending SMS to "+reminder+"...")
        remote_monitor.tropo_remote_sms(reminder, message)

if __name__ == '__main__':
    send_message_to_reminder_list()