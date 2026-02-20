# Hospital Manager – Emergency Room Simulation 🏥

A real-time Emergency Room simulation built using **Python and Pygame**.
This project models a **multi-server priority queueing system** using discrete-event simulation principles.

The system simulates stochastic patient arrivals, severity-based prioritization, doctor assignment, and treatment completion in a dynamic graphical environment.

---

##  Game Screenshots

###  Emergency Room View
<img width="900" height="811" alt="image" src="https://github.com/user-attachments/assets/eb4f8cdc-eea1-4e8a-9e92-6c7118de2709" />

###  Patient Under Treatment
<img width="900" height="824" alt="image" src="https://github.com/user-attachments/assets/5dd72cd3-166c-4e78-b92a-82bec9715d95" />

###  Waiting Area Queue
<img width="883" height="816" alt="image" src="https://github.com/user-attachments/assets/420ee8a1-a6d9-4bc1-a1ad-d8ffc23f814a" />


---

##  Features

* Real-time discrete-event simulation
* Multi-doctor (multi-server) system
* Severity-based priority queue (Critical > Moderate > Minor)
* Heap-based scheduling using `heapq`
* Adjustable number of doctors
* Adjustable patient arrival probability
* Custom simulation duration (in minutes)
* Start / Pause / Resume / Restart controls
* Scrollable hospital layout
* Live statistics panel (time, queue size, treated count)

---

##  Simulation Model

### Patient Severity Structure

| Severity | Priority | Service Time (seconds) |
| -------- | -------- | ---------------------- |
| Critical | 1        | 20 – 30                |
| Moderate | 2        | 10 – 20                |
| Minor    | 3        | 5 – 10                 |

Lower numerical priority means higher urgency.

The system follows a **non-preemptive priority queue discipline**.

---

##  How It Works

Each simulation step:

1. Increments simulation time
2. Generates patient arrivals probabilistically
3. Updates service time for busy doctors
4. Releases doctors when treatment completes
5. Assigns highest-priority waiting patient
6. Updates waiting time of queued patients

The simulation ends when the defined duration is reached.

---

##  Performance Metrics

The simulation tracks:

* Total patients treated
* Queue length
* Simulation time
* Throughput
* Doctor utilization
* Average waiting time

These metrics allow analysis of congestion and system stability.

---

##  Project Structure

```
Hospital-Simulation/
│
├── config.py
├── entities.py
├── simulation.py
├── ui.py
├── main.py
├── Assets/
```

---

##  Installation & Run

### Requirements

* Python 3.x
* Pygame

### Install Pygame

```
pip install pygame
```

### Run the Simulation

```
python main.py
```

---

##  Mathematical Model

Arrival Rate:

λ = p

Service Rate:

μ = 1 / Avg(Service Time)

Utilization:

ρ = λ / (cμ)

Where:

* `c` = number of doctors
* Stability condition: ρ < 1

If ρ ≥ 1, the queue grows without bound.

---

##  Concepts Demonstrated

* Discrete Event Simulation
* Priority Queues
* Multi-Server Queueing Systems
* Stochastic Modeling
* Event-Driven Programming
* Real-Time GUI Rendering

---

This project serves as a dynamic experimental tool for analyzing emergency department congestion, resource allocation, and system stability under uncertainty.
