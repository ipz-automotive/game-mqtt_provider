from r3e_api import R3ESharedMemory
import time
import math
import paho.mqtt.client as mqtt


def on_connect(mqttc, obj, flags, reason_code, properties):
    print("reason_code: " + str(reason_code))


def on_message(mqttc, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


def on_publish(mqttc, obj, mid, reason_code, properties):
    print("mid: " + str(mid))


def on_log(mqttc, obj, level, string):
    print(string)

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
# Uncomment to enable debug messages
# mqttc.on_log = on_log
mqttc.connect("21.37.14.88", 1883)

mqttc.loop_start()

shared_memory = R3ESharedMemory()
shared_memory.update_offsets()
def get_rpm():
    shared_memory.update_buffer()
    engine_rps = shared_memory.get_value('EngineRps')
    rpm = engine_rps * (60 / (2 * math.pi))
    return rpm

while True:
    shared_memory.update_buffer()
    velocity = shared_memory.get_value('Player.Velocity')
    v_m_per_s = math.sqrt(velocity['X']**2 + velocity['Y']**2 + velocity['Z']**2)


    speed_kmh = v_m_per_s * 3.6

    gear = shared_memory.get_value('Gear')
    rpm = get_rpm()
    mqttc.publish("speed", f"{speed_kmh}")
    mqttc.publish("rpm", f"{rpm}")
    mqttc.publish("gear", f"{gear}")
    time.sleep(0.05)
