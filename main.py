from flask import Flask
from flask_restful import Api, Resource, request, abort
from cityModules.neighborhood import NeighborhoodSchema

app = Flask(__name__)
api = Api(app)

city = []


def find_neighborhood(neighborhood_name):
    for neighborhood in city:
        if neighborhood.name == neighborhood_name:
            return neighborhood
    return None


class CityController(Resource):

    def init(self, city_data):
        schema = NeighborhoodSchema(many=True)
        city.extend(schema.load(city_data))

    def post(self):
        city_data = request.get_json(force=True)["city_data"]
        self.init(city_data)
        return "City data recieved", 201

    def get(self):
        schema = NeighborhoodSchema(many=True)
        result = schema.dump(city)
        return result

    def delete(self):
        city.clear()
        return "City data removed", 204


api.add_resource(CityController, "/sunlightAPI/barcelona")


class SunlightController(Resource):


    def getSunlightHours(self, neighborhood_name, building_name, apartment_number):
        neighborhood = find_neighborhood(neighborhood_name)
        if not neighborhood:
            abort("Wrong name of neighborhood")
        building = neighborhood.find_building(building_name)
        if not building:
            abort("Wrong building name")
        apartment = building.find_apartment(apartment_number)
        if not apartment:
            abort("Wrong apartment number")
        sunlight_start, sunlight_stop = apartment.get_sunlight_hours() if all(apartment.get_sunlight_hours()) \
                                        else neighborhood.compute_sunlight_hours(building, apartment)
        return "{} - {}".format(sunlight_start, sunlight_stop)

    def get(self, neighborhood_name, building_name, apartment_number):
        return self.getSunlightHours(neighborhood_name, building_name, apartment_number)


api.add_resource(SunlightController, "/sunlightAPI/barcelona/<string:neighborhood_name>/<string:building_name>/<int:apartment_number>/")

if __name__ == "__main__":
    app.run(debug=True)
