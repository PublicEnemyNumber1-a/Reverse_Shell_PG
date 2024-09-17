### **Documentation for Payload Generator V4.0 by PhantomCode**


#### **Purpose:**
The Payload Generator V4.0 is an advanced tool designed for remotely controlling a target’s machine using a reverse shell. It provides functionality for real-time webcam streaming, screen sharing, file management (upload/download), system manipulation (lock, shutdown, reboot), keylogging, and credential extraction (e.g., Google Chrome logins and Wi-Fi passwords). This version also includes integration with Ngrok for tunneling through NAT/firewalls and Ncat for TCP connections.

---

### **Setup Instructions**

#### **Requirements**

Before running the payload, ensure the following Python modules are installed on the attacker's machine:

```bash
pip install socket subprocess os time ctypes random pickle opencv-python numpy pyaudio pynput pywin32 threading struct pyautogui re json base64 pycryptodomex
```

Install **pywin32** (for Windows-based targets) if necessary:

```bash
pip install pywin32
```

#### **Ngrok Setup:**
1. **Download Ngrok** from [ngrok.com](https://ngrok.com) and ensure it’s properly installed on your machine.
2. Run the following command to create a TCP tunnel on port 8080 (or another specified port):
   ```bash
   ngrok tcp 8080
   ```
   This will provide you with a TCP forwarding address, something like `tcp://0.tcp.ngrok.io:xxxxx`. Note the address and port number for the next steps.

#### **Ncat Setup:**
Use Ncat or Netcat to listen for incoming connections on the port being forwarded by Ngrok. Run the following command on your terminal:
```bash
ncat -lvnp 8080
```
or 
```bash
nc -lvnp 8080
```

#### **Configure and Run the Payload:**

1. Open the **Payload_generator_V-4.0.py** file and modify the following:
   - **Attacker IP**: The IP address from the Ngrok connection (`0.tcp.ngrok.io`).
   - **Attacker Port**: The port number provided by Ngrok (`xxxxx`).

2. After modifying these details, run the Python script to generate and execute the payload on the target machine:
   ```bash
   python Payload_generator_V-4.0.py
   ```

Once the payload is executed on the target, the reverse shell will establish a connection back to your Ncat listener.

---

### **Payload Commands**

This version of the payload allows the following commands to be executed on the target machine through the reverse shell. Each command initiates a specific action on the victim's system:

| **Command**              | **Description**                                                                 |
|--------------------------|---------------------------------------------------------------------------------|
| `webcam`                 | Starts streaming the target’s webcam feed to the attacker’s machine.              |
| `stop_webcam`            | Stops the webcam streaming.                                                       |
| `screenshare`            | Starts real-time screen sharing of the target’s display.                          |
| `stop_screenshare`       | Stops screen sharing.                                                             |
| `upload <filepath>`      | not done                                                                          |
| `download <filepath>`    | not done                                                                          |
| `lockscreen`             | Locks the target’s screen.                                                        |
| `shutdown`               | Shuts down the target’s machine.                                                  |
| `reboot`                 | Reboots the target’s machine.                                                     |
| `extract_google_logins`  | Extracts stored login credentials from Google Chrome.                             |
| `get_wifi_passwords`     | Extracts saved Wi-Fi passwords from the target machine.                           |
| `popups`                 | Creates random annoying pop-up windows on the target's screen.                    |
| `keylogs`                | Displays logged keystrokes from the keylogger running on the target machine.      |
| `start_keylogger`        | Starts a keylogger that records the target's keystrokes.                          |
| `stop_keylogger`         | Stops the keylogger.                                                              |
| `audio_real_time`        | Streams live audio from the target’s microphone to the attacker’s machine.        |
| `stop_audio`             | Stops the real-time audio streaming.                                              |
| `get_clipboard_content`  | Retrieves the current clipboard content from the target.                          |

---

### **Features and Functionality**

#### **1. Webcam and Screen Sharing**
- The **webcam** command starts streaming video from the target’s webcam in real-time, while **screenshare** starts streaming the target’s display.
- Use the **stop_webcam** and **stop_screenshare** commands to stop the streams.

#### **2. File Management (Upload/Download)**
- Not yet done

#### **3. System Actions**
- **lockscreen**: Locks the target's screen remotely.
- **shutdown** and **reboot** commands allow full control of the target system’s power state.
  
#### **4. Credential and Data Extraction**
- **extract_google_logins** retrieves all saved login credentials from Google Chrome.
- **get_wifi_passwords** collects stored Wi-Fi passwords from the target system.

#### **5. Pop-ups for Disruption**
- The **popups** command spawns random pop-up windows on the target’s machine, causing disruption and annoyance.

#### **6. Keylogging**
- The **start_keylogger** command begins capturing all keystrokes from the target’s keyboard. 
- **keylogs** retrieves the stored keystrokes, while **stop_keylogger** stops the logging process.

#### **7. Audio Capture**
- The **audio_real_time** command streams live audio from the target's microphone to the attacker’s system, while **stop_audio** stops the streaming.

#### **8. Clipboard Content**
- The **get_clipboard_content** command fetches whatever is currently in the clipboard of the target machine.

---

### **GUI Setup for Viewing Webcam and Screen Stream**

1. Run the **Main.py** file after starting the reverse shell to open the GUI.
2. This GUI allows real-time viewing of webcam streams and screen sharing data.
3. Use the respective commands in the reverse shell to start and stop the streams.

---

### **Troubleshooting**

1. **Connection Issues**:
   - If Ngrok disconnects, rerun the `ngrok tcp` command and restart the payload.
   - Ensure Ncat is listening on the same port forwarded by Ngrok.
   
2. **Failed Commands**:
   - Double-check that all Python dependencies are installed.
   - Ensure the correct file paths are used for upload/download actions.

3. **Keylogger Not Working**:
   - Make sure that `pynput` is properly installed and functioning on both the attacker and target systems.

---

### **Author and Legal Information**

- **Author**: PhantomCode  
- **Version**: 4.0  
- **Project**: Reverse Shell Payload Generator

#### **Legal Disclaimer**:
This tool is intended for educational purposes and authorized testing only. The author is not responsible for any misuse or damage caused by this tool. Unauthorized access to computer systems or networks is illegal and punishable by law. Always obtain explicit permission from the system owner before running tests or executing this payload.

# Copyright (c) 2024 PhantomCode943. All rights reserved.
