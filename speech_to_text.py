# Python program to translate
# speech to text and text to speech
import speech_recognition as sr
import time
# Initialize the recognizer
def speech_to_text():
    print('listening')
    r = sr.Recognizer()
    # timeout variable can be omitted, if you use specific value in the while condition
    timeout = 10 # [seconds]
    timeout_start = time.time()
    # Loop infinitely for user to
    # speak
    while True:
        
        # Exception handling to handle
        # exceptions at the runtime
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source2:
                
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
                
                #listens for the user's input
                audio2 = r.listen(source2)
                
                # Using google to recognize audio
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                return MyText
    
                print("Did you say ",MyText)
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("unknown error occurred")

speech_to_text()
