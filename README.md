# Pichler LG350 Communication Library

A Python library and REST API for communicating with Pichler LG350 ventilation units.
This project enables you to read sensor values from the ventilation system and modify settings remotely using the Nabto protocol.

## Requirements

- Python 3.x (Python 2.x also supported)
- Pichler LG350 ventilation unit
- LAN access to the device
- Nabto libraries for your operating system

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pichler-io
   ```

2. **Download Nabto libraries**
   - Download [Nabto libraries](https://downloads.nabto.com/assets/nabto-libs/4.3.0/nabto-libs.zip)
   - Extract the appropriate libraries (.dll for Windows, .so for Linux/macOS) to the `libs` folder

3. **Configure device credentials**
   - Copy `pichler.ini.example` to `pichler.ini` (if example exists) or create the file
   - Add your device ID, username, and password:
   ```ini
   [pichler]
   device = your-device-id
   user = your-username
   pass = your-password
   ```

4. **Secure your credentials** (recommended)
   ```bash
   git update-index --skip-worktree pichler.ini
   ```

## Quick Start

### Test Your Setup

Run the info script to verify everything is working:

```bash
python info.py
```

This should output current sensor readings like:
```json
{
  "level": 2,
  "supply_vol": 145,
  "supply_temp": 21.5,
  "extract_vol": 142,
  "extract_temp": 22.1,
  "outdoor_temp": 18.3
}
```

### Start the REST API Server

```bash
python main.py
```

The server will start on `http://localhost:8080`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

See LICENSE file for details.
