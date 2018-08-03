
# driftkit
Python script that reads speed camera data and displays their locations, distance from you, and other important information. Designed to work with data from the City of Edmonton open data portal.

![demo](assets/demo.gif)


## File structure
Generated by [autoTree.py](https://github.com/shavavo/autoTreeFormat)
```
├── assets                  # Non-code files
│   └── data.csv            # Intersection safety device data
├── templates               #
|   ├── index.html          # Flask webserver main page
|   └── map.html            # Map page
|
├── driftkit.py             # Main file (the file that you run)
├── README.md               # General documentation (this file)
└   LICENSE                 # MIT License
```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
Install the following modules if you don't already have them
```
$ pip install flask
$ pip install haversine
$ pip install requests
$ pip install socket
```

### Installing

Simply clone the repository into a location of your choosing

```
$ git clone https://github.com/ttamre/driftkit.git
```


## Running driftkit

### Starting the program
If your default python version is version 3.x, run the following in your terminal
```
$ python driftkit.py
```

If it is something else, run the following in your terminal instead
```
$ python3 driftkit.py
```

To check your default python version, run the following command
```
$ python --version
```

### Usage
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

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the GNU General Public License - see [LICENSE](LICENSE) for more details