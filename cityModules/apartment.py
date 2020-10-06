from marshmallow import Schema, fields


class Apartment:

    def __init__(self, apartment_number):
        self.apartment_number = apartment_number
        self.sunlight_start = None
        self.sunlight_stop = None

    def __str__(self):
        return "number: {} / sunlight_start: {} / sunlight_stop: {}".format(self.apartment_number, self.sunlight_start, self.sunlight_stop)

    def set_sunlight_hours(self, sunlight_start, sunlight_stop):
        self.sunlight_start = sunlight_start
        self.sunlight_stop = sunlight_stop

    def get_sunlight_hours(self):
        return self.sunlight_start, self.sunlight_stop


class ApartmentSchema(Schema):

    apartment_number = fields.Int(required=True)
    sunlight_start = fields.Time()
    sunlight_stop = fields.Time()

    class Meta:
        fields = ("apartment_number", "sunlight_start", "sunlight_stop")
        ordered = True