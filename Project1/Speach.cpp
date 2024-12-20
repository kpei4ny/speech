#include "Speach.h"

Speach::Speach() {
    remove(filePath.c_str());  // Remove the file if it exists

    // Create threads
    pyThread = thread(&Speach::run_python_script, this);
    procThread = thread(&Speach::process_output_file, this);
}

Speach::~Speach() {
    // Wait for threads to finish before destroying the object
    pyThread.join();
    procThread.join();
}

void Speach::scroll(int displacement) {
    INPUT input = {};
    input.type = INPUT_MOUSE;
    input.mi.dwFlags = MOUSEEVENTF_WHEEL;
    input.mi.mouseData = displacement;
    SendInput(1, &input, sizeof(INPUT));
}

void Speach::button_press(WORD keyCode) {
    INPUT input = {};
    input.type = INPUT_KEYBOARD;
    input.ki.wVk = keyCode;

    // Press the key
    SendInput(1, &input, sizeof(INPUT));
    Sleep(20);  // Hold the key for 20ms
    // Release the key
    input.ki.dwFlags = KEYEVENTF_KEYUP;
    SendInput(1, &input, sizeof(INPUT));
}

void Speach::run_python_script() {
    int start = system(pythonCommand);  // Run the Python script
    if (start == 0) {
        cout << "Python script started successfully" << endl;
    }
    else {
        cerr << "Python script error" << endl;
    }
}

void Speach::process_output_file() {
    string lastLine;  // Last read line

    while (true) {
        ifstream file(filePath.c_str());

        if (file.is_open()) {
            string currentLine;
            string newLastLine;

            // Read file line by line
            while (getline(file, currentLine)) {
                newLastLine = currentLine;  // Store the last line read
            }

            file.close();

            // If the line has changed, process it
            if (!newLastLine.empty() && newLastLine != lastLine) {
                lastLine = newLastLine;  // Update last line

                // Handle commands in the last line
                if (lastLine.find("next") != string::npos) {
                    ofstream clearing(filePath.c_str());
                    clearing << " ";
                    clearing.close();
                    scroll(-500);  // Scroll down
                    cout << "Scrolled down!" << endl;
                }
                else if (lastLine.find("back") != string::npos) {
                    ofstream clearing(filePath.c_str());
                    clearing << " ";
                    clearing.close();
                    scroll(500);  // Scroll up
                    cout << "Scrolled up!" << endl;
                }
                else if (lastLine.find("play") != string::npos) {
                    ofstream clearing(filePath.c_str());
                    clearing << " ";
                    clearing.close();
                    button_press(0x20);  // Pause
                    cout << "Pause!" << endl;
                }
                else if (lastLine.find("mute") != string::npos) {
                    ofstream clearing(filePath.c_str());
                    clearing << " ";
                    clearing.close();
                    button_press(0x4D);  // Mute
                    cout << "Mute!" << endl;
                }
            }
        }
        else {
            cerr << "Error opening output file!" << endl;
        }

        Sleep(100);  // Sleep to reduce CPU load
    }
}