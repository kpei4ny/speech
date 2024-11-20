#pragma once

#include <iostream>
#include <windows.h>
#include <fstream>
#include <string>
#include <thread>
using namespace std;

class Speach {
private:
    const char* pythonCommand = "python3 ..\\Python\\UI\\main.py";  // Path to Python script
    const string filePath = "..\\Python\\output.txt";           // Path to output file
    thread pyThread;                               // Thread for running Python script
    thread procThread;                             // Thread for processing output file

public:
    Speach();

    ~Speach();

    // Function to scroll the mouse wheel
    void scroll(int displacement);

    // Function to press a button
    void button_press(WORD keyCode);

    // Function to run the Python script
    void run_python_script();

    // Function to process the output file
    void process_output_file();
};
