import time
import qi

session = qi.Session()
session.connect("tcp://192.168.1.239:9559")

apl_service = session.service("ALAnimationPlayer")
asr_service = session.service("ALAnimatedSpeech")

# set the local configuration
configuration = {"bodyLanguageMode":"contextual"}

# say the text with the local configuration
# time.sleep(2)
# apl_service.run("animations/Stand/Gestures/YouKnowWhat_1")
apl_service.run("animations/Stand/Emotions/Positive/Embarrassed_1")
# asr_service.say("Hey there!")
# asr_service.say("^start(animations/Stand/Emotions/Positive/Embarrassed_1)")