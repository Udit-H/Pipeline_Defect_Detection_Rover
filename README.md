# Pipeline Defect Detection Rover

A web-based remote control system for a Raspberry Pi robot with live video streaming. This project allows you to control a robot's movements (forward, backward, left, right, stop) through a web interface while viewing real-time video feed from the robot's camera.

## Features

- **Web-based Control Interface**: Control the robot from any device with a web browser
- **Live Video Streaming**: Real-time video feed from the robot's camera via MJPEG streaming
- **Automatic IP Detection**: Dynamically detects the Raspberry Pi's local IP address - no hardcoding needed
- **Motor Control**: 4-direction movement control (Forward, Backward, Left, Right) with Stop functionality
- **Responsive Design**: Grid-based button layout with hover effects for intuitive control
- **Multi-threaded**: Flask server runs with threading enabled for smooth operation

## Hardware Requirements

- **Raspberry Pi** (any model with GPIO support - 3B+, 4, or 5 recommended)
- **Motor Driver** (L298N or similar dual H-bridge motor driver)
- **DC Motors** (2x motors for differential drive)
- **USB Camera or Raspberry Pi Camera Module**
- **Robot Chassis** with wheels
- **Power Supply** (for both Raspberry Pi and motors)
- **Jumper Wires** for GPIO connections

## GPIO Pin Configuration

The following GPIO pins (BOARD numbering) are used for motor control:

```
Motor_In1 = GPIO 29  (Motor 1 Forward)
Motor_In2 = GPIO 31  (Motor 1 Backward)
Motor_In3 = GPIO 33  (Motor 2 Forward)
Motor_In4 = GPIO 35  (Motor 2 Backward)
```

### Wiring Diagram

Connect your motor driver to the Raspberry Pi GPIO pins as follows:

| Motor Driver Pin | Raspberry Pi GPIO (BOARD) | Description |
|------------------|---------------------------|-------------|
| IN1 | 29 | Left Motor Forward |
| IN2 | 31 | Left Motor Backward |
| IN3 | 33 | Right Motor Forward |
| IN4 | 35 | Right Motor Backward |
| GND | GND | Common Ground |

**Note**: Ensure the motor driver has a separate power supply for the motors. Connect the Raspberry Pi and motor driver grounds together.

## Software Requirements

- Python 3.7+
- Flask
- OpenCV (cv2)
- RPi.GPIO

## Installation on Raspberry Pi

### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Python Dependencies

```bash
# Install pip if not already installed
sudo apt install python3-pip -y

# Install required Python packages
pip3 install flask
pip3 install RPi.GPIO
pip3 install opencv-python

# Install additional OpenCV dependencies
sudo apt install -y python3-opencv
sudo apt install -y libatlas-base-dev libjasper-dev libqt4-test
```

### 3. Enable Camera (if using Raspberry Pi Camera Module)

```bash
sudo raspi-config
```
Navigate to **Interface Options** → **Camera** → **Enable**

Reboot the Raspberry Pi:
```bash
sudo reboot
```

### 4. Clone/Download the Project

```bash
# Clone the repository (replace with your repo URL)
git clone https://github.com/yourusername/Pipeline_Defect_Detection_Rover.git
cd Pipeline_Defect_Detection_Rover

# Or download and extract manually
```

### 5. Verify Directory Structure

Ensure your project has the following structure:
```
Pipeline_Defect_Detection_Rover/
├── Control_Robot_Using_Webpage.py
└── templates/
    └── temp.html
```

## Usage

### 1. Run the Application

```bash
python3 Control_Robot_Using_Webpage.py
```

The server will automatically detect your Raspberry Pi's IP address and display it:
```
Server running on: 192.168.x.x:8080
```

### 2. Access the Web Interface

From any device on the same network:
1. Open a web browser
2. Navigate to: `http://[RASPBERRY_PI_IP]:8080`
   - Example: `http://192.168.1.105:8080`

### 3. Control the Robot

- **Forward**: Move robot forward
- **Backward**: Move robot backward
- **Left**: Turn robot left
- **Right**: Turn robot right
- **Stop**: Stop all motors

The interface also displays the live video feed from the camera.

## Auto-Start on Boot (Optional)

To run the script automatically when the Raspberry Pi boots:

### Using systemd Service

1. Create a service file:
```bash
sudo nano /etc/systemd/system/robot-control.service
```

2. Add the following content:
```ini
[Unit]
Description=Robot Web Control Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Pipeline_Defect_Detection_Rover
ExecStart=/usr/bin/python3 /home/pi/Pipeline_Defect_Detection_Rover/Control_Robot_Using_Webpage.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Enable and start the service:
```bash
sudo systemctl enable robot-control.service
sudo systemctl start robot-control.service
```

4. Check status:
```bash
sudo systemctl status robot-control.service
```

## Troubleshooting

### Camera Not Working
- Verify camera connection: `vcgencmd get_camera`
- Try `raspistill -o test.jpg` to test camera
- Change camera index in code: `cv2.VideoCapture(0)` → `cv2.VideoCapture(1)`

### GPIO Permission Issues
- Add your user to the GPIO group:
  ```bash
  sudo usermod -a -G gpio pi
  ```

### Cannot Access Web Interface
- Check firewall settings
- Verify both devices are on the same network
- Try accessing from the Pi itself: `http://localhost:8080`

### Import Errors
- Ensure all packages are installed: `pip3 list | grep -E "Flask|opencv|RPi"`
- Try reinstalling: `pip3 install --upgrade [package-name]`

## Network Configuration

The application automatically detects your Raspberry Pi's local IP address. To use this on different networks:
1. Simply connect your Pi to the network
2. Run the application
3. Note the IP address displayed in the terminal
4. Access the web interface using that IP

## Port Configuration

Default port is **8080**. To change it, modify line 127:
```python
app.run(Url_Address, 8080, threaded=True)
```
Change `8080` to your desired port number.

## Safety Considerations

- Always test in a safe environment first
- Ensure emergency stop functionality works
- Keep the robot within line of sight
- Test motor directions before full assembly
- Use appropriate power supply ratings
- Add fuses/circuit breakers for protection

## Future Enhancements

- [ ] Add PWM speed control
- [ ] Implement ultrasonic sensors for obstacle avoidance
- [ ] Add defect detection AI/ML models
- [ ] Mobile-responsive UI improvements
- [ ] Battery level monitoring
- [ ] Recording functionality for video feed

## License

This project is open source and available for educational purposes.

## Contributors

- RVCE Sem 2 EL Team

## Acknowledgments

- Built using Flask web framework
- OpenCV for video streaming
- RPi.GPIO for hardware control

---

**Project**: Pipeline Defect Detection Rover  
**Institution**: RV College of Engineering  
**Semester**: 2  
**Department**: EL (Electronics)
