from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep



# NOTE sleep times are needed to wait for page elements to load before sending next command
class Populi_Bot():

    def assignment_checker():
        username = 'charles.parmley@codeimmersives.com'
        password = 'earthday19!@'
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(firefox_options=options)

        # Navigate to assignments page
        driver.get("https://dfa.populiweb.com/router/courseofferings/10734937/assignments/index")
        sleep(1)

        # Enter username in google login form
        elem = driver.find_element_by_id("identifierId")
        elem.send_keys(username)
        elem.send_keys(Keys.RETURN)
        sleep(1)

        # Enter password in google login form
        elem = driver.find_element_by_name("password")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        sleep(4)

        # Grab all the <a></a> tags with a class name of 'remote_name' (assingment links have this class name)
        elem = driver.find_elements_by_class_name("remote_nav")
        
        # Grab the second to last assignment link (This is the newest assignement issued)
        link = elem[-2].get_attribute("href")
        title = elem[-2].get_attribute("innerHTML")
        # Do not close the driver before the 2 'elem' commands above or program fails
        driver.close()

        f = open("Assignment_List.txt", "r")
        assignments = f.readlines()
        f.close()

        # Check assignment file for already existing homework link
        for assignment in assignments:
            # If it already exists exit the function
            if link in assignment:
                return False
        

        # Add the new assignment to the assignments file
        f = open("Assignment_List.txt", "a")
        f.write(f'{title} {link}\n')
        f.close()

        # Pass the homework description and link back to the slack bot for posting
        return title,link

