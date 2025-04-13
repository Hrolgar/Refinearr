# Refinarr

[//]: # (<a href="https://github.com/hrolgar/refinearr">)

[//]: # (<img alt="GPL 2.0 License" src="https://img.shields.io/github/license/hrolgar/refinarr.svg"/>)

[//]: # (</a>)
<a href="https://github.com/hrolgar/refinearr/releases">
<img alt="Current Release" src="https://img.shields.io/github/release/hrolgar/refinearr.svg"/>
</a>
<a href="https://hub.docker.com/r/hrolgar/refinearr">
<img alt="Docker Pull Count" src="https://img.shields.io/docker/pulls/hrolgar/refinearr.svg"/>
</a>

Refinarr is a command-line tool that goes beyond filtering and deleting torrents from qBittorrent. In addition to its original functionality, Refinarr now integrates with Sonarr to handle tasks such as renaming episode files based on updated series information. (Radarr integration is also included as a framework for future enhancements.) The project leverages environment variables to manage sensitive data and configuration details.
## Features

### qBittorrent Management:

    - Login: Connects to the qBittorrent WebUI API.
    - Torrent Filtering: Lists and filters torrents based on configurable thresholds (age, last activity, popularity, etc.). 
    - Pretty-Printed Output: Displays torrent details in a colorful, boxed format. 
    - Interactive Deletion: Provides a prompt to confirm deletion, skip torrents, or delete all remaining torrents interactively.
### Sonarr Integration:
   - Series Processing: Retrieves series data from Sonarr.
   - Episode Renaming: Identifies episodes (via a defined set of criteria) and issues rename commands so that files are renamed based on updated series metadata.

### Radarr Integration:

- Framework Ready: Radarr functionality is added as a basis for future development. (Currently, Radarr methods are stubbed and do nothing.)

### Environment Management:

- All configuration and credentials are managed via environment variables.
- For local usage, a .env file can be used. 
- For Docker deployments, environment variables are supplied via Docker Compose (or other container orchestration tools).

## Recommended Setup: Docker Compose

For most users, the recommended approach is to deploy Refinarr using Docker Compose. This method avoids the need to manage a local Python environment manually and allows you to easily supply environment variables.

### Docker Compose Setup
1. Create a ``docker-compose.yml`` file in the project root with the following content:
    ````yaml
    services:
      refinarr:
        image: hrolgar/refinearr:latest
        environment:
            # qBittorrent Configuration
          - QBIT_BASE_URL=${QBIT_BASE_URL}
          - QBIT_USERNAME=${QBIT_USERNAME}
          - QBIT_PASSWORD=${QBIT_PASSWORD}
          - QBIT_INTERVAL_MINUTES=120
          # Use either QBIT_RUN_TIME or QBIT_INTERVAL_MINUTES, but not both.
          - QBIT_AGE_THRESHOLD_DAYS=16
          - QBIT_LAST_ACTIVITY_THRESHOLD_DAYS=10
          # SONARR Configuration
          - SONARR_BASE_URL=${SONARR_BASE_URL}
          - SONARR_API_KEY=${SONARR_API_KEY}
          - SONARR_RUN_TIME=04:00
          # Use either SONARR_INTERVAL_MINUTES or SONARR_RUN_TIME, but not both.
    
          # RADARR Configuration
          - RADARR_BASE_URL=${RADARR_BASE_URL}
          - RADARR_API_KEY=${RADARR_API_KEY}
          - RADARR_RUN_TIME=04:00
          # Use either RADARR_INTERVAL_MINUTES or RADARR_RUN_TIME, but not both.
          - SLEEP_INTERVAL=60
    ````
2. Supply Environment Variables:
    Set your sensitive environment variables (e.g., QBIT_USERNAME, QBIT_PASSWORD, SONARR_API_KEY, and RADARR_API_KEY) via your host’s environment or by using an .env file that Docker Compose can load.

3. Run Docker Compose:
    ````bash
    docker-compose up -d
    ````
   This will pull (or build) the Refinarr image, launch the container with your specified configuration, and run the application in schedule mode by default.

### Alternative: Docker Run Command
If you prefer not to use Docker Compose, you can run the container using a single ``docker run`` command. 
For example:

````bash
docker run -d \
  -e QBIT_BASE_URL=${QBIT_BASE_URL} \
  -e QBIT_USERNAME="${QBIT_USERNAME}" \
  -e QBIT_PASSWORD="${QBIT_PASSWORD}" \
  -e QBIT_INTERVAL_MINUTES=120 \
  -e QBIT_AGE_THRESHOLD_DAYS=16 \
  -e QBIT_LAST_ACTIVITY_THRESHOLD_DAYS=10 \
  -e SONARR_BASE_URL=${SONARR_BASE_URL} \
  -e SONARR_API_KEY="${SONARR_API_KEY}" \
  -e SONARR_RUN_TIME="04:00" \
  -e RADARR_BASE_URL=${RADARR_BASE_URL} \
  -e RADARR_API_KEY="${RADARR_API_KEY}" \
  -e RADARR_RUN_TIME="04:00" \
  -e SLEEP_INTERVAL=60 \
  hrolgar/refinearr:latest
````

In this setup, the container will always run in schedule mode since its ENTRYPOINT is configured with the --schedule flag.


## For Developers (Forking and Local Development)

If you wish to fork Refinarr or run it in a local development environment without Docker Compose:
You can set up the project in one of two ways: manually or by using an automated setup script.

### Automated Setup (Recommended)
If you prefer a one-command setup, you can use the provided shell or batch script. The scripts will:

- Create the virtual environment (if it does not exist)

- Activate the virtual environment

- Install dependencies from ``requirements.txt``

- Create the ``.env`` file with default values (if it doesn’t already exist)

### Unix/macOS Setup Script
Run the following command from the project root:
````bat 
setup\file.bat
````

### Windows Setup Script

Run the batch script by either double-clicking the file or executing it from a command prompt:
````batch
setup\file.bat
````

Once the appropriate setup script finishes, you can run the main script:
````batch
python main.py
````

### Manual Setup
1. Clone the Repository
    ````bash 
    git clone https://your.repo.url/qbittorrent-manager.git
    cd qbittorrent-manager
    ````
2. Create and Activate a Virtual Environment:

   - Unix/macOS:
       ````bash 
       python -m venv venv
       source venv/bin/activate
       ````

     - Windows:
     python -m venv venv
     venv\Scripts\activate

3. Install Dependencies:
    ````bash 
    pip install -r requirements.txt
    ````

4. Create the .env File:

    Create a file named .env in the project root and add the environment variables you need. You can use the provided .env.example as a template.

5. Run the Script:

    ````bash 
    python main.py
    ````


## Command-Line Arguments
This application uses Python’s built-in argparse module to allow configuration via command-line arguments. Currently, we support the following options:

- ``--non-interactive``:
    Runs the application in non-interactive mode. In this mode the program automatically deletes all filtered torrents without prompting the user.

- ``--schedule``:
    Runs the job on a continuous schedule, allowing the application to trigger a daily run for torrent cleanup. The scheduled run time is specified via the RUN_TIME environment variable (default is "02:00").

### Example Usage

- Run once, prompting the user interactively:
    ````bash
    python main.py
    ````

- Run once, automatically deleting without user input:

    ````bash
    python main.py --non-interactive
    ````

- Run continuously with daily scheduling (non-interactive, recommended for Docker deployments):

    ````bash
    python main.py --schedule
    ````