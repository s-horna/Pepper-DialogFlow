import time

import qi
from naoqi import ALProxy

session = qi.Session()
session.connect("tcp://192.168.1.239:9559")
tabletService = session.service("ALTabletService")
try:
    # Display a local web page located in boot-config/html folder
    # The ip of the robot from the tablet is 198.18.0.1
    tabletService.showWebview("http://198.18.0.1/apps/boot-config/preloading_dialog.html")

    time.sleep(3)

    # Javascript script for displaying a prompt
    # ALTabletBinding is a javascript binding inject in the web page displayed on the tablet
    script = """
        var name = prompt("Please enter your name", "Harry Pepper");
        ALTabletBinding.raiseEvent(name)
    """

    # Don't forget to disconnect the signal at the end
    signalID = 0

    # function called when the signal onJSEvent is triggered
    # by the javascript function ALTabletBinding.raiseEvent(name)
    def callback(event):
        print ("your name is: "+ event)
        promise.setValue(True)

    promise = qi.Promise()

    # attach the callback function to onJSEvent signal
    signalID = tabletService.onJSEvent.connect(callback)

    # inject and execute the javascript in the current web page displayed
    tabletService.executeJS(script)

    try:
        promise.future().hasValue(30000)
    except RuntimeError:
        raise RuntimeError('Timeout: no signal triggered')
except Exception as e:
    print(str(e))