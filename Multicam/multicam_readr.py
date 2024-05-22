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

# Output CSV file
output_file = 'reader_output.csv'

# Initialize CSV writer
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['IP', 'Channel', 'Profile', 'Resolution', 'Bitrate', 'Frame'])

    # Read IP addresses from CSV file
    with open('ip_addr.csv', newline='') as csvfile:
        ip_reader = csv.reader(csvfile)
        for row in ip_reader:
            ip_address = row[0]
            url = f"http://{username}:{password}@{ip_address}:8082/wmf/index.html#/setup/basic_videoProfile"
            
            # Initialize WebDriver
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            
            try:
                # Navigate to the URL (this will automatically authenticate)
                driver.get(url)
                
                # Wait for the page to load after authentication
                wait = WebDriverWait(driver, 40)
                wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="profilepage"]')))
                
                # Loop through each camera channel
                for camera_num in range(1, 5):
                    
                    camera_button_xpath = f'//*[@id="setup-channel-selector"]/div[2]/ul/li[3]/div[1]/button[{camera_num}]'
                    
                    # Locate and click the camera button
                    camera_button = driver.find_element(By.XPATH, camera_button_xpath)
                    driver.execute_script("arguments[0].scrollIntoView(true);", camera_button)
                    camera_button.click()

                    # Wait for loading overlay to disappear
                    overlay_xpath = '//div[contains(@class, "tui-loading-animate")]'
                    WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, overlay_xpath)))
                    wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="profilepage"]')))

                    # Loop through each profile (H.264, H.265, Cobra Vision)
                    profiles = ["H.264", "H.265", "Cobra Vision"]
                    for profile_num in range(1, 4):
                        # Selecting Profile Radio button
                        profile_radio_button_id = f"profileRadio{profile_num}"
                        radio_button = wait.until(EC.element_to_be_clickable((By.ID, profile_radio_button_id)))
                        driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
                        driver.execute_script("arguments[0].click();", radio_button)

                        # Wait for elements to disappear
                        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'tui-loading-animate')))
                        
                        # Read current profile settings
                        resolution_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="profilepage"]/div/div[6]/div[2]/div[1]/div[2]/select'))
                        current_resolution = resolution_dropdown.first_selected_option.text
                        
                        fps_dropdown = Select(driver.find_element(By.XPATH, '//*[@id="profilepage"]/div/div[6]/div[2]/div[2]/div[2]/select'))
                        current_fps = fps_dropdown.first_selected_option.text
                        
                        bitrate_input = driver.find_element(By.XPATH, '//*[@id="profilepage"]/div/div[6]/div[2]/div[4]/div[3]/input')
                        current_bitrate = bitrate_input.get_attribute('value')
                        
                        # Write the data to CSV
                        writer.writerow([ip_address, f"Channel {camera_num}", profiles[profile_num - 1], current_resolution, current_bitrate, current_fps])
            
            except Exception as e:
                print(f"Error processing IP {ip_address}: {e}")
            
            finally:
                # Quit WebDriver
                driver.quit()