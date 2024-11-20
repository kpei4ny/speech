import pyaudio
import speech_recognition as sr

class Choose_Device:

    p = pyaudio.PyAudio()
    current_device = p.get_default_input_device_info()
    index_of_current_device = current_device["index"]

    necessary_devices = []
    index = 0
    r = None
    mic = None

    def __init__(self):
        # Заповнюємо список доступних пристроїв
        self.filling_necessary_devices()

        # Виведення списку пристроїв
        for i, value in enumerate(Choose_Device.necessary_devices):
            print(f"{i}. {value}")

        # Вибір індексу мікрофона
        try:
            mic_index = int(input("Write here the index of the necessary microphone\nwhat do you want to use: "))
            if mic_index < 0 or mic_index >= len(Choose_Device.necessary_devices):
                raise IndexError("Invalid index of the microphone.")
            
            Choose_Device.index = mic_index
            Choose_Device.r = sr.Recognizer()
            Choose_Device.mic = sr.Microphone(device_index=mic_index)
            print(f"Microphone {Choose_Device.necessary_devices[mic_index]} is ready for use.")

        except (ValueError, IndexError) as e:
            print(f"Invalid input. Using default microphone: {Choose_Device.necessary_devices[0]}")
            Choose_Device.index = 0
            Choose_Device.r = sr.Recognizer()
            Choose_Device.mic = sr.Microphone(device_index=0)

    def filling_necessary_devices(self):
        """Заповнюємо список доступних пристроїв."""
        for i in range(self.p.get_device_count()):
            device_info = self.p.get_device_info_by_index(i)
            if device_info["maxInputChannels"] > 0:
                Choose_Device.necessary_devices.append(device_info["name"])

    def record_text(self):
        """Слухаємо та повертаємо розпізнаний текст."""
        try:
            with Choose_Device.mic as source:
                print("Listening...")
                audio = Choose_Device.r.listen(source)
                return Choose_Device.r.recognize_google(audio)

        except sr.RequestError as e:
            print(f"Could not request results: {e}")
            return ""

        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""

    def output_text(self, text):
        """Записуємо текст у файл."""
        try:
            with open("output.txt", "w", encoding="utf-8") as f:
                f.write(text + "\n")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def start_speech(self):
        """Основний цикл розпізнавання."""
        text = self.record_text()
        self.output_text(text)
        print(f"Recognized text: {text}")


