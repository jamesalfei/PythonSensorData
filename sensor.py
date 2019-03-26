import requests
import time
from datetime import datetime
from datetime import timedelta

ENABLE_TEXTS = False
ENABLE_DB = False

G_FORCE_UPPER_THRESHOLD = 0.14
G_FORCE_LOWER_THRESHOLD = -0.14

GYRO_UPPER_THRESHOLD = 20
GYRO_LOWER_THRESHOLD = -20

TIME_THRESHOLD_IN_SECONDS = 60
timestamp = datetime.now() - timedelta(seconds=60)

TOM_ENDPOINT = "https://justtrack-api.herokuapp.com/messenger/notify"
DEE_ENDPOINT = "https://justtrack-api.herokuapp.com/sensor/input"
TOM_JSON = {
    "status-code": "1"
}

print("Application started at " + str(timestamp))


def should_trigger():
    if (accelerometer_reading_x > G_FORCE_UPPER_THRESHOLD or accelerometer_reading_x < G_FORCE_LOWER_THRESHOLD or
        accelerometer_reading_y > G_FORCE_UPPER_THRESHOLD or accelerometer_reading_y < G_FORCE_LOWER_THRESHOLD or
        gyroscopic_reading_x > GYRO_UPPER_THRESHOLD or gyroscopic_reading_x < GYRO_LOWER_THRESHOLD or
        gyroscopic_reading_y > GYRO_UPPER_THRESHOLD or gyroscopic_reading_y < GYRO_LOWER_THRESHOLD):
        return True
    return False


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
        print("Accelerometer Y-Axis reading: " + str(round(accelerometer_reading_y, 2)))
        print("Gyroscope X-Axis reading: " + str(round(gyroscopic_reading_x, 2)))
        print("Gyroscope Y-Axis reading: " + str(round(gyroscopic_reading_y, 2)))

        if ENABLE_DB:
            # Persist data
            new_data = {
                "A_X": data["accelerometer"]["x"],
                "A_Y": data["accelerometer"]["y"],
                "A_Z": data["accelerometer"]["z"],
                "G_X": data["gyro"]["x"],
                "G_Y": data["gyro"]["y"],
                "G_Z": data["gyro"]["z"]
            }

            r = requests.post(DEE_ENDPOINT, json=new_data)

        # COMPARE READINGS AGAINST THRESHOLDS
        if should_trigger():
            print("Triggered")
            # SEND MY TEXT HERE
            if datetime.now() > (timestamp + timedelta(seconds=TIME_THRESHOLD_IN_SECONDS)):
                timestamp = datetime.now()
                print("Sending text")

                if ENABLE_TEXTS:
                    r = requests.post(TOM_ENDPOINT, json=TOM_JSON)
                    print(r.status_code)
            else:
                print("NOT Sending text")

        print("\n")
        time.sleep(1)
    except KeyboardInterrupt:
        break

