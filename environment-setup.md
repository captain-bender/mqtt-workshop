
## Set up the docker-compose Environment
This setup will launch both the MQTT broker and a Python service that continuously publishes simulated sensor data.

**Project Structure**
First, create the following folder and file structure. This organizes the configuration and the simulator code neatly.

```
mqtt_workshop/
├── docker-compose.yml
├── mosquitto/
│   └── config/
│       └── mosquitto.conf
└── sensor_simulator/
    ├── Dockerfile
    ├── main.py
    └── requirements.txt
```

1. ```docker-compose.yml```

    This file orchestrates the two services. The simulator will automatically wait for the broker to be ready before starting.

2. ```sensor_simulator/Dockerfile```

    This builds the Python environment for our simulated sensor.

3. ```sensor_simulator/requirements.txt```

    A simple file listing our only Python dependency.

4. ```sensor_simulator/main.py```
    
    This is the heart of the simulator. It connects to the mqtt_broker service (by its name) and publishes data to two different topics every 5 seconds.

5. ```mosquitto/config/mosquitto.conf```

    Since version 2.0, Mosquitto no longer allows anonymous connections by default. Our sensor_simulator tries to connect without a username or password, and the broker correctly refuses it. We need to add a configuration file that tells the broker to listen on port 1883 and to allow clients to connect without a username/password.

**How to Run**

Open a terminal in the mqtt_workshop directory and run:
```
docker-compose up --build
```
Now we are ready for the experiments.

## Set up the experiments' environment
Create and Activate the Virtual Environment

Create a dedicated folder for our client scripts and set up a Python virtual environment inside it. This keeps our project dependencies tidy.

This step assumes that you have installed Python 3 on your laptop.

Instructions:

- On your computer (not inside the mqtt_workshop folder), create a new folder to hold your client scripts. Let's call it smartbuilding_client.

- Open a terminal and navigate into this new folder: 
    ```
    cd smartbuilding_client
    ```
- Create the virtual environment by running:
    ```
    python3 -m venv venv
    ```
- Activate the environment. The command depends on your operating system:
    ```
    .\venv\Scripts\activate
    ```
- Install paho-mqtt by running the proper pip command.
    ```
    pip install paho-mqtt
    ```

## Docker compose explanation

This Docker Compose file orchestrates a small, self-contained network of two services.

Service 1: `mqtt_broker`

This service is the central nervous system of our smart building system — the **MQTT broker**. It’s like a dedicated post office for all the sensor data.

* `image: eclipse-mosquitto:2.0`
    This tells Docker to download and run the official **Eclipse Mosquitto** software, version 2.0, which is a popular and reliable MQTT broker. We're using a pre-built image, like using a pre-fabricated component.

* `container_name: mqtt_broker`
    We give our container a simple, predictable name, `mqtt_broker`, so other services can easily find it on the Docker network.

* `ports: - "1883:1883"`
    This is a crucial step. It maps port **1883** from inside the container to port **1883** on your local machine. This is what allows the Python scripts you run on your computer (`monitor.py`, `controller.py`) to connect to the broker running inside Docker.

* `volumes: - ./mosquitto/config/...`
    This line injects our custom `mosquitto.conf` file into the container. This is how we gave the broker special instructions—specifically, to `allow_anonymous true`—overriding its default, more secure behavior for our workshop.

Service 2: `sensor_simulator`

This service is the "smart" part of our smart building—a simulated network of **sensors**. It's a Python script that continuously generates and publishes data.

* `build: ./sensor_simulator`
    Unlike the broker, we don't download a pre-built image. Instead, this tells Docker to build a **custom image** from the `Dockerfile` located in our `sensor_simulator` folder. This is how we package our own Python script into a runnable service.

* `container_name: sensor_simulator`
    Just like the broker, we give it a simple name.

* `depends_on: - mqtt_broker`
    This is a vital instruction for startup order. It tells Docker, "**Do not start the sensor_simulator until the mqtt_broker service has started first.**" This prevents the simulator from trying to connect to a broker that doesn't exist yet, avoiding startup errors.