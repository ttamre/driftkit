# driftkit
[![CircleCI](https://circleci.com/gh/ttamre/driftkit/tree/master.svg?style=svg)](https://circleci.com/gh/ttamre/driftkit/tree/master)

Python script that reads speed camera data and displays their locations, distance from you, and other important information. Designed to work with data from the City of Edmonton open data portal.

![demo](demo.gif)


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Create a virtual environment and install the required dependencies
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

### Installing

Clone the repository into a location of your choosing

```
$ git clone https://github.com/ttamre/driftkit.git
```


### Usage
```
. venv/bin/activate   # if not already active
python3 driftkit.py
```

```
  _____  _____  _____ ______ _______ _  _______ _______ 
 |  __ \|  __ \|_   _|  ____|__   __| |/ /_   _|__   __|
 | |  | | |__) | | | | |__     | |  | ' /  | |    | |   
 | |  | |  _  /  | | |  __|    | |  |  <   | |    | |   
 | |__| | | \ \ _| |_| |       | |  | . \ _| |_   | |   
 |_____/|_|  \_\_____|_|       |_|  |_|\_\_____|  |_|   
 
----------------------------------------------------------------------
Checking for update...
Data already up to date
----------------------------------------------------------------------
Would you like to use the terminal or the webserver interface?
> 
```
Enter ```terminal``` (webserver interface is not yet functional)

```
Current Latitude >
Current Longitude >
```
Enter your latitude and longitude (you can get this information in Google Maps) as precisely as you can to ensure accuracy (a missing digit can throw off the distance calculations by a very large margin)

```
Enter max distance to display cameras from (0 for no limit) >
```
If you want to show cameras within a certain distance from you, enter that distance (in kilometres). Otherwise, enter ```0```

The program will print the camera data

```
Options: refresh, lite, quit
>
```
Enter one of the three options

```refresh``` will ask you for your new coordinates and max distance and update the distances accordingly

```lite``` will re-run the program with a condensed output

```quit``` will exit the program


## Contributing

Please email me at ttamre@ualberta.ca for details on code of conduct, and the process for submitting pull requests.

## Authors

* **Tem Tamre** - *Project Lead/Owner* - [Github](https://github.com/ttamre)

See also the list of [contributors](https://github.com/ttamre/driftkit/graphs/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License - see [LICENSE](LICENSE) for more details
