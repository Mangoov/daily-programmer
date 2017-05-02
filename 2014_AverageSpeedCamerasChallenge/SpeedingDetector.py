__author__ = 'ejullap'
import re
from _datetime import datetime


class SpeedingDetector:
    camera_logs = []
    speed_limit = float()
    camera_positions = []
    speeding_cars = dict()

    def parse_speed_log(self, log_name):
        speed_log = open(log_name, 'r')
        camera_logs = {}
        for log_line in speed_log:
            if log_line.startswith("Speed limit"):
                if "mph" in log_line:
                    self.speed_limit = float(re.findall("\d+.\d+", log_line)[0])*1.61
                else:
                    self.speed_limit = float(re.findall("\d+.\d+", log_line)[0])
            elif log_line.startswith("Speed camera"):
                numbersInString = [int(s) for s in log_line.split() if s.isdigit()]
                self.camera_positions.append(numbersInString[1])
            elif log_line.startswith("Start of log"):
                if len(camera_logs) != 0:
                    self.camera_logs.append(camera_logs)
                camera_logs = {}
            elif log_line.startswith("Vehicle"):
                licensePlate = self.get_license_plate(log_line)
                timestamp = self.get_timestamp(log_line)
                camera_logs[licensePlate] = timestamp

    def get_license_plate(self, log_line):
        return log_line[8:16]

    def get_timestamp(self, log_line):
        timestamp = log_line[-10:].strip("\n").strip(".").strip(" ")
        return timestamp

    def get_all_speeding_vehicles(self):
        for i in range(0, len(self.camera_positions)-2):
            self.get_speeding_vehicle_between_cameras(i, i+1)
        for vehicle in self.speeding_cars:
            print("Vehicle " + str(vehicle) + " was speeding " + str(self.speeding_cars[vehicle]) + " over limit")

    def get_speeding_vehicle_between_cameras(self, camera1, camera2):
        distance = self.camera_positions[camera2] - self.camera_positions[camera1]
        for vehicle in self.camera_logs[camera1]:
            camera1_time = self.camera_logs[camera1][vehicle]
            camera2_time = self.camera_logs[camera2][vehicle]
            time_for_distance = (datetime.strptime(camera2_time, "%H:%M:%S") - datetime.strptime(camera1_time, "%H:%M:%S")).total_seconds()
            speed = (3600 * distance / 1000) / time_for_distance
            if speed > self.speed_limit:
                self.speeding_cars[vehicle] = round(speed - self.speed_limit, 2)







speedDetector = SpeedingDetector()
speedDetector.parse_speed_log("speed_logs.txt")
speedDetector.get_all_speeding_vehicles()