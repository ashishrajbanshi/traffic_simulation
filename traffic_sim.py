import traci
import pandas as pd
import matplotlib.pyplot as plt

def run_sim():
    traci.start(["sumo", "-c", "network/intersection.sumocfg"])

    step = 0
    data = []

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        # Control traffic light
        phase = step // 50 % 2  # switch every 50 steps
        traci.trafficlight.setPhase("J", phase)

        # Track each vehicle
        for vid in traci.vehicle.getIDList():
            speed = traci.vehicle.getSpeed(vid)
            pos = traci.vehicle.getPosition(vid)
            wait = traci.vehicle.getWaitingTime(vid)
            edge = traci.vehicle.getRoadID(vid)
            data.append({
                "step": step,
                "vehicle": vid,
                "speed": speed,
                "x": pos[0],
                "y": pos[1],
                "wait_time": wait,
                "edge": edge
            })
        step += 1

    traci.close()
    df = pd.DataFrame(data)
    df.to_csv("intersection_stats.csv", index=False)

    # Plot queue length by step
    df['stopped'] = df['speed'] < 0.1
    queue_length = df[df['stopped']].groupby('step').size()

    queue_length.plot()
    plt.xlabel("Step")
    plt.ylabel("Queue Length")
    plt.title("Queue Length Over Time")
    plt.savefig("queue_plot.png")

if __name__ == "__main__":
    run_sim()
