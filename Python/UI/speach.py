import pyaudio
import speech_recognition as sr
import os
import threading


class Choose_Device:
    p = pyaudio.PyAudio()
    necessary_devices = []
    mic = None
    r = sr.Recognizer()
    index = 0

    def __init__(self):
        self.lock = threading.Lock()  # Захист мікрофона від паралельного доступу
        self.filling_necessary_devices()
        Choose_Device.index = 0
        self.set_microphone(Choose_Device.index)

    def filling_necessary_devices(self):
        """Заповнюємо список доступних пристроїв."""
        Choose_Device.necessary_devices.clear()  # Очистити список перед заповненням
        count_of_devices = Choose_Device.p.get_device_count()
        for i in range(count_of_devices):
            name_of_device = Choose_Device.p.get_device_info_by_index(i)["name"]
            formatted_name = self._format_device_name(name_of_device)
            if formatted_name:
                Choose_Device.necessary_devices.append(formatted_name)

    def _format_device_name(self, name_of_device):
        """Видаляє зайві символи з назви пристрою."""
        if "(" in name_of_device:
            return name_of_device.split("(")[1].split(")")[0].strip()
        return name_of_device.strip()

    def set_microphone(self, index):
        """Встановлюємо новий мікрофон."""
        with self.lock:  # Забезпечуємо синхронізацію
            if Choose_Device.mic:
                print("Releasing old microphone.")
                del Choose_Device.mic  # Звільняємо попередній ресурс
            Choose_Device.mic = sr.Microphone(device_index=index)
            print(f"Microphone set to: {Choose_Device.necessary_devices[index]}")

    def change_output_device(self, name_of_chosen_device):
        """Змінюємо пристрій виводу."""
        self.filling_necessary_devices()
        for i, device_name in enumerate(Choose_Device.necessary_devices):
            if device_name == name_of_chosen_device:
                Choose_Device.index = i
                self.set_microphone(i)
                print(f"Device changed to: {device_name}")
                return
        raise ValueError(f"Device '{name_of_chosen_device}' not found.")

    def record_text(self):
        """Слухаємо та повертаємо розпізнаний текст."""
        with self.lock:  # Гарантуємо, що мікрофон доступний лише для одного потоку
            try:
                with Choose_Device.mic as source:
                    print("Listening...")
                    audio = Choose_Device.r.listen(source, timeout=5)  # Обмежуємо час очікування
                    return Choose_Device.r.recognize_google(audio)
            except sr.WaitTimeoutError:
                return "Timeout: No speech detected."
            except sr.UnknownValueError:
                return "Could not understand audio."
            except Exception as e:
                return f"Error: {e}"

    def start_speech(self):
        """Основний цикл розпізнавання."""
        text = self.record_text()
        self.output_text(text)
        return text

    def output_text(self, text):
        """Записуємо текст у файл."""
        try:
            output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text + "\n")
        except IOError as e:
            print(f"Error writing to file: {e}")

    def get_name_of_current_device(self):
        return Choose_Device.necessary_devices[Choose_Device.index]
