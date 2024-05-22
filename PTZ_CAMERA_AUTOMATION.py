import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import json

# Set Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Optional: Run in headless mode if you don't need a browser window
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')

# Set authentication credentials
username = "admin"
password = "Orbital227"

# Read IP addresses from CSV file
with open('ip_addr.csv', newline='') as csvfile:
    ip_reader = csv.reader(csvfile)
    for row in ip_reader:
        ip_address = row[0]
        url = f"http://{username}:{password}@{ip_address}:8081/wmf/index.html#/setup/basic_videoProfile"
        
        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Navigate to the URL (this will automatically authenticate)
        driver.get(url)
        
        # Wait for the page to load after authentication
        wait = WebDriverWait(driver, 30)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="profilepage"]')))
            
        # Selecting Profile (H.264, H.265 ETC)
        for profile_num in range(1, 4):
            # Selecting Profile Radio button
            profile_radio_button_id = f"profileRadio{profile_num}"
            radio_button = driver.find_element(By.ID, profile_radio_button_id)
            driver.execute_script("arguments[0].click();", radio_button)
            
            # Find the resolution dropdown
            resolution_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="profilepage"]/div/div[6]/div[4]/div[2]/div[1]/div[2]/select'))
            if profile_num == 1:
                desired_resolution = "string:3840x2160"
            else:
                desired_resolution = "string:1920x1080"
            resolution_dropdown.select_by_value(desired_resolution)
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'modal')))
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'tui-loading-animate')))

            # Setting frame rate
            fps_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="profilepage"]/div/div[6]/div[4]/div[2]/div[2]/div[2]/select'))
            if profile_num == 1:
                desired_fps_value = "number:15"
            elif profile_num == 2:
                desired_fps_value = "number:15"
            elif profile_num == 3:
                desired_fps_value = "number:2"
            fps_dropdown.select_by_value(desired_fps_value)

            # Setting maximum bitrate
            bitrate_input = driver.find_element(By.XPATH, '//*[@id="profilepage"]/div/div[6]/div[4]/div[2]/div[3]/div[3]/input')
            if profile_num == 1:
                bitrate_input_value = "8192"
            elif profile_num == 2:
                bitrate_input_value = "2048"
            elif profile_num == 3:
                bitrate_input_value = "4000"
            bitrate_input.clear()  # Clear any existing value
            bitrate_input.send_keys(bitrate_input_value)

            # Find and click the "Apply" button
            apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="profilepage"]/div/div[7]/div/button[1]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)  # Scroll to the button
            apply_button.click()
            
            # Wait for the confirmation box
            confirmation_box = wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/form/div[3]/button[1]')))
            confirmation_box.click()
            
            # Wait for the confirmation box to disappear
            wait.until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/form/div[3]/button[1]')))
        
        # Quit WebDriver
        driver.quit()