import time
import pyupm_grove as grove
import math

class LightSensor:
    def __init__(self, threshold = 10.):
        # AIO pin 2
        self.light = grove.GroveLight(2)
        self.normalLight = self.light.raw_value()
        self.state = 0
        self.threshold = threshold

    def getLightState(self):
        _obtainedLightRawList = []
        _deltaList = []
        
        for i in xrange(20):
            _obtainedLightRawList.append(self.light.raw_value())
            time.sleep(0.5)
        
        _prev = _obtainedLightRawList[0]
        
        for i in xrange(len(_obtainedLightRawList)):
            _deltaList.append(math.fabs(_prev-_obtainedLightRawList[i]))
            _prev = _obtainedLightRawList[i]
        self.lightDelta = sum(_deltaList)/len(_obtainedLightRawList)
#        threshold 10
        if sum(_deltaList)/len(_obtainedLightRawList) < self.normalLight/len(_obtainedLightRawList) + self.threshold:
            self.state = 0
        else:
            self.state = 1

    def __call__(self):
        self.getLightState()

# Example
#light = LightSensor()
#light.getLightState()
#print(light.state)