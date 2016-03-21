import time, sys, signal, atexit
import pyupm_biss0001 as upmMotion

class MotionSensor:
    def __init__(self, threshold = 0.4):
        # GPIO pin D2
        self.motion = upmMotion.BISS0001(2)
        self.state = 0
        self.average  = 0
        self.threshold = threshold
    
    def getMotionState(self):
        _obtainMotionValue = []
        _delta = 0.
        
        for i in xrange(20):
            _obtainMotionValue.append(self.motion.value())
            time.sleep(0.5)
        
        for i in xrange(len(_obtainMotionValue)):
            if _obtainMotionValue[i]:
                _delta += 1
        
        self.average  =  _delta/len(_obtainMotionValue)
        
        if self.average == 0.0:
            self.state = 0
        elif self.average <= self.threshold/2 and self.average>0:
            self.state = 1
        elif self.average <= self.threshold and self.average>self.threshold/2:
            self.state = 2
        elif self.average > self.threshold:
            self.state = 3

    def __call__(self):
        self.getMotionState()

# Example
#motion = MotionSensor()
#print(motion.getMotionState(),motion.state)
