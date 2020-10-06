import math
from typing import List
from marshmallow import Schema, fields, post_load

from cityModules.building import Building, BuildingSchema
from cityModules.apartment import Apartment


class Neighborhood:

    def __init__(self, name: str, apartments_height: float, buildings: List[Building]):
        self.name = name
        self.apartments_height = apartments_height

        self.buildings = buildings

        self.day_length = 9.1833333333  # hours
        self.sunrise_hour = 8.23333333333
        self.sunset_hour = 17.416666666667

    def __str__(self):
        return "name: {} / apartments_height: {} / buildings: {}".format(self.name, self.apartments_height,
                                                                         [str(building) for building in self.buildings])

    def find_building(self, name: str):
        for building in self.buildings:
            if building.name == name:
                return building

        return None

    def get_distance_between_buildings(self, building1: Building, building2: Building):
        distance = 0
        count = False
        for b in self.buildings:
            if (b.name == building1.name or b.name == building2.name) and count == False:
                count = True
                distance += b.distance
                continue
            if (b.name == building1.name or b.name == building2.name) and count == True:
                break
            if count:
                distance += b.distance

        return distance

    def get_angle_between_apartment_and_building(self, apartment: Apartment, target_building: Building,
                                                 source_building: Building):
        rel_height = self.apartments_height * apartment.apartment_number
        rel_building_height = target_building.apartments_count * self.apartments_height - rel_height

        distance = self.get_distance_between_buildings(target_building, source_building)

        print(distance)

        tg = rel_building_height / distance

        return math.degrees(math.atan(tg))

    def compute_sunlight_hours(self, building: Building, apartment: Apartment):
        left_cover_angle = 0
        right_cover_angle = 0

        left = True

        for b in self.buildings:
            if b.name == building.name:
                left = False
                continue

            if left:
                angle = self.get_angle_between_apartment_and_building(apartment, b, building)
                if angle > left_cover_angle:
                    left_cover_angle = angle
            else:
                angle = self.get_angle_between_apartment_and_building(apartment, b, building)
                if angle > right_cover_angle:
                    right_cover_angle = angle

        sunrise_delay = (left_cover_angle * self.day_length) / 180  # [hour]
        sunset_acc = (right_cover_angle * self.day_length) / 180  # [hour]

        sunlight_start = self.sunrise_hour + sunrise_delay
        sunlight_stop = self.sunset_hour - sunset_acc

        sunlight_start_h = int(sunlight_start)
        sunlight_start_m = (sunlight_start * 60) % 60
        sunlight_start_s = (sunlight_start * 3600) % 60

        sunlight_stop_h = int(sunlight_stop)
        sunlight_stop_m = (sunlight_stop * 60) % 60
        sunlight_stop_s = (sunlight_stop * 3600) % 60

        apartment.set_sunlight_hours("%d:%02d:%02d" % (sunlight_start_h, sunlight_start_m, sunlight_start_s),
                                     "%d:%02d:%02d" % (sunlight_stop_h, sunlight_stop_m, sunlight_stop_s))
        return apartment.get_sunlight_hours()


class NeighborhoodSchema(Schema):
    name = fields.Str(required=True)
    apartments_height = fields.Float(required=True)
    buildings = fields.List(fields.Nested(BuildingSchema), required=True)

    class Meta:
        fields = ("name", "apartments_height", "buildings")
        ordered = True

    @post_load
    def make_neighborhood(self, data, **kwargs):
        return Neighborhood(**data)
