import time

# To make this class better output limits could be added
# as well as direction of regulation (cooling or heating)
# Limiting integration sum could also be implemented to minimize overshooting

class PID:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.input = 0
        self.output = 0

        self.I = 0

        self.prev_time = time.time()
        self.prev_error = 0
        self.error = 0


    def compute(self): #computing PID output using variable dt
        error = -(self.setpoint - self.input) # negative sign because system is cooling
        self.I = self.I + error * self.ki * (time.time() - self.prev_time) #multiplying by ki here
        D = (error - self.prev_error) / (time.time() - self.prev_time)
        D = -D # negative sign because system is cooling

        self.output = error * self.kp + self.I + D * self.kd #computing output
        self.prev_error = self.error
        self.prev_time = time.time()

    def get_output(self):
        return self.output
    
    def set_setpoint(self, setpoint):
        self.setpoint = setpoint

    def set_input(self, input):
        self.input = input