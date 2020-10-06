from marshmallow import Schema, fields, post_load
from cityModules.apartment import Apartment


class Building:

    def __init__(self, name: str, apartments_count: int, distance: float):
        self.name = name
        self.apartments_count = apartments_count
        self.distance = distance
        self.apartments = [Apartment(i) for i in range(self.apartments_count)]

    def __str__(self):
        return "name: {} / apartment_count: {} / distance:  {}m / apartments: {}".format(self.name,
                                                                                         self.apartments_count,
                                                                                         self.distance,
                                                                                         [str(apartment) for apartment
                                                                                          in self.apartments])

    def find_apartment(self, ap_nr: int):
        for a in self.apartments:
            if a.apartment_number == ap_nr:
                return a

        return None


class BuildingSchema(Schema):
    name = fields.Str(required=True)
    apartments_count = fields.Int(required=True)
    distance = fields.Int(required=True)
    apartments = fields.List(fields.Nested("ApartmentSchema"))

    class Meta:
        fields = ("name", "apartments_count", "distance", "apartments")
        ordered = True

    @post_load
    def make_building(self, data, **kwargs):
        return Building(**data)