import random
import heapq


class EmergencyRoomSimulation:
    def __init__(self, num_doctors=3, arrival_prob=0.15, sim_time=480):
        self.sim_time = sim_time
        self.current_time = 0
        self.arrival_prob = arrival_prob

        self.doctors = []
        self.set_doctors(num_doctors)

        self.queue = []
        self.total_treated = 0

        self.severity_levels = {
            "Critical": {"priority": 1, "service": (20, 30)},
            "Moderate": {"priority": 2, "service": (10, 20)},
            "Minor": {"priority": 3, "service": (5, 10)}
        }

    # ------------------------
    # Dynamic Controls
    # ------------------------
    def set_doctors(self, num_doctors):
        current = len(self.doctors)
        if num_doctors > current:
            for _ in range(num_doctors - current):
                self.doctors.append({"status": "free", "patient": None, "time_left": 0})
        elif num_doctors < current:
            self.doctors = self.doctors[:num_doctors]

    def set_arrival_probability(self, prob):
        self.arrival_prob = max(0.01, min(prob, 1))

    # ------------------------
    # Random Generators
    # ------------------------
    def generate_severity(self):
        r = random.random()
        if r < 0.2:
            return "Critical"
        elif r < 0.5:
            return "Moderate"
        else:
            return "Minor"

    def generate_service_time(self, severity):
        low, high = self.severity_levels[severity]["service"]
        return random.randint(low, high)

    # ------------------------
    # Simulation Step
    # ------------------------
    def step(self):
        if self.current_time >= self.sim_time:
            return False

        self.current_time += 1

        # Arrival
        if random.random() < self.arrival_prob:
            severity = self.generate_severity()
            priority = self.severity_levels[severity]["priority"]
            patient = {"severity": severity, "waiting_time": 0}
            heapq.heappush(self.queue, (priority, self.current_time, patient))

        # Update doctors
        for doctor in self.doctors:
            if doctor["status"] == "busy":
                doctor["time_left"] -= 1
                if doctor["time_left"] <= 0:
                    doctor["status"] = "free"
                    doctor["patient"] = None
                    self.total_treated += 1

        # Assign patients
        for doctor in self.doctors:
            if doctor["status"] == "free" and self.queue:
                _, _, patient = heapq.heappop(self.queue)
                service_time = self.generate_service_time(patient["severity"])
                doctor["status"] = "busy"
                doctor["patient"] = patient["severity"]
                doctor["time_left"] = service_time

        # Update waiting times
        updated_queue = []
        while self.queue:
            priority, arrival, patient = heapq.heappop(self.queue)
            patient["waiting_time"] += 1
            updated_queue.append((priority, arrival, patient))

        for item in updated_queue:
            heapq.heappush(self.queue, item)

        return True
