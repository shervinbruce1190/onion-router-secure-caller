# Onion Router Secure Caller

A privacy-focused phone calling application built with Kivy that demonstrates secure communication through simulated onion routing. Features include multi-layered encryption, animated matrix-style UI, Twilio integration, and multiple calling methods.

![Onion Router Secure Caller](https://api.placeholder.com/600/300)

## Features

- 🔒 Simulated onion routing with multi-layered Fernet encryption
- 🌐 Support for international calling with country code selection
- 📱 Multiple calling methods: System Dialer, Twilio API, and Web Service
- 🖥️ Matrix-inspired animated UI with real-time status indicators
- 🔐 Network visualization with simulated node activity

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Internet connection for downloading dependencies

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/onion-router-secure-caller.git
cd onion-router-secure-caller
```

### Step 2: Set Up a Virtual Environment (Recommended)

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt file, install the necessary packages individually:

```bash
pip install kivy
pip install cryptography
pip install twilio
```

### Step 4: Configure Twilio (Optional)

To use the Twilio integration features:

1. Sign up for a [Twilio account](https://www.twilio.com/try-twilio)
2. Get your Account SID and Auth Token from the Twilio dashboard
3. Purchase a phone number through Twilio
4. Edit the `EnhancedCallHandler` class in `app.py` to include your credentials:

```python
# Replace with your actual credentials
TWILIO_ACCOUNT_SID = "your_account_sid_here"
TWILIO_AUTH_TOKEN = "your_auth_token_here"
TWILIO_PHONE_NUMBER = "your_twilio_number_here"
```

**Note:** For security, consider using environment variables instead of hardcoding credentials:

```python
import os
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER")
```

### Step 5: Run the Application

```bash
python app.py
```

## Usage

1. **Select Target Region**: Choose the country code for the number you want to call
2. **Enter Target Number**: Input the phone number without the country code
3. **Choose Call Method**:
   - System Dialer: Uses your device's native phone app
   - Twilio: Makes calls through the Twilio API (requires configuration)
   - Web Service: Opens a web-based calling service
4. **Initiate Call**: Click the "INITIATE SECURE CALL" button to start the call process
5. **Monitor Status**: Watch the status indicators to track call progress

## System Requirements

### Minimum Requirements:
- **OS**: Windows 7+, macOS 10.12+, Linux with X11
- **Processor**: Dual-core 1.5 GHz or better
- **Memory**: 2 GB RAM
- **Storage**: 100 MB available space
- **Internet**: Broadband connection for Twilio and web services

### Recommended Requirements:
- **OS**: Windows 10+, macOS 12+, Ubuntu 20.04+
- **Processor**: Quad-core 2.0 GHz or better
- **Memory**: 4 GB RAM
- **Display**: 1280x720 resolution or higher
- **Internet**: High-speed connection for optimal performance

## Technical Overview

### Onion Routing Simulation
The application simulates the principles of onion routing by encrypting call data with multiple layers of encryption. Each simulated node has its own encryption key, and the data is wrapped in successive layers before transmission.

### Kivy UI Framework
The user interface is built using Kivy, a cross-platform Python framework that allows the application to run on desktop and mobile platforms. The matrix-style animations and visual effects are implemented using Kivy's graphics capabilities.

### Telephony Integration
The application supports multiple methods for initiating calls:
- **System Dialer**: Uses the `tel:` URI protocol
- **Twilio API**: Utilizes the Twilio REST API for web-based calling
- **Web Service**: Opens external web-based calling services

## Educational Purpose

This project is designed for educational purposes to demonstrate:
- Principles of secure communication and onion routing
- Implementation of cryptographic protocols in Python
- Integration with telephony systems and APIs
- Development of animated UIs with Kivy

## Troubleshooting

### Common Issues:

#### Kivy Installation Problems
If you encounter issues installing Kivy:
```bash
pip install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/
```

#### Missing Dependencies on Linux
For Linux users who encounter dependency issues:
```bash
sudo apt-get install python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev pkg-config libgl1-mesa-dev libgles2-mesa-dev
```

#### Twilio Connection Errors
If the Twilio integration fails, verify:
- Your account credentials are correct
- Your Twilio account is active and funded
- The destination number is in a valid format with country code
- Your Twilio number has the appropriate capabilities enabled

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This application is intended for educational purposes to demonstrate secure communication principles. It includes simulated security features and is not intended for mission-critical communications that require actual security guarantees.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- The Kivy team for their excellent cross-platform framework
- Twilio for their telephony API services
- The cryptography library maintainers
