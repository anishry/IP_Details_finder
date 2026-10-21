# Public IP Details Finder

A lightweight, dark-themed desktop application built with Python and Tkinter to retrieve public IP address information, including geolocation, network provider details, timezone, and network flags.

The application can automatically detect your own public IP address or look up another IP address.

## Features

- **Automatic public IP detection**
- **IP address lookup** for a user-entered address
- **Geolocation details:** Country, region, city, postal code, latitude, longitude, and coordinates
- **Network information:** ISP, organisation, AS number, AS name, and timezone
- **Network flags:** Mobile network, proxy/VPN, and hosting provider indicators
- **Google Maps integration** for reported coordinates
- **Copy individual values** to the clipboard
- **Copy lookup results as JSON**
- **Dark-themed graphical interface**
- **Background processing** to keep the interface responsive

## Technologies Used

- Python 3.8+
- Tkinter
- Python standard-library modules
- [ipify](https://www.ipify.org/) — public IP detection
- [ip-api.com](https://ip-api.com/) — IP geolocation and network information

No third-party Python packages are required.

## Requirements

- Python 3.8 or later
- Tkinter installed
- Internet connection

## Installation and Execution

### 1. Clone the repository

Replace the example URL with your actual GitHub repository URL.

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
cd YOUR-REPOSITORY
```

### 2. Run the application

Save the Python script as `ip_details_gui.py`.

```bash
python ip_details_gui.py
```

Alternatively, on Linux or macOS:

```bash
python3 ip_details_gui.py
```

On Debian or Ubuntu, install Tkinter if required:

```bash
sudo apt install python3-tk
```

## How to Use

1. Launch the application.
2. The application attempts to identify your public IP address automatically.
3. Enter another IP address in the search field to look up its information.
4. Click **Lookup** or press Enter.
5. Click **My IP** to retrieve your current public IP information again.
6. Review the Location, Network, and Network Flags sections.
7. Use the copy controls to copy individual values.
8. Click **Copy all as JSON** to copy the complete lookup response.
9. Click **Open in Google Maps** to view the reported coordinates when available.

## API Services

### Public IP Detection

The application uses the ipify API:

`https://api64.ipify.org?format=json`

### IP Geolocation

The application uses the ip-api.com API to retrieve available geolocation and network information.

The returned fields may include country, region, city, postal code, coordinates, timezone, ISP, organisation, AS information, and mobile, proxy, and hosting indicators.

## Project Structure

```text
YOUR-REPOSITORY/
├── ip_details_gui.py
└── README.md
```

## Security and Privacy Considerations

- IP addresses are sent to external API providers to perform lookups.
- The current source code uses an **HTTP endpoint** for ip-api.com, so that API request is not protected by HTTPS.
- IP geolocation is approximate and cannot reliably determine a person's exact physical location.
- Proxy, VPN, and hosting indicators are estimates supplied by the API.
- Review the API providers' terms and privacy policies before using the application.

## Limitations

- An internet connection is required.
- Results depend on the availability and accuracy of third-party APIs.
- Geolocation may be affected by VPNs, proxies, mobile networks, and ISP routing.
- The application displays API-provided information and does not independently verify it.

## Contributing

Contributions and suggestions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Implement and test your changes.
4. Submit a pull request with a description of your changes.

## License

No license is specified in the provided source code. Add a `LICENSE` file before publishing the repository if you want to establish explicit permissions for reuse and distribution.

## Disclaimer

This project is intended for educational, diagnostic, and authorised network-information purposes. The displayed information may be incomplete or inaccurate. Do not rely solely on these results for security-critical decisions.
