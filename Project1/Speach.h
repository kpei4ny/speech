#pragma once
#include <windows.h>
#include <fstream>
#include <string>
#include <thread> // Для роботи з потоками

using namespace std;


class Speach{
private:
    //default paths
    const char* pythonCommand = "python3 main.py";
    const string filePath = "output.txt";
    thread pyThread;
    thread procThread;
public:
    Speach() {
        // Запуск потоків
        remove(filePath.c_str());

        thread pyThread(run_python_script, pythonCommand);
        thread procThread(process_output_file, filePath);
    }
    ~Speach() {
        pyThread.join();
        procThread.join();
    }
    // Функція для прокручування колеса миші
    void scroll(int displacement) {
        INPUT input = {};
        input.type = INPUT_MOUSE;
        input.mi.dwFlags = MOUSEEVENTF_WHEEL;
        input.mi.mouseData = displacement; // Додатнє значення - прокрутка вверх, негативне - вниз
        SendInput(1, &input, sizeof(INPUT));
    }

    // Функція для натискання кнопки
    void button_press(WORD keyCode) {
        INPUT input = {};
        input.type = INPUT_KEYBOARD;
        input.ki.wVk = keyCode; // Код для клавіші (VKF)

        // Нажаття клавіші
        SendInput(1, &input, sizeof(INPUT));
        Sleep(20); // Як довго утримується клавіша
        // Відпускання клавіші
        input.ki.dwFlags = KEYEVENTF_KEYUP;
        SendInput(1, &input, sizeof(INPUT));
    }

    // Функція для запуску Python-скрипта
    void run_python_script(const char* command) {
        int start = system(command);
        if (start == 0) {
            cout << "Python script started successfully" << endl;
        }
        else {
            cerr << "Python file error" << endl;
        }
    }

    // Функція для обробки файлу output.txt
    void process_output_file(const string& filePath) {

        while (true) {


            ifstream file(filePath.c_str());


            if (file.is_open()) {
                string currentLine;
                string newLastLine;
                string lastLine; // Змінна для збереження останнього рядка 

                // Читаємо файл рядок за рядком
                while (getline(file, currentLine)) {
                    newLastLine = currentLine; // Зберігаємо останній зчитаний рядок
                }
                file.close();
                lastLine = newLastLine; // Оновлюємо останній рядок

                // Якщо новий рядок відрізняється від попереднього
                if (!newLastLine.empty()) {
                    //cout << "New line: " << lastLine << endl;

                    // Обробка команд
                    if (lastLine.find("next") != string::npos) {
                        ofstream clearing(filePath.c_str());
                        clearing << " ";
                        clearing.close();

                        scroll(-500); // Прокрутка вниз
                        cout << "Scrolled down!" << endl;
                    }
                    else if (lastLine.find("back") != string::npos) {
                        ofstream clearing(filePath.c_str());
                        clearing << " ";
                        clearing.close();

                        scroll(500); // Прокрутка вверх
                        cout << "Scrolled up!" << endl;
                    }
                    else if (lastLine.find("play") != string::npos) {
                        ofstream clearing(filePath.c_str());
                        clearing << " ";
                        clearing.close();

                        button_press(0x20); // пауза
                        cout << "Pause!" << endl;
                    }
                    else if (lastLine.find("mute") != string::npos) {
                        ofstream clearing(filePath.c_str());
                        clearing << " ";
                        clearing.close();

                        button_press(0x4d); // mute
                        cout << "Mute!" << endl;
                    }

                }
                file.close();
            }
            else {
                cerr << "Text file error!" << endl;
            }

            Sleep(100); // Затримка для зменшення навантаження

        }
    }
};

