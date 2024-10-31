# Hand Gesture Volume Control

This project implements a hand gesture recognition system to control the volume of your computer's audio output using real-time video input. The system leverages computer vision techniques to detect hand positions and gestures, allowing users to increase or decrease the volume based on the distance between their thumb and index finger.

## Features

- **Real-Time Hand Tracking**: Utilizes a hand tracking module to detect hand landmarks and gestures in real-time.
- **Volume Control**: Adjusts the system volume based on the distance between the thumb and index finger, with defined thresholds for volume increase and decrease.
- **Visual Feedback**: Displays the current volume level and a visual representation of the volume bar on the video feed.
- **Cross-Platform Compatibility**: Works with any webcam-enabled device and is implemented in Python.

## Requirements

- Python3
- OpenCV
- NumPy
- PyCaw
- mediaPipe

## Usage
Simply have both the codes in a folder and then run VolumeHandControl.py.

you can clone the repo if you want to, but it is overkill as there are only two codes present.


## How It Works
The program captures video frames from your webcam.
It detects hand landmarks using a custom hand tracking module.
Based on the distance between the thumb tip and index finger tip, it calculates the volume level and adjusts it accordingly.
A visual representation of the current volume is displayed on the video feed.
Troubleshooting
No Hand Detected: Ensure your hand is within the camera's view and there is sufficient lighting.
Volume Not Changing: Check if the system audio is not muted and ensure the correct audio device is selected.
Acknowledgments
OpenCV for computer vision functionalities.
PyCaw for audio control in Windows.
Hand tracking techniques inspired by various computer vision projects.
