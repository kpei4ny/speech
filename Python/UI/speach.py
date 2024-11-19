import speech_recognition as sr
import threading
import time

r = sr.Recognizer()

def record_text():
    
    while(1):
        try:
            with sr.Microphone() as source2:
                # r.adjust_for_ambient_noise(source2, duration = 0.2)
                audio2 = r.listen(source2)
                r.operation_timeout(100)
                MyText = r.recognize_google(audio2)
                
                return MyText

        except sr.RequestError as e:
            print("Could not request resultsl {0}".format(e))
    
        except sr.UnknownValueError:
            MyText = " "
            return MyText
            
    return




def output_text(text):
    f = open("output.txt", "w")
    if text == 0:
        text = " ";
    f.write(text)
    f.write("\n")
    f.close()
    return

def start_speach():
    while(1):
        text = record_text()
        output_text(text)
        
        print("Wrote text")


speach_thread = threading.Thread(target=start_speach)
speach_thread.start()