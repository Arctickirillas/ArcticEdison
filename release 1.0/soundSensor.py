import pyupm_mic as upmMicrophone

class MicSound:
    def __init__(self, threshold = 150):
        self.myMic = upmMicrophone.Microphone(1)
        self.state = 0
        self.threshold = threshold
    
    def getNoiseState(self):
        buffer = upmMicrophone.uint16Array(128)
        len = self.myMic.getSampledWindow(100, 128, buffer)
        
        threshContext = upmMicrophone.thresholdContext()
        threshContext.averageReading = 0
        threshContext.runningAverage = 0
        threshContext.averagedOver = 1
        
        self.thresh = self.myMic.findThreshold(threshContext, 30, buffer, len)
        
        if self.thresh<=115:
            self.state = 0
        elif self.thresh>115 and self.thresh<self.threshold-self.threshold/7:
            self.state = 1
        elif self.thresh>=self.threshold-self.threshold/7 and self.thresh<=self.threshold:
            self.state = 2
        elif self.thresh>self.threshold:
            self.state = 3
        else:
            '''Smth wrong!'''

    def __call__(self):
        self.getNoiseState()


# Example
#mic = MicSound()
#mic.getNoiseState()
#print(mic.thresh, mic.state)
