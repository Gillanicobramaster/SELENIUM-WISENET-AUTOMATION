import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
# Set Chrome options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Optional: Run in headless mode if you don't need a browser window
chrome_options.add_argument('--ignore-ssl-errors=yes')
chrome_options.add_argument('--ignore-certificate-errors')

# Set authentication credentials
username = "admin"
password = "Orbital227"
def write_to_csv(ip, channel, status):
    with open('output.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([ip, f"{channel}", status])

# Read IP addresses from CSV file
with open('ip_addr.csv', newline='') as csvfile:
    ip_reader = csv.reader(csvfile)
    for row in ip_reader:
        ip_address = row[0]
        url = f"http://{username}:{password}@{ip_address}:8082/wmf/index.html#/setup/basic_videoProfile"
        
        # Initialize WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Navigate to the URL (this will automatically authenticate)
        driver.get(url)
        
        # Wait for the page to load after authentication
        wait = WebDriverWait(driver, 40)
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="profilepage"]')))
        
        camera_button_xpath = f'//*[@id="setup-channel-selector"]/div[2]/ul/li[3]/div[1]/button[4]'        
        # Locate and scroll the camera button into view
        camera_button = driver.find_element(By.XPATH, camera_button_xpath)    
        # Click on the camera button
        camera_button.click()
        overlay_xpath = '//div[contains(@class, "tui-loading-animate")]'
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, overlay_xpath)))
        print("Overlay disappeared")
        wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="profilepage"]')))
        for profile_num in range(1, 4):
            # Select profile radio button
            profile_radio_button_id = f"profileRadio{profile_num}"
            radio_button = wait.until(EC.element_to_be_clickable((By.ID, profile_radio_button_id)))
            driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
            driver.execute_script("arguments[0].click();", radio_button)
            print("Radio button clicked")
                
                
            # Wait for the page to fully update with new profile settings
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'tui-loading-animate')))
                
            # Find the resolution dropdown and select desired resolution
            resolution_dropdown = Select(driver.find_element(By.XPATH, '//*[@name="Resolution"]'))
            resolution_dropdown.select_by_value("string:1920x1080")
                
            # Wait for elements to disappear
            wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'tui-loading-animate')))
                
            # Find and select FPS dropdown
            fps_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="profilepage"]/div/div[6]/div[2]/div[2]/div[2]/select'))
            if profile_num == 1:
                desired_fps_value = "number:10"
            elif profile_num == 2:
                desired_fps_value = "number:15"
            elif profile_num == 3:
                desired_fps_value = "number:2"
            fps_dropdown.select_by_value(desired_fps_value)
                
            # Find and set maximum bitrate
            bitrate_input = driver.find_element(By.XPATH, '//*[@id="profilepage"]/div/div[6]/div[2]/div[4]/div[3]/input')
            bitrate_input.clear()
            if profile_num == 1:
                bitrate_input_value = "2560"
            elif profile_num == 2:
                bitrate_input_value = "2560"
            elif profile_num == 3:
                bitrate_input_value = "4000"
            bitrate_input.send_keys(bitrate_input_value)
                
            # Find and click the "Apply" button
            apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="profilepage"]/div/div[10]/button[1]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", apply_button)
            # Click the apply_button
            apply_button.click()
            time.sleep(3)

            # Confirm the settings
            confirmation_box_xpath = '//button[@ng-click="ok()"]'
            confirmation_box = wait.until(EC.element_to_be_clickable((By.XPATH, confirmation_box_xpath)))
            driver.execute_script("arguments[0].scrollIntoView(true);", confirmation_box)
            driver.execute_script("arguments[0].click();", confirmation_box)
            print("Confirmation OK button clicked")
            print(f"Profile {profile_num}: Confirmation accepted")
            time.sleep(5)
        write_to_csv(ip_address, "Channel 4", "Done")
        # Quit WebDriver
        driver.quit()