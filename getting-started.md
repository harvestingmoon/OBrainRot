# Getting Started



## Prerequisites
Before running the project, ensure you have:
- **Docker** installed ([Get Docker](https://docs.docker.com/get-docker/))

## Running the Project with Docker
You can run the project in a Docker container using the following steps:

### 1️⃣ Build the Docker Image
Clone the repository and navigate into the project folder:
```bash
git clone https://github.com/harvestingmoon/OBrainRot.git
cd OBrainRot
```

Build the Docker image:
```bash
docker build -t obrainrot:latest .
```

### 2️⃣ Run the Docker Container
Run the container interactively:
```bash
docker run -it --rm -p 8000:5000 obrainrot:latest /bin/bash
```
This command:
- Starts an interactive terminal (`-it`)
- Removes the container after it stops (`--rm`)
- Maps port **5000** inside the container to **8000** on your host machine (`-p 8000:5000`)
- Runs the container using the latest image (`obrainrot:latest`)
- Opens a Bash shell inside the container (`/bin/bash`)

### 3️⃣ Start the Flask Server
Inside the running container, start the Flask application:
```bash
python main.py
```

## Stopping the Container
To stop the running container, press:
```bash
CTRL + C
```
Since we used the `--rm` flag, the container will be removed automatically.

## Development Notes
- FFmpeg is pre-installed in the Docker image.
- The project requires `requirements.txt` dependencies, which are installed automatically.

