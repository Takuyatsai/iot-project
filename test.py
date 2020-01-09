from machine import Pin,PWM
import mfrc522, time, network, urequests

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("Takuya iPhone","123456789") #連結之wifi
while not sta_if.isconnected():
    pass
print("WIFI已連上")
rfid = mfrc522.MFRC522(0, 2, 4, 5, 14)
led = Pin(15, Pin.OUT)
pwm = PWM(Pin(12, Pin.OUT))

def alarmBeep(pwm):
     pwm.freq(1000)     #設定頻率為 1KHz    
     pwm.duty(512)      #設定工作週期為 50%
     time.sleep(1)          #持續時間 1 秒
     pwm.deinit()          #停止發聲
     time.sleep(2)          #持續時間 2 秒
    
while True:
    led.value(0)
    stat, tag_type = rfid.request(rfid.REQIDL)
    if stat == rfid.OK:
        stat, raw_uid = rfid.anticoll()
        if stat == rfid.OK:
            led.value(1)
            id = "%02x%02x%02x%02x" % (raw_uid[0],raw_uid[1],raw_uid[2],raw_uid[3])
            print("偵測到卡號:", id)
            alarmBeep(pwm)
            ifttt_url = "https://maker.ifttt.com/trigger/class/with/key/pSh8EgIL8r9vkeYq7vhptkb8O_4OmkHJYVJXrZs6WTF"
            urequests.get(ifttt_url + "?value1=" +id)
            time.sleep(0.5)

