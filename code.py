from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Initialize Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

#form URL
url = 'Your_form_link'  # backcheck form

# Excel or Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('Your_credential.json Path', scope)
client = gspread.authorize(creds)

# Opening Sheet
sheet = client.open("Sheet Name").sheet1  #sheet name


data_rows = sheet.get_all_values()[1:]  # Skipink the header row

# If Login required the put your Username and password for login
USERNAME = "__" 
PASSWORD = "__" 


for data in data_rows:
    try:
        # Open the form for each dataset (ensures fresh reload)
        driver.get(url)

        # Handle Login Pageif 
        try:
            # Wait for the username and password fields to load
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
            )
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
            )
            login_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
            )

            # Input
            username_field.send_keys(USERNAME)
            password_field.send_keys(PASSWORD)
            login_button.click()
            print("Login successful!")
        except TimeoutException:
            print("No login page appeared; continuing.")

        # Handle "Unsaved record popup
        try:
            load_record_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "your_path of button if any popup with duplicates entry or other"))
            )
            load_record_button.click()
            print("Popup handled: Clicked 'Button_name' button.")
        except TimeoutException:
            print("No 'Your_button_name' popup appeared.")

        # Wait form to fully load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//form'))
        )

        # Detect all input text areas without entering Xpaths of all
        input_fields = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']"))
        )

        # Fill the input fields of 1st row then 2nd row row wise
        for i, field in enumerate(input_fields):
            if i < len(data):  # don't exceed available data
                try:
                    field.clear()  # Clear if any exist
                    field.send_keys(data[i])  # Enter data from the sheet or excel
                except ElementNotInteractableException:
                    print(f"Input field {i+1} not interactable.")
        
        # Wait for the Submit button
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'submit-form'))
        )
        submit_button.click()

        # Wait for the confirmatio
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "Thank you")]'))
        )

        print(f"Data set {data} submitted successfully!")

    except TimeoutException as e:
        print(f"Timeout occurred for data set {data}: {e}")
    except NoSuchElementException as e:
        print(f"Element not found for data set {data}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for data set {data}: {e}")

# Close the browser after all 
driver.quit()
