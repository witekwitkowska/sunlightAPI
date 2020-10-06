# sunlightAPI

A new feature has been requested for our room listings in future Barcelona: we want to display
the sunlight hours that a given apartment receives in a day. 
Calculations are made assuming:
* It is December 22nd sunlight hours, ie sunlight hours will be between 08:14 and 17:25
* Buildings are distributed in neighbourhoods,
* In those neighbourhoods, the buildings are always aligned east to west,
* The sun rises in the east and travels at a constant radial speed until setting,
* The only shadows created in a neighbourhood are artefacts of the buildings in it,
* We consider an apartment receives sunlight when either its eastern or western exterior
wall is fully covered in sunlight and/or when the sun is directly overhead,
* There is only one apartment per floor; in a building with N floors they are numbered from
0 to N-1.

API has two endpoints defined:
* init method that takes a String containing a JSON describing the city, with this format:
[{ neighborhood: <name_string>, apartments_height: <number>, buildings: [{name:<name_string>, apartments_count: <number>, distance: <number>}]}]
It is assumed the building list is ordered from east to west.
* getSunlightHours method which takes a neighbourhood name, building name, and
apartment number. It returns the sunlight hours as a string like “hh:mm:ss - hh:mm:ss” in
24hr format.

## Running the project

In new virtual environment (Python 3) run:

`pip3 install -r requirements.txt`  

And start server with:

` python3 main.py `  
