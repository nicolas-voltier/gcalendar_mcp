# Google Calendar MCP Server

This MCP server provides access to your Google Calendar events and allows you to manage them through an MCP interface. It runs as a standalone server using `mcp-proxy` and can be accessed by any MCP-compatible client.

## Requirements

- **Python 3.10 or higher** - MCP requires Python 3.10+
- Google Cloud project with Calendar API enabled
- OAuth credentials for authentication

## Features

- **View calendar events** for any date or date range
- **Create new events** with title, time, description, location, and attendees
- **Update existing events** with new details
- **Pre-built prompts** for common calendar actions

## Installation

### 1. Clone this repository

```bash
git clone <repository-url>
cd gcalendar_mcp
```

### 2. Create a virtual environment

Create a virtual environment with Python 3.10 or higher (recommended to use highest python version):

```bash
# Check your Python version
python --version

# Create a virtual environment
# On Windows:
python -m venv venv

# On macOS/Linux (specify Python version explicitly to 3.13)
python3.13 -m venv venv
```

### 3. Activate the virtual environment

```bash
# On macOS/Linux:
source venv/bin/activate
```

### 4. Install dependencies

Install all required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```


### 5. Set up Google Calendar API credentials

Before running the server, you need to set up Google OAuth credentials:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create OAuth credentials (Desktop client OAuth ID)
5. Download the credentials JSON file

### 6. Run quick authentication setup

Use the `quick_auth_setup.py` script to set up authentication:

```bash
python quick_auth_setup.py
```

This script will:
- Guide you through placing your `credentials.json` file in the project directory
- Initiate the OAuth flow to authenticate with Google
- Save your authentication token for future use

**Note:** The credentials and token files are stored in the project directory (same folder as `calendar_mcp_server.py`).

## Running the MCP Server

### Using mcp-proxy

Once your virtual environment is set up and activated, you can run the MCP server using `mcp-proxy`:

```bash
# Make sure your virtual environment is activated
# Then run:
mcp-proxy run calendar_mcp_server.py
```

The server will start and listen for MCP client connections. You can connect to it using any MCP-compatible client.

#### Configuring the Port

By default, `mcp-proxy` will use a random port. To specify a custom port, use the `--port` option:

```bash
# Run on a specific port (e.g., 8080)
mcp-proxy --port 8080 run calendar_mcp_server.py
```

You can also configure the host address using the `--host` option (default is `127.0.0.1`):

```bash
# Run on a specific port and host
mcp-proxy --port 8080 --host 127.0.0.1 run calendar_mcp_server.py
```


**Note:** When you start the server, `mcp-proxy` will display the URL where the server is accessible (e.g., `http://127.0.0.1:8080/sse`). Use this URL to connect your MCP client.


## Resources

The server exposes the following MCP resources:

- `calendar://events/{date}` - Returns events for a specific date

Example usage:
```
calendar://events/today
calendar://events/tomorrow
calendar://events/2023-07-15
```

## Tools

The server provides the following tools:

1. `list_events(date_start, date_end=None)` - List events in a date range
2. `create_event(summary, start_datetime, end_datetime, ...)` - Create a new calendar event
3. `update_event(event_id, ...)` - Update an existing event

## Prompts

Pre-built prompts to simplify common actions:

1. `today_events` - Quick access to today's calendar
2. `schedule_meeting` - Guided prompt to create a new meeting

## Authentication

On first use, the server will open a browser window for Google OAuth authentication. After authorizing the application, your credentials will be stored in `token.json` for future use.

The authentication files are stored in the project directory:
- Credentials: `credentials.json` (in the project root)
- Token: `token.json` (in the project root)

## Troubleshooting

- **Python version issues**: This project requires Python 3.10 or higher. If you see errors like `No matching distribution found for mcp[cli]`, check your Python version.
- **Authentication errors**: Ensure your `credentials.json` file is correctly placed in the project directory (same folder as `calendar_mcp_server.py`).
- **MCP installation problems**: Try using `uv` instead of `pip` for a more reliable installation experience.
- **mcp-proxy not found**: Make sure you've installed all dependencies from `requirements.txt` and your virtual environment is activated.

## Notes

- The server uses UTC for timestamps. Event times are displayed in the local timezone.
- You need a valid `credentials.json` file from Google Cloud Console to use this server.
- Your authentication token is stored in `token.json` after first login.
- The server logs are written to `calendar_mcp_server.log` in the project directory.
