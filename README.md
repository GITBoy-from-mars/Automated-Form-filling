# Automated-Form-filling Using Selenium
# Fully automated form filling Python Scripts From Database like Excel or Google sheet i implement the google sheet version in it <br>
In this code you can automate your form filling process if the forms are too many and you have data in excel with questions, I use Chromedriver.exe you can find out for your chrome version from here https://googlechromelabs.github.io/chrome-for-testing/#stable <br>

# Lets talk about Process <br>
Firstly Your Chromedriver will initialised and open new chrome window without login and open the form that you i pasted there then it will check if any login page appered it will handeled it make sure you have put correct username or password then it will identify the first input text area with this loop <br>

input_fields = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='text']")) 
        ) <br>


Then it will pull fist column data (Exclude Header) from the database make sure the database has same numbers of questions that asked in form I have maked it for my 1k Questions and around 2lakhs of data <br>

It will Itterate the full data through the for loop when the question will end it will reach the second input area and so on <br>

After all iteration it will click on # Submit Button and if any duplicate popup it will handle this also just enter the text you want to click on popup <br>
And this process continue till the data ends
<br>
Let me know any modification or new to me if any required
TQ
