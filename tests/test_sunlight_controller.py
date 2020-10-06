import unittest
import requests

BASE = "http://127.0.0.1:5000/"

JSON = {"city_data":
            [
                {
                    "name": "gracia",
                    "apartments_height": 2.5,
                    "buildings":
                        [
                            {
                                "name": "do",
                                "apartments_count": 4,
                                "distance": 20
                            },
                            {
                                "name": "re",
                                "apartments_count": 6,
                                "distance": 25
                            },
                            {
                                "name": "mi",
                                "apartments_count": 5,
                                "distance": 15
                            },
                            {
                                "name": "fa",
                                "apartments_count": 2,
                                "distance": 20
                            },
                            {
                                "name": "sol",
                                "apartments_count": 1,
                                "distance": 0
                            }
                        ]
                },
                {
                    "name": "example",
                    "apartments_height": 2.50,
                    "buildings":
                        [
                            {
                                "name": "do",
                                "apartments_count": 12,
                                "distance": 0
                            }
                        ]
                }
            ]
}


class TestSunlightController(unittest.TestCase):

    def setUp(self):
        response = requests.post(BASE + "sunlightAPI/barcelona", json=JSON)
        self.assertEqual(response.json(), "City data recieved")

    def test_get(self):
        response = requests.get(BASE + "sunlightAPI/barcelona/gracia/mi/3")
        self.assertEqual(str(response), "<Response [200]>")
        time_format = '([01]?[0-9]|2[0-3]):[0-5][0-9] - ([01]?[0-9]|2[0-3]):[0-5][0-9]'
        self.assertRegex(response.content.decode().strip(), time_format)

    def test_get_not_existing_neighborhood(self):
        response = requests.get(BASE + "sunlightAPI/barcelona/gracian/mi/3")
        self.assertEqual(response.content.decode(), "Wrong name of neighborhood")

    def test_get_not_existing_building(self):
        response = requests.get(BASE + "sunlightAPI/barcelona/gracia/las/3")
        self.assertEqual(response.content.decode(), "Wrong building name")

    def test_get_not_existing_apartment(self):
        response = requests.get(BASE + "sunlightAPI/barcelona/gracia/mi/23")
        self.assertEqual(response.content.decode(), "Wrong apartment number")


if __name__ == '__main__':
    unittest.main()
