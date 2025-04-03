import time
import sys
from PID import PID
import matplotlib as plt


SET_TEMP = 60 # temperature to maintain to ensure maximum power operation witohut derating

# Passing command line arguments
try:
    if int(sys.argv[-1]):
        SET_TEMP = int(sys.argv[-1])
except ValueError:
    if (len(sys.argv) > 1):
        print("Invalid command line argument")


EMERGENCY_SHUTDOWN_TEMP = 85 # Temperature threshold for emergency shutdown

# Control constants
PUMP_MAX_SIGNAL = 100 # Pump is running at maximum power
PUMP_MIN_SIGNAL = 0 # Pump is stopped

FAN_MAX_SIGNAL = 100 # Fan is running at maximum power
FAN_MIN_SIGNAL = 0 # Fan is stopped


# PID

# Coefficients should be adjusted when system is running
# to achieve the best regulation and effectiveness

# Coefficients for pump PID
KP_PUMP = 1
KI_PUMP = 1
KD_PUMP = 0

# Coefficients for fan PID
KP_FAN = 1
KI_FAN = 1
KD_FAN = 0

def constrain(value, minimum, maximum):
    return max(min(value, maximum), minimum)

def main():

    time_points = []
    temperature_points = []
    pump_signal_points = []
    fan_signal_points = []

    # Emulated variables
    coolant_temp = 55
    ignition_switch = True # system is on
    pump_speed = 0
    fan_speed = 0


    # PID controller for temperature of the coolant
    pump_pid = PID(KP_PUMP, KI_PUMP, KD_PUMP, SET_TEMP)
    fan_pid = PID(KP_FAN, KI_FAN, KD_FAN, SET_TEMP)


    while ignition_switch:

        # Emergency Shutdown
        if coolant_temp >= EMERGENCY_SHUTDOWN_TEMP:
            ignition_switch = False # Assuming ignition switch also would switch off the inverter
            pump_speed = 0
            fan_speed = 0
            print("Emergency Shutdown")
            break

        # Controlling the pump
        pump_pid.set_input(coolant_temp) # coolant temp needs to be read from the sensor
        pump_pid.compute() 
        pump_speed = constrain(pump_pid.get_output(), PUMP_MIN_SIGNAL, PUMP_MAX_SIGNAL) # set pump speed accordingly to maintain the temperature

        
        # Controlling the fan
        fan_pid.set_input(coolant_temp) # coolant temp needs to be read from the sensor
        fan_pid.compute()
        fan_speed = constrain(fan_pid.get_output(), FAN_MIN_SIGNAL, FAN_MAX_SIGNAL) # set fan speed accordingly to maintain the temperature

        # Emulating cooling effect
        coolant_temp -= 0.1 * fan_speed # Fan has more cooling effect
        coolant_temp -= 0.05 * pump_speed

        #Emulating heating effect
        coolant_temp += 1 # Emulating inverter producing heat


        print(f"Coolant temperature: {round(coolant_temp, 2)}, Fan speed: {round(fan_speed, 2)}, Pump Speed: {round(pump_speed, 2)}")

        time_points.append(time.time())
        temperature_points.append(coolant_temp)
        pump_signal_points.append(pump_speed)
        fan_signal_points.append(fan_speed)

        # Plotting the data
        plt.figure(figsize=(10, 6))
        
        # Temperature plot
        plt.subplot(3, 1, 1)
        plt.plot(time_points, temperature_points, 'r-', label='Temperature')
        plt.axhline(y=SET_TEMP, color='g', linestyle='--', label='Target Temp')
        plt.ylabel('Temperature (°C)')
        plt.title('Cooling System Performance')
        plt.legend()
        plt.grid(True)

        time.sleep(0.5)

if __name__ == "__main__":
    main()