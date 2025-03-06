---

### **Documentation for Payload Generator V4.5 by Public Enemy Number 1**

#### **Purpose:**

The Payload Generator V4.5 is an advanced cybersecurity tool developed for remote control and exploitation of target machines using a reverse shell. Building on the features of previous versions, this tool enables real-time interaction with the victim’s system, offering functionalities such as webcam and screen streaming, keylogging, system control (lock, shutdown, reboot), credential extraction, and file manipulation. Version 4.5 introduces improved connection handling, streamlined integration with Ngrok, and additional system commands for enhanced exploitation.

---

### **New Features in V4.5:**

- **Connection Handling Improvements:** Enhanced error handling for Ngrok and TCP connections to ensure more reliable connectivity.
- **Terminal Management:** Automatic terminal clearing after entering attacker details for better clarity and command focus.
- **Modular Commands:** New modular structure for extending payload commands.
- **Command Streamlining:** Simplified payload commands for easier control over the victim’s machine.

---

### **Setup Instructions**

#### **Requirements**

Before running the payload, ensure that the following Python modules are installed on the attacker’s machine:

```bash
pip install socket subprocess os time ctypes random pickle opencv-python numpy pyaudio pynput pywin32 threading struct pyautogui re json base64 pycryptodomex pyarmor
```

For Windows-based targets, also install **pywin32**:

```bash
pip install pywin32
```

#### **Ngrok Setup:**

1. **Download and Install Ngrok** from [ngrok.com](https://ngrok.com) on the attacker’s machine.
2. Create a TCP tunnel on the desired port (e.g., 8080) with the following command:
   ```bash
   ngrok tcp 8080
   ```
3. Note the TCP forwarding address provided by Ngrok (e.g., `tcp://0.tcp.ngrok.io:xxxxx`). You will use this IP and port for the payload connection.

#### **Configure and Run the Payload:**

1. Open and run the payload script:
   ```bash
   python Payload_generator_V-4.5.py
   ```
2. Enter the following information when prompted:
   - **Attacker IP**: The IP address from the Ngrok connection (`0.tcp.ngrok.io`).
   - **Attacker Port**: The port number provided by Ngrok (`xxxxx`).

3. The payload will attempt to establish a connection back to the attacker's machine.

#### **Using Ncat:**

Use Ncat (or Netcat) to listen for incoming connections on the port being forwarded by Ngrok:
```bash
ncat -lvnp 8080
```

---

### **Payload Commands in V4.5**

| **Command**            | **Description**                                                                 |
|------------------------|---------------------------------------------------------------------------------|
| `webcam`               | Streams live video from the target’s webcam.                                     |
| `stop_webcam`          | Stops the webcam stream.                                                         |
| `screenshare`          | Streams the target’s screen in real-time.                                        |
| `stop_screenshare`     | Stops screen sharing.                                                            |
| `upload <filepath>`    | Not done!                                                                        |
| `download <filepath>`  | Not done!                                                                        |
| `lockscreen`           | Locks the target’s screen.                                                       |
| `shutdown`             | Shuts down the target machine.                                                   |
| `reboot`               | Reboots the target machine.                                                      |
| `keylogs`              | Displays keystrokes recorded by the keylogger.                                   |
| `start_keylogger`      | Starts recording keystrokes from the target’s machine.                           |
| `stop_keylogger`       | Stops the keylogger.                                                             |
| `extract_google_logins`| Extracts stored credentials from Google Chrome.                                  |
| `get_wifi_passwords`   | Retrieves saved Wi-Fi passwords from the target machine.                         |
| `popups`               | Creates random pop-up windows on the target machine.                             |
| `audio_real_time`      | Streams live audio from the target’s microphone.                                 |
| `stop_audio`           | Stops the live audio stream.                                                     |
| `get_clipboard_content`| Retrieves the content from the target’s clipboard.                               |

---

### **Detailed Features and Functionalities**

#### **1. Webcam and Screen Streaming**
The tool allows remote access to both the target's webcam and display in real-time:
- Use the **webcam** command to start live video streaming from the victim’s webcam.
- Use **screenshare** to stream the target’s desktop or active window display.
- Stop these streams using the **stop_webcam** and **stop_screenshare** commands.

#### **2. File Upload/Download**
For file manipulation:
- **upload <filepath>** allows you to send a file from the attacker’s machine to the target.
- **download <filepath>** lets you retrieve files from the target’s machine.

#### **3. System Control Commands**
The attacker can control basic system states with commands:
- **lockscreen**: Locks the target's screen.
- **shutdown** and **reboot**: Control the system’s power state, shutting down or restarting the machine.

#### **4. Keylogging**
- **start_keylogger** begins capturing all key presses on the target's keyboard.
- **keylogs** retrieves and displays the captured keystrokes.
- **stop_keylogger** halts the keylogger.

#### **5. Credential Extraction**
Data collection from the target includes:
- **extract_google_logins**: Retrieves login credentials stored in the target’s Google Chrome browser.
- **get_wifi_passwords**: Collects saved Wi-Fi passwords stored on the target machine.

#### **6. Disruptive Pop-ups**
- **popups**: Spawns random pop-up windows to annoy or confuse the victim.

#### **7. Audio and Clipboard Capture**
- **audio_real_time** streams live audio from the target’s microphone to the attacker’s system.
- **get_clipboard_content** retrieves the current clipboard content from the target machine.

---

### **Connection Handling Improvements in V4.5**

The major enhancement in V4.5 is the reliability of the connection handling system. Previously, connection drops with Ngrok required manually restarting the payload and listener. In this version:
- Automatic connection re-establishment mechanisms are in place.
- Error messages will notify the attacker in the terminal if the connection is lost, and the payload will attempt to reconnect.

---

### **GUI for Live Streaming**

In addition to the reverse shell commands, a GUI is available for easier viewing of webcam and screen streams:
1. Run **Main.py** to launch the GUI interface.
2. The GUI provides real-time video and screen feeds from the victim machine, with start/stop controls for webcam and screen share streams.

---

### **Troubleshooting Tips**

1. **Connection Issues**:
   - If Ngrok disconnects, rerun the `ngrok tcp` command to re-establish the tunnel.
   - Ensure that Ncat/Netcat is listening on the same port forwarded by Ngrok.

2. **Command Failures**:
   - Double-check that all Python dependencies are installed and up-to-date.
   - Ensure correct file paths are used for uploading or downloading files.

3. **Keylogger Not Capturing Data**:
   - Make sure `pynput` is installed properly on both the attacker and target systems.
   - Verify that the keylogger thread is running and not interrupted.

---

### **Legal Disclaimer**

**Author**: Public Enemy Number 1
**Version**: 4.5  
**Project**: Reverse Shell Payload Generator

This tool is intended strictly for educational and authorized penetration testing purposes. Any unauthorized use of this tool on systems without explicit permission is illegal and punishable by law. Always obtain proper authorization before running security tests.

**Copyright (c) 2024 Public Enemy Number 1. All rights reserved.**

---
