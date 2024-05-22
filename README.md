# PTZ_CAMERA_AUTOMATION
## Files
The project includes mostly 2 types of scripts for two types of cameras. One for PTZ Camera and one for Multi-Cams.
- Script for Updating Settings
- Script for Reading the settings
- **PTZ_CAMERA_AUTOMATION** for updating settings of PTZ Cameras
- **PTZ_CAMERA_READER** for reading the settings of PTZ Cameras

## PTZ_CAMERA_AUTOMATION Script
**PTZ_CAMERA_AUTOMATION** is a Python script that uses Selenium to automate the process of updating settings on PTZ cameras. The script reads IP addresses from a CSV file and modifies various video profiles  (H.264,H.265 AND COBRA VISION) and update settings including resolution, frame rate, and bitrate.

## Requirements
To install all the requirements run
pip install -r requirements.txt

## Clone the repository:
1. Clone the repository:
    ```sh
    git clone https://github.com//Gillanicobramaster/SELENIUM-WISENET-AUTOMATION.git
    ```

## Usage
1. Prepare a CSV file (`ip_addr.csv`) with the list of IP addresses.
2. Run the script:
    `python PTZ_CAMERA_AUTOMATION.py`

## PTZ READER SCRIPT
**PTZ_CAMERA_READER** is a Python script that uses Selenium to read data of various fields of multiple profiles and saving the result in a csv file

