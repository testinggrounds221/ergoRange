import csv
import random

x_value = 0
angle_1 = 0
angle_2 = 0
angle_3 = 0
i = 0
FIELD_NAMES = ["Time", "Elbow", "Knee", "Spine"]

with open('accuracyGen.csv', 'w') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)
    csv_writer.writeheader()

with open('accuracyGen.csv', 'a') as csv_file:
    csv_writer = csv.DictWriter(csv_file, fieldnames=FIELD_NAMES)

    while i < 120:
        info = {
            "Time": x_value,
            "Elbow": angle_1,
            "Knee": angle_2,
            "Spine": angle_3
        }

        csv_writer.writerow(info)

        print(x_value, angle_1, angle_2, angle_3)

        x_value += 1
        angle_1 = random.randint(0, 100)
        angle_2 = random.randint(0, 100)
        angle_3 = random.randint(0, 100)
        i += 1
