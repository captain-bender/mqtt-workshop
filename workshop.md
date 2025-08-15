## Hands-on experiments part of the workshop

### Experiment 1: Monitoring the Building

**Objective**: Understand how to subscribe to topics and use wildcards to filter message streams.

Instructions:
1. Open a terminal in your smartbuilding_client folder and activate the virtual environment (source venv/bin/activate or .\venv\Scripts\activate).

2. Run the monitoring script:
```
python monitor.py
```

Key Concepts to Discuss:

- Topic Hierarchy: Examine, e.g., smartbuilding/floor1/room101/temperature. This is like a file path, making the data organized and queryable.

- Wildcards: Focus on the line client.subscribe("smartbuilding/#").

    - Multi-level wildcard (#): The # acts as a catch-all. It subscribes us to every topic that begins with smartbuilding/.

    - Single-level wildcard (+): If we only wanted the temperature from every room on floor 1, what would we subscribe to?

- Relevance to AI/Robotics: How you'd monitor a fleet of drones or get all sensor readings from a specific robot?


### Experiment 2: Controlling the building's HVAC system & QoS

**Objective**: Understand how to publish messages and the importance of Quality of Service (QoS) for reliable commands.

Instructions:
1. Open a new, second client terminal.

2. In this new terminal, navigate to the smartbuilding_client folder and activate the venv.

3. Run the controller script:
```
python controller.py
```

Key Concepts to Discuss:

- Publishing:This script is now acting as a Publisher, just like the simulator.

- Quality of Service (QoS): This is the most critical concept here.

    - QoS 0 (At Most Once): "Fire and forget." Used by our sensor simulator. It's fast, but messages can be lost. Perfect for non-critical, high-volume data where a missed reading isn't a disaster.

    - QoS 1 (At Least Once): "Acknowledged delivery." The broker ensures the message is delivered. It might arrive more than once, but it will arrive. This is the minimum standard for sending a command, like "turn on HVAC."

    - QoS 2 (Exactly Once): "Guaranteed delivery." The highest level of reliability, ensuring a message is received exactly once. It's slower due to a four-part handshake. Use this for critical, non-repeatable actions like "initiate firmware update" or "dispense medication."

### Experiment 3: Building a Resilient System 

**Objective**: Demonstrate how the Retain flag and Last Will and Testament (LWT) create robust, state-aware systems.

A. Test the Retain Flag (10 mins)

Instructions:

1. Make sure the controller.py script is running in its terminal.

2. Go to the monitor.py terminal and stop the script with Ctrl+C.

3. Restart it immediately: python monitor.py.

Discussion: 

The *Retain flag* tells the broker to keep a 'sticky note' of the last message for that topic. Any new subscriber gets that message immediately. This is essential for dashboards so they can show a device's current state without waiting for the next update.

B. Test the Last Will & Testament

Instructions:

1. Make sure both monitor.py and controller.py are running.

2. Go to the terminal running controller.py and close the window/tab directly to simulate a crash (do not use Ctrl+C).

Discussion: 

This is the 'dead man's switch' of MQTT. The controller told the broker its 'last will' when it connected. When the broker detected the unexpected disconnection, it published the will on the client's behalf. This is how a central system can reliably detect when a remote sensor or robot has failed.

