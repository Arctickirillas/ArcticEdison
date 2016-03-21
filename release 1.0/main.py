# Party Detector Main
# 12AMI / Volkovich P., Voronina M., Rudakov K.

import time
import threading
from time import gmtime, strftime

import lcd as LCDS
import lightSensor as LS
import soundSensor as SS
import motionSensor as MS
import piezoVibrationSensor as PVS
import soundPlayer as SP
import mraa

import getIP
import sms

# -- Telegram bot
import telebot
token = '192564123:AAGRl-UZkjcre5a6DvdFtnmkxyEqL6CMdTg'
bot = telebot.TeleBot(token)

# -- Connect with FireBase
from firebase import firebase
firebase = firebase.FirebaseApplication('https://arcticedison.firebaseio.com/#', None)

def getPushFromFirebase():
    return firebase.get('','last/notification/push')
def getPullFromFirebase():
    return firebase.get('','last/notification/pull')

def putToFirebase(date, soundSensor, vibrationSensor, moveSensor, lightSensor, soundThreshold, vibrationThreshold, moveThreshold, lightThreshold, status, push, pull, number = "+79601825839"):
    field =  \
    {
    "date" : date,
    "sensor" : {
            "sound" : soundSensor,
            "vibration" : vibrationSensor,
            "move" : moveSensor,
            "light" : lightSensor
                },
    "threshold" : {
            "sound" : soundThreshold,
            "vibration" : vibrationThreshold,
            "move" : moveThreshold,
            "light" : lightThreshold
                },
    "status" : status,
    "number" : number,
    "notification" : {
            "pull" : 0,
            "push" : 0
        }
    }
    prevDate = firebase.get('','last/date')
    prevField = firebase.get('','last')
    firebase.put('',prevDate,prevField)
    firebase.put('','last',field)

class Phone:
    number ="+79601825839"

phone = Phone()

class Threshold:
    sound = 150.
    light = 10.
    vibration = 858.
    motion = 0.4
thresholds = Threshold()

#class Previous:
#    date  = ''
#    field = ''
#prev = Previous()


# -- Initialization Sensors:
# i2c
lcd = LCDS.LCDScreen()
# aio(2)
light = LS.LightSensor()
# aio(1)
mic = SS.MicSound()
# gpio d2
motion = MS.MotionSensor()
# aio(0)
vibration = PVS.PiezoVibration()
# gpio d(6)
touch = mraa.Gpio(6)
touch.dir(mraa.DIR_IN)
# gpio d(5)
buzzer = SP.SoundPlayer()
# gpio d(8)
blueLight = mraa.Gpio(8)
blueLight.dir(mraa.DIR_OUT)
# gpio d(7)
redLight = mraa.Gpio(7)
redLight.dir(mraa.DIR_OUT)

class State:
    stateTitle = 'Normal'
    state = 1
s = State()


# -- State Estimation
def getStates(lightState,micState,motState,vibState):
    if lightState==0 and micState==0 and motState==0  and vibState==0:
        s.stateTitle = 'Silence'
        s.state = 0
    elif (lightState==0  and micState<2  and motState<2 and vibState==0) or \
        (lightState==0 and micState<=2  and motState<1 and vibState==0) or \
        (lightState==0 and micState == 0  and motState<=3 and vibState==0):
            s.stateTitle = 'Normal'
            s.state = 1
    elif lightState==1 and micState<3 and micState>0 and motState>0 and motState<3 and vibState==1:
        s.stateTitle = 'Loud'
        s.state = 2
    elif (lightState==1 and micState==3 and motState>1 and vibState==1) or (micState==3 and vibState==1) or (micState==3):
        s.stateTitle = 'PARTY HARD!!!'
        s.state = 3
    else:
        s.stateTitle = 'Loud'
        s.state = 2

    return s.state,s.stateTitle

def returnOptions():
    return light.lightDelta,mic.thresh,motion.average,vibration.average

# -- Sensor button
class Counter:
    count = 0
    light = 0
    mic = 0
    motion = 0
    vibration = 0
c = Counter()

def changeInfo(args):
    if c.count == 3:
        c.count = 0
    else:
        c.count += 1

    if c.count == 0:
        lcd.setOption('Light', c.light)
    elif c.count == 1:
        lcd.setOption('Sound', c.mic)
    elif c.count == 2:
        lcd.setOption('Motion', c.motion)
    elif c.count == 3:
        lcd.setOption('Vibrtion', c.vibration)


