# MLR Networks Discover Script

Script to read in a list of devices and execute a CLI command, saving the output to a Excel file. Periodically re-executing the command and saving a new set of output every 8 hours when run as a deamon.

## Build and start the image.

Run the image as a deamon:

docker-compose up --build -d

Run the image with interactive feedback:

docker-compose up --build

## Change Target Devices

To change the devices that the script will target update the switches.csv within the /app folder.



