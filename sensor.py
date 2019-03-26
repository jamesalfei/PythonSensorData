import requests
import time
import json


G_FORCE_UPPER_THRESHOLD =  0.14
G_FORCE_LOWER_THRESHOLD = -0.14

GYRO_UPPER_THRESHOLD =  20
GYRO_LOWER_THRESHOLD = -20

TOM_ENDPOINT = "https://justtrack-api.herokuapp.com/messenger/notify"

events = {
    "crash": "1",
    "theft": "2"
}

# r = requests.post(TOM_ENDPOINT, data=events["crash"])
# print(r.text)

while True:

    # GET DATA
    with open("reading.json", "r") as f:
        data = json.load(f)
        accelerometer_reading = float(data["accelerometer"]["x"])
        gyroscopic_reading = float(data["gyro"]["x"])

    # SHOW DATA
    print("Accelerometer X-Axis reading: " + str(round(accelerometer_reading, 2)))
    print("Gyroscope X-Axis reading: " + str(round(gyroscopic_reading, 2)))

    # COMPARE READINGS AGAINST THRESHOLDS
    if (accelerometer_reading > G_FORCE_UPPER_THRESHOLD
        or accelerometer_reading < G_FORCE_LOWER_THRESHOLD
        or gyroscopic_reading > GYRO_UPPER_THRESHOLD
        or gyroscopic_reading < GYRO_LOWER_THRESHOLD):
        print("Sending SMS: 'GRAND THEFT AUTO UNDERWAY!'")
        break

    print("Sleeping...\n")
    time.sleep(1)