touch.isr(mraa.EDGE_RISING, changeInfo, changeInfo)

def changLightState(light):
    state = 0
    for i in xrange(20):
        state = 1 - state
        light.write(state)
        time.sleep(0.5)

# -- Threads

def startThreads():
    mic.threshold,vibration.threshold,motion.threshold,light.threshold = thresholds.sound,thresholds.vibration,thresholds.motion,thresholds.light
    thL = threading.Thread(target=light)
    thMic = threading.Thread(target=mic)
    thMot = threading.Thread(target=motion)
    thPV = threading.Thread(target=vibration)
    thL.start(),thMic.start(),thMot.start(),thPV.start()
    thL.join(),thMic.join(),thMot.join(),thPV.join()
    
    c.light,c.mic,c.motion,c.vibration = light.lightDelta,mic.thresh,motion.average,vibration.average
    
    s.state, s.stateTitle = getStates(light.state,mic.state,motion.state,vibration.state)
    
    date = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    putToFirebase(date, mic.state,vibration.state, motion.state,light.state,mic.threshold,vibration.threshold,motion.threshold,light.threshold,s.stateTitle, 0, 0, phone.number)
    
    
    lcd.setOption('State',s.stateTitle)
    lcd.setLCDState(s.state)
    
    redLight.write(0),blueLight.write(0)
    if s.state != 3:
        buzzer.playSound(s.state)
    elif s.state == 2:
        changLightState(blueLight),blueLight.write(1)
        buzzer.playSound(s.state)
    elif s.state == 3:
        bot.send_message(149374407,'PARTY HARD!!!')
        sms.sendSMS(phone.number)
        buzzer.playSound(s.state)
        changLightState(redLight),redLight.write(1)


# -- Telegram Bot
token = '192564123:AAGRl-UZkjcre5a6DvdFtnmkxyEqL6CMdTg'
def listener(messages):
    info = 'Hello! My name is arcticEdisonBot!\n'\
    'You can type:\n'\
    '/status - to get the last status,\n'\
    '/rushStatus - to get status immediately,\n'\
    '/estStates - to get the estimated state,\n'\
    '/getWiFiIP - to get wifi ip adress,\n'\
    '/info - to get help.\n\n'\
    '@arcticEdisonBot'
    for message in messages:
        if message.text == '/status':
            status = 'Light: '+str(c.light)+' Sound: '+str(c.mic)+ \
            ' Motion: '+str(c.motion)+' Vibrtion: '+str(c.vibration)
            bot.reply_to(message, status)
        elif message.text == '/rushStatus':
            bot.send_message(message.chat.id, 'Please, wait...')
            startThreads()
            status = 'Light: '+str(c.light)+' Sound: '+str(c.mic)+ \
            ' Motion: '+str(c.motion)+' Vibrtion: '+str(c.vibration)
            bot.reply_to(message, status)
        elif message.text == '/estStates':
            bot.reply_to(message, s.stateTitle)
        elif message.text == '/info':
            bot.reply_to(message, info)
        elif message.text == '/getWiFiIP':
            bot.reply_to(message, getIP.getIP('wlan0'))
        else:
            bot.reply_to(message, 'Type /info for help!')

bot = telebot.TeleBot(token)
bot.set_update_listener(listener)

def startBot():
    bot.polling(none_stop=True, interval=True)
def startMain():
    
    while True:
        startThreads()
        time.sleep(300)

def pushPull():
    while True:
        if getPushFromFirebase() == 1:
            startThreads()
        if getPullFromFirebase() == 1:
            thresholds.sound = (firebase.get('','last/threshold/sound'))
            thresholds.vibration = (firebase.get('','last/threshold/vibration'))
            thresholds.motion = (firebase.get('','last/threshold/move'))
            thresholds.light = (firebase.get('','last/threshold/light'))
            phone.number = (firebase.get('','last/number'))
            startThreads()
        time.sleep(15)

# -- Main
if __name__ == '__main__':
    thBot = threading.Thread(target=startBot)
    thMain = threading.Thread(target=startMain)
    thPP = threading.Thread(target=pushPull)
    thBot.start(),thMain.start(),thPP.start(),thBot.join(),thMain.join(),thPP.join()








  
    
