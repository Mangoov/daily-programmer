__author__ = 'Julien Lapointe'

#Challenge Uncompleted (bugs in code)
#http://www.reddit.com/r/dailyprogrammer/comments/2kpnky/10292014_challenge_186_intermediate_syzygyfication/

from math import cos, sin
from itertools import combinations

class SyzygyDetector:
    planets = ['sun', 'mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus']
    orbital_radius = {'sun': 0.00, 'mercury': 0.38, 'venus': 0.72, 'earth': 1.00,
                     'mars': 1.52, 'jupiter': 5.20, 'saturn': 9.58, 'uranus': 19.19}
    orbital_period = {'sun': 1.00, 'mercury': 0.24, 'venus': 0.62, 'earth': 1.00,
                     'mars': 1.88, 'jupiter': 11.86, 'saturn': 29.46, 'uranus': 84.02}

    planet_combinations = combinations(planets, 2)
    planet_positions = dict()

    def list_syzygy(self, year):
        i = 0.01
        while i <= year:
            self.check_syzygy(i)
            i += 0.01

    def check_syzygy(self, year):
        self.get_planet_positions(year)
        slopes = self.get_syzygy_line_functions(year)
        syzygy_found = []
        aligned_planets = []
        for slope in slopes:
            for planet in self.planet_positions:
                if self.planet_aligned_conditions(slope, planet):
                    aligned_planets.append(planet)
            if len(aligned_planets) >= 3:
                sentence = "Syzygy will occur in " + year + " with " + str(aligned_planets)
                syzygy_found.append(sentence)
            #print(aligned_planets)
            aligned_planets.clear()
        return syzygy_found

    def planet_aligned_conditions(self, slope, planet):
        if type(slope[0]) is None:
            if planet[1] == slope[1]:
                return True
        elif type(slope[0]) is not None and type(slope[1]) is None:
            print("sensitive case")
        else:
            #print(planet, self.planet_positions[planet])
            yResult = self.planet_positions[planet][0] * slope[0] + slope[1]
            yResult = round(yResult, 2)
            #print(yResult, self.planet_positions[planet][1])
            if self.planet_positions[planet][1] == yResult:
                return True
            else:
                return False

    def get_syzygy_line_functions(self, year):
        syzygy_line_functions = []
        for combination in self.planet_combinations:
            syzygy_line_functions.append(self.get_line_function(combination, year))
        return syzygy_line_functions

    def get_line_function(self, planet_combination, year):
        pos1 = self.planet_positions[planet_combination[0]]
        pos2 = self.planet_positions[planet_combination[1]]
        slope = self.get_slope(pos1, pos2)
        intercept = self.get_intercept(pos2, slope)
        return [slope, intercept]

    def get_intercept(self, pos, slope):
        try:
            intercept = pos[1] - (slope * pos[0])
            return round(intercept, 2)
        except (ZeroDivisionError, TypeError):
            return

    def get_slope(self, pos1, pos2):
        try:
            slope = (pos2[1] - pos1[1])/(pos2[0] - pos1[0])
            return slope
        except ZeroDivisionError:
            return pos1[1]

    def get_planet_positions(self, year):
        for planet in self.planets:
            self.planet_positions[planet] = self.get_orbital_position(planet, year)

    def get_orbital_position(self, planet, year):
        angle = self.get_planet_angle(planet, year)
        x = self.orbital_radius[planet] * cos(angle)
        y = self.orbital_radius[planet] * sin(angle)
        return [round(x, 2), round(y, 2)]

    def get_planet_angle(self, planet, year):
        angle = (360 * year / self.orbital_period[planet]) % 360
        return round(angle, 2)

syzygy = SyzygyDetector()
#for thing in syzygy.planet_combinations:
#    print(thing)
print(syzygy.list_syzygy(20))