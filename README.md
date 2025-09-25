
# TikTok Live Viewer Bot

Automate TikTok live viewer bots using Opera in headless mode with built-in VPN.

## Features

- Headless browser automation with Opera
- Built-in VPN for location spoofing
- Multiple bot accounts management
- Customizable viewing patterns
- Proxy support for additional anonymity

## Requirements

- Python 3.8+
- Opera browser with headless support
- ChromeDriver or similar WebDriver

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python tiktok_bot.py --help
```

## Configuration

Edit `config.json` to customize bot behavior:

```json
{
    "max_viewers": 10,
    "view_duration_min": 5,
    "view_duration_max": 30,
    "use_vpn": true,
    "vpn_countries": ["US", "CA", "GB"]
}
```

## Contributing

Feel free to submit pull requests or open issues.
