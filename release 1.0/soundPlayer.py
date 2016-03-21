import mraa
import time
import pyupm_buzzer as upmBuzzer

# toDo
class SoundPlayer:
    def __init__(self):
#        self.buzzer = mraa.Pwm(5)
        self.buzzer = upmBuzzer.Buzzer(5)
        self.buzzer.stopSound()
    

    def playSound(self,state):
        
        melodyNormal = [upmBuzzer.DO, upmBuzzer.MI, upmBuzzer.SOL]
        melodyLoud = [upmBuzzer.SOL,upmBuzzer.SOL,upmBuzzer.SOL,upmBuzzer.MI]
        

        if state == 1:
            for i,note in enumerate(melodyNormal):
                self.buzzer.playSound(melodyNormal[i], 100000)
                time.sleep(0.2)
            self.buzzer.stopSound()
        elif state == 2:
            for i,note in enumerate(melodyLoud):
                self.buzzer.playSound(melodyLoud[i], 100000)
                time.sleep(0.2)
            self.buzzer.stopSound()
        elif state == 3:
            for i in range(3):
                self.buzzer.playSound(1, 5000000)
                self.buzzer.playSound(500, 5000000)
            self.buzzer.stopSound()
        else:
            self.buzzer.stopSound()

    def stopSound(self):
        self.buzzer.stopSound()



#                value = 0.7
#                note = noteFrequencies[noteMIDIKeys.index(i)]
#                print(note)
#                self.buzzer.write(value)
#                self.buzzer.period_us(int((10**6)/note))
#                self.buzzer.enable(True)
#                time.sleep(0.2)
#                self.buzzer.enable(False)


#        chords = [upmBuzzer.DO, upmBuzzer.RE, upmBuzzer.MI, upmBuzzer.FA,\
#                upmBuzzer.SOL, upmBuzzer.LA, upmBuzzer.SI, upmBuzzer.DO,upmBuzzer.SI];
#        for chord_ind in range (0,7):
#                # play each note for one second
#                print self.buzzer.playSound(chords[chord_ind], 100000)
#                time.sleep(0.1)


# Example
#s = SoundPlayer()
#while True:
#        s.toPlaySound(0)
#del s