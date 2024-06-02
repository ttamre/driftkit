# driftkit
<img src="https://img.shields.io/badge/python-3.12.3-blue" /> [![CircleCI](https://circleci.com/gh/ttamre/driftkit/tree/master.svg?style=shield)](https://circleci.com/gh/ttamre/driftkit/tree/master)


Python script that reads speed camera data and displays their locations, distance from you, and other important information.

Works with the City of Edmonton's open data portal, https://data.edmonton.ca


## Getting Started

### Installation
Download the project, create a virtual environment, and install the required dependencies
```
git clone https://github.com/ttamre/driftkit.git
cd driftkit

python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt
```

### Usage
```
. venv/bin/activate   # if not already active
python3 driftkit.py
```

```
----------------------------------------------------------------------
 _____  _____  _____ ______ _______ _  _______ _______ 
|  __ \|  __ \|_   _|  ____|__   __| |/ /_   _|__   __|
| |  | | |__) | | | | |__     | |  | ' /  | |    | |   
| |  | |  _  /  | | |  __|    | |  |  <   | |    | |   
| |__| | | \ \ _| |_| |       | |  | . \ _| |_   | |   
|_____/|_|  \_\_____|_|       |_|  |_|\_\_____|  |_|   
 
----------------------------------------------------------------------
Location >               # Enter your current address (or any address)
----------------------------------------------------------------------
```

```
Max radius (0 for no limit) >  # Enter a max radius to search
```



The program will print the camera data

```
Options: refresh, lite, traps, quit
>
```
Enter one of the three options

```r``` or ```refresh``` will ask you for a new address and max distance and update the distances accordingly

```l``` or ```lite``` will re-run the program with a condensed output

```t``` or ```traps``` will show you speed trap zones near you

```q``` or ```quit``` will exit the program

## License

This project is licensed under the GNU General Public License - see [LICENSE](LICENSE) for more details

![demo](demo.gif)