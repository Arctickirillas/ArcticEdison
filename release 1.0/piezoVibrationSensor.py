import time
import array
import pyupm_ldt0028 as ldt0028


class PiezoVibration:
    def __init__(self, threshold = 100):
        # Create the LDT0-028 Piezo Vibration Sensor object using AIO pin 0
        self.sensor = ldt0028.LDT0028(0)
        self.average  = 0
        self.state = 0
        self.text = 'Silence'
        self.threshold = threshold
    
    
    def getState(self):
        _obtainedSampleList = []
        
        for i in xrange(20):
            _obtainedSampleList.append(self.sensor.getSample())
            time.sleep(0.5)
        
        self.average  =  sum(_obtainedSampleList)/len(_obtainedSampleList)

        if self.average >= self.threshold:
            self.state = 1
            self.text = 'Loud clatter!'
        else:
            self.state = 0
            self.text = 'Silence'

    def __call__(self):
        self.getState()

# Example
#p = PiezoVibration()
#p.getState()