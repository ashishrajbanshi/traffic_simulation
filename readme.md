# 🚦 Traffic Intersection Simulation with SUMO and Python

This project simulates vehicle flow through a four-way traffic intersection using **SUMO (Simulation of Urban MObility)** and **Python** via the **TraCI** interface. It models traffic light control, vehicle movement, and vehicle queue length over time, and generates analytics including a CSV log and a queue length visualization.

---

## Project Structure

### `network/intersection.nod.xml` & `intersection.edg.xml`

These XML files define the **layout of the road network**:

* Nodes `A`, `B`, `C`, `D` represent the four corners (North, South, East, West).
* Node `J` is the central intersection junction.
* Edges connect each outer node to the junction and back.

### `network/intersection.net.xml`

This is the **compiled network** file, generated using `netconvert`:

```bash
netconvert -n intersection.nod.xml -e intersection.edg.xml -o intersection.net.xml
```

It contains:

* Internal junction logic.
* Allowed vehicle turns.
* Lane definitions.
* Traffic light phases and timings.

### `network/intersection.rou.xml`

This file defines:

* A single vehicle type: `car`.
* Four routes:

  * `north_south`, `south_north`, `east_west`, `west_east`.
* Vehicles `veh0` to `veh3` spawn at intervals (0s, 2s, 4s, 6s) on different routes.

### `network/intersection.sumocfg`

Main SUMO configuration file specifying the network and route files. Used to launch the simulation in both CLI and GUI modes.

---

## `traffic_sim.py`: Main Simulation Script

This Python script uses the `traci` interface to control and monitor the simulation.

### Key Features:

* **Starts the SUMO simulation** using `intersection.sumocfg`.
* **Alternates traffic light phases** every 50 simulation steps.
* **Tracks all active vehicles**:

  * Logs speed, position (`x`, `y`), waiting time, and current edge.
* **Estimates queue length** by counting vehicles with speed < 0.1 m/s.
* **Collects data step-by-step** into a list of dictionaries.
* **Exports analytics**:

  * A CSV file of detailed traffic data.
  * A line chart showing how queue length evolves over time.

---

## Outputs

### `intersection_stats.csv`

| step | vehicle | speed | x | y | wait\_time | edge |
| ---- | ------- | ----- | - | - | ---------- | ---- |

Each row represents the state of a vehicle at a given simulation step. This dataset is useful for:

* Custom traffic analysis.
* Model training for traffic prediction.
* Evaluating the efficiency of traffic light logic.

---

### `queue_plot.png`

* **X-axis**: Simulation steps.
* **Y-axis**: Number of vehicles considered "stopped" (speed < 0.1 m/s).
* This plot helps visualize traffic congestion over time.

### Four-way intersection simulation using sumo-gui

![image](https://github.com/user-attachments/assets/2c78477a-5aaf-4420-82e5-226e1ba7192c)

---

## How to Run the Simulation

1. **Make sure SUMO is installed and available in your path.**

2. (Optional) **Generate the network** if `intersection.net.xml` is missing:

   ```bash
   netconvert -n network/intersection.nod.xml -e network/intersection.edg.xml -o network/intersection.net.xml
   ```

3. **Run SUMO GUI to visualize the simulation**:

   ```bash
   sumo-gui -c network/intersection.sumocfg
   ```

4. **Run the simulation with Python to collect data**:

   ```bash
   python traffic_sim.py
   ```

After the run:

* Check `intersection_stats.csv` for detailed simulation data.
* Open `queue_plot.png` to view the queue trend.

---

## Summary

This project provides a compact framework for experimenting with traffic light logic and vehicle flow through a simple intersection. It’s a great starting point for:

* Traffic signal optimization experiments.
* Studying urban mobility patterns.
* Learning how to use SUMO + Python (TraCI).
