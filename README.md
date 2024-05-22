# PTZ_CAMERA_AUTOMATION

## Project Description
The Project aims to update settings of Wisenet webpage using selinium to save time. Scripts are written for both ptz and multicams

## Requirements
To install all the requirements run
pip install -r requirements.txt

## Clone the repository:
1. Clone the repository:
    ```sh
    git clone https://github.com//Gillanicobramaster/SELENIUM-WISENET-AUTOMATION.git
    ```
## Files
The project includes mostly 2 types of scripts for two types of cameras. One for PTZ Camera and one for Multi-Cams.
- Script for Updating Settings
- Script for Reading the settings
- **PTZ_CAMERA_AUTOMATION** for updating settings of PTZ Cameras
- **PTZ_CAMERA_READER** for reading the settings of PTZ Cameras

## PTZ_CAMERA_AUTOMATION Script
**PTZ_CAMERA_AUTOMATION** is a Python script that uses Selenium to automate the process of updating settings on PTZ cameras. The script reads IP addresses from a CSV file and modifies various video profiles  (H.264,H.265 AND COBRA VISION) and update settings including resolution, frame rate, and bitrate.


## Usage
1. Prepare a CSV file (`ip_addr.csv`) with the list of IP addresses.
2. Run the script: (For updating settings)
    `python PTZ_CAMERA_AUTOMATION.py`

   
## PTZ READER SCRIPT
**PTZ_CAMERA_READER** is a Python script that uses Selenium to read data of various fields of multiple profiles and saving the result in a csv file

Run the script: (For reading settings)
    `python PTZ_CAMERA_READER.py`

    
# Multi CAMERA AUTOMATION
## File Structure

- **multicam_main.py**: Main Script responsible for updating settings for Channel 1, 2 ,3 and 4 respectively
- **multicam_readr.py** Script which reads various fields from multi cams for all the four channels.
- **Channel..4.py**: Scripts for updating settings of a single channel as indicated by file name i.e Channel1.py for Channel 1 and so

## Usage
1. Prepare a CSV file (`ip_addr.csv`) with the list of IP addresses.
2. Run the script: (For updating settings of all the 4 channels)
    `python multicam_main.py` 
Similarly for reading the script run the following command
`python multicam_readr.py`

