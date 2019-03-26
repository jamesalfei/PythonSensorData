import requests
from datetime import datetime
from datetime import timedelta
import sys
import time

G_FORCE_UPPER_THRESHOLD = 0.14
G_FORCE_LOWER_THRESHOLD = -0.14

GYRO_UPPER_THRESHOLD = 20
GYRO_LOWER_THRESHOLD = -20

TIME_THRESHOLD_IN_SECONDS = 60
timestamp = datetime.now() - timedelta(seconds=60)

TOM_ENDPOINT = "https://justtrack-api.herokuapp.com/messenger/notify"
TOM_JSON = {
    "status-code": "1"
}

### POSTING TO TOM'S EVENT ENDPOINT ###
# r = requests.post(TOM_ENDPOINT, json=TOM_JSON)
# print(r.status_code)

print("Application started at " + str(timestamp))

while True:

    try:
        # GET DATA
        data = requests.get("http://localhost:9054/data").json()
        accelerometer_reading_x = float(data["accelerometer"]["x"])
        accelerometer_reading_y = float(data["accelerometer"]["y"])
        gyroscopic_reading_x = float(data["gyro"]["x"])
        gyroscopic_reading_y = float(data["gyro"]["y"])

        # SHOW DATA
        print("Accelerometer X-Axis reading: " + str(round(accelerometer_reading_x, 2)))
        print("Accelerometer X-Axis reading: " + str(round(accelerometer_reading_y, 2)))
        print("Gyroscope X-Axis reading: " + str(round(gyroscopic_reading_x, 2)))
        print("Gyroscope X-Axis reading: " + str(round(gyroscopic_reading_y, 2)))

        # COMPARE READINGS AGAINST THRESHOLDS
        if (accelerometer_reading_x > G_FORCE_UPPER_THRESHOLD or accelerometer_reading_x < G_FORCE_LOWER_THRESHOLD or
                accelerometer_reading_y > G_FORCE_UPPER_THRESHOLD or accelerometer_reading_y < G_FORCE_LOWER_THRESHOLD or
                gyroscopic_reading_x > GYRO_UPPER_THRESHOLD or gyroscopic_reading_x < GYRO_LOWER_THRESHOLD or
                gyroscopic_reading_y > GYRO_UPPER_THRESHOLD or gyroscopic_reading_y < GYRO_LOWER_THRESHOLD):
            print("Triggered")
            if datetime.now() > (timestamp + timedelta(seconds=TIME_THRESHOLD_IN_SECONDS)):
                #Send my text here
                timestamp = datetime.now()
                print('Sending text')
            else:
                print("NOT Sending text")

        print('\n')
        time.sleep(1)
    except KeyboardInterrupt:
        break

new_data = {
        "A_X": None,
        "A_Y": None,
        "A_Z": None,
        "G_X": None,
        "G_Y": None,
        "G_Z": None
}

new_data["A_X"] = data["accelerometer"]["x"]
new_data["A_Y"] = data["accelerometer"]["y"]
new_data["A_Z"] = data["accelerometer"]["z"]
new_data["G_X"] = data["gyro"]["x"]
new_data["G_Y"] = data["gyro"]["y"]
new_data["G_Z"] = data["gyro"]["z"]

