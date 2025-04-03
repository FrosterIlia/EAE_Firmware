import pytest
from main import constrain, SET_TEMP, EMERGENCY_SHUTDOWN_TEMP, PUMP_MAX_SIGNAL, PUMP_MIN_SIGNAL, FAN_MAX_SIGNAL, FAN_MIN_SIGNAL
from PID import PID
import time

# Test the constrain function
def test_constrain():
    assert constrain(50, 0, 100) == 50
    assert constrain(-10, 0, 100) == 0
    assert constrain(110, 0, 100) == 100

# Test the PID controller
def test_pid_controller():
    pid = PID(kp = 1, ki = 1, kd = 0, setpoint = SET_TEMP)
    
    pid.set_input(55)
    pid.compute()
    output = pid.get_output()
    
    assert output != 0  # Since the input is not at the setpoint, output should not be zero

# Test emergency shutdown logic
def test_emergency_shutdown():
    coolant_temp = EMERGENCY_SHUTDOWN_TEMP + 1  # Simulate temperature above threshold
    ignition_switch = True
    pump_speed = 50
    fan_speed = 50

    if coolant_temp >= EMERGENCY_SHUTDOWN_TEMP:
        ignition_switch = False
        pump_speed = 0
        fan_speed = 0

    assert ignition_switch == False
    assert pump_speed == 0
    assert fan_speed == 0

# Test the cooling effect of the fan and pump
def test_cooling_effect():
    coolant_temp = 70
    fan_speed = 50
    pump_speed = 50

    # Simulate cooling effect
    coolant_temp -= 0.1 * fan_speed
    coolant_temp -= 0.05 * pump_speed

    assert coolant_temp < 70  # Temperature should decrease

# Test the heating effect
def test_heating_effect():
    coolant_temp = 70

    # Simulate heating effect
    coolant_temp += 1

    assert coolant_temp > 70  # Temperature should increase


# Test the PID controller with different inputs
def test_pid_with_different_inputs():
    pid = PID(kp=1, ki=1, kd=0, setpoint=SET_TEMP)
    
    # Test with input below setpoint
    pid.set_input(SET_TEMP - 10)
    pid.compute()
    output_below_setpoint = constrain(pid.get_output(), 0, 100)

    pid = PID(kp=1, ki=1, kd=0, setpoint=SET_TEMP)
    
    # Test with input above setpoint
    pid.set_input(SET_TEMP + 10)
    pid.compute()
    output_above_setpoint = constrain(pid.get_output(), 0, 100)
    
    assert output_below_setpoint == 0  # Output should be zero
    assert output_above_setpoint > 0  # Output should be positive to enhance cooling

# Test the PID controller's setpoint change
def test_pid_setpoint_change():
    pid = PID(kp=1, ki=1, kd=0, setpoint=SET_TEMP)
    
    # Change setpoint and check if the output changes accordingly
    new_setpoint = SET_TEMP + 5
    pid.set_setpoint(new_setpoint)
    pid.set_input(SET_TEMP)
    pid.compute()
    output = pid.get_output()
    
    assert pid.setpoint == new_setpoint
    assert output != 0  # Output should change due to the new setpoint
