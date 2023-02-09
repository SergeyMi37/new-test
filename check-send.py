# Программа регулярного чтения датчика температуры и посылки сообщения телеботу
#pip install requests
#pip install --upgrade pip
import requests
import threading
import datetime

def send_telegram(text: str):
    TOKEN="111"
    url = "https://api.telegram.org/bot"
    channel_id = "555"
    url += TOKEN
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })

    if r.status_code != 200:
        #raise Exception("post_text error")
        print("Ошибка",r.status_code)
    else:
        print("Послано удачно")

def f():
    threading.Timer(3600.0, f).start()  # Перезапуск через 3600 секунд - каждый час
    _dt=str(datetime.datetime.today().strftime("%Y-%m-%d_%H.%M"))
    tfile=open("/sys/bus/w1/devices/28-3cade381c52f/w1_slave")
    ttext=tfile.read()
    tfile.close()
    temp=ttext.split("\n")[1].split(" ")[9]
    _temp=float(temp[2:])/1000
    #print(_temp)
    if _temp<15:
        _msg=_dt+" 🚨🚨🚨🚨🚨 Внимание предельный нижний порог темпратуры "+str(_temp)
        send_telegram(_msg)
        print(_msg)
    else:
        _msg="👉"+_dt+" температура "+str(_temp)
        print(_msg)
        send_telegram(_msg)

if __name__ == '__main__':
    send_telegram("👉Старт мониторинга за температурой")
    f()
