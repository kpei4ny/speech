#pragma once
#include <windows.h>
#include <fstream>
#include <string>
#include <thread> // ��� ������ � ��������

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
        // ������ ������
        remove(filePath.c_str());

        thread pyThread(run_python_script, pythonCommand);
        thread procThread(process_output_file, filePath);
    }
    ~Speach() {
        pyThread.join();
        procThread.join();
    }
    // ������� ��� ������������� ������ ����
    void scroll(int displacement) {
        INPUT input = {};
        input.type = INPUT_MOUSE;
        input.mi.dwFlags = MOUSEEVENTF_WHEEL;
        input.mi.mouseData = displacement; // ������ �������� - ��������� �����, ��������� - ����
        SendInput(1, &input, sizeof(INPUT));
    }

    // ������� ��� ���������� ������
    void button_press(WORD keyCode) {
        INPUT input = {};
        input.type = INPUT_KEYBOARD;
        input.ki.wVk = keyCode; // ��� ��� ������ (VKF)

        // ������� ������
        SendInput(1, &input, sizeof(INPUT));
        Sleep(20); // �� ����� ���������� ������
        // ³��������� ������
        input.ki.dwFlags = KEYEVENTF_KEYUP;
        SendInput(1, &input, sizeof(INPUT));
    }

    // ������� ��� ������� Python-�������
    void run_python_script(const char* command) {
        int start = system(command);
        if (start == 0) {
            cout << "Python script started successfully" << endl;
        }
        else {
            cerr << "Python file error" << endl;
        }
    }

    // ������� ��� ������� ����� output.txt
    void process_output_file(const string& filePath) {

        while (true) {


            ifstream file(filePath.c_str());


            if (file.is_open()) {
                string currentLine;
                string newLastLine;
                string lastLine; // ����� ��� ���������� ���������� ����� 

                // ������ ���� ����� �� ������
                while (getline(file, currentLine)) {
                    newLastLine = currentLine; // �������� ������� �������� �����
                }
                file.close();
                lastLine = newLastLine; // ��������� ������� �����

                // ���� ����� ����� ����������� �� ������������
                if (!newLastLine.empty()) {
                    //cout << "New line: " << lastLine << endl;

                    // ������� ������
                    if (lastLine.find("next") != string::npos) {
                        ofstream clearing(filePath.c_str());
                        clearing << " ";
                        clearing.close();

                        scroll(-500); // ��������� ����
                        cout << "Scrolled down!" << endl;
                    }
                    else if (lastLine.find("back") != string::npos) {
                        ofstream clearing(filePath.c_str());
                        clearing << " ";
                        clearing.close();

                        scroll(500); // ��������� �����
                        cout << "Scrolled up!" << endl;
                    }
                    else if (lastLine.find("play") != string::npos) {
                        ofstream clearing(filePath.c_str());
                        clearing << " ";
                        clearing.close();

                        button_press(0x20); // �����
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

            Sleep(100); // �������� ��� ��������� ������������

        }
    }
};

