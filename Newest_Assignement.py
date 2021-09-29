from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from datetime import date 



# NOTE sleep times are needed to wait for page elements to load before sending next command
class Populi_Bot():

    # Post new assignments
    def assignment_checker(username,password,options):
        driver = webdriver.Firefox(firefox_options=options)

        # Navigate to assignments page
        print("Opening Populi")
        driver.get("https://dfa.populiweb.com/router/courseofferings/10734937/assignments/index")
        sleep(1)

        # Enter username in google login form
        # print('Entering google user')
        elem = driver.find_element_by_id("identifierId")
        elem.send_keys(username)
        elem.send_keys(Keys.RETURN)
        sleep(3)

        # Enter password in google login form
        # print('Entering google password')
        elem = driver.find_element_by_name("password")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        sleep(5)

        # Grab all the <a></a> tags with a class name of 'remote_name' (assingment links have this class name)
        # print('Finding Assignments')
        elem = driver.find_elements_by_class_name("remote_nav")
        # Add all found assignments to a list
        found_assignments = []
        for item in elem:
            # print('Link added')
            title = item.get_attribute("innerHTML")
            link = item.get_attribute("href")
            found_assignments.append([title,link])

        # Close the webdriver after done using its functions
        driver.close()
        driver.quit()

        # Open the known assignments file and store contents
        f = open("Assignment_List.txt", "r")
        assignments = f.readlines()
        f.close()
        
        # For every assignment link on Populi
        for item in found_assignments:
            flag = True
            # See if it exists in the known assignemnts file contents
            for assignment in assignments:
                title = item[0]
                link = item[1]
                # If it already exists, move to the next link on Populi
                if link in assignment:
                    flag = False
                    break
            # If a Populi assignment link is not in the file
            if flag == True:
                # Add the new assignment to the assignments file
                print("Adding new assignment to file")
                f = open("Assignment_List.txt", "a")
                f.write(f'{title} {link}\n')
                f.close()
                # Pass the homework description and link back to the Slack_Bot for posting
                return title,link


    # Post link to class
    def todays_zoom_link(username,password,options):
        # Open the known dates file and store contents
        f = open("Class_Dates.txt", "r")
        class_days = f.readlines()
        f.close()
        # Get todays date
        today = date.today()
        today = str(today)
        flag = True
        # Scan the dates from the file
        for day in class_days:
            # If it already exists, move to the next date from the file
            if today in day:
                flag = False
                break

        # If todays date is not found run the link poster
        if flag == True:
            print('Posting Zoom Link')
            options.add_argument('--headless')
            driver = webdriver.Firefox(firefox_options=options)

            # Navigate to calendar page
            # print("Opening Populi")
            driver.get("https://dfa.populiweb.com/calendar/index.php")
            sleep(1)

            # Enter username in google login form
            # print('Entering google user')
            elem = driver.find_element_by_id("identifierId")
            elem.send_keys(username)
            elem.send_keys(Keys.RETURN)
            sleep(3)

            # Enter password in google login form
            # print('Entering google password')
            elem = driver.find_element_by_name("password")
            elem.send_keys(password)
            elem.send_keys(Keys.RETURN)
            sleep(5)

            # Locate todays cell in the calender (Sort of...)
            # print('Locating today')
            elem = driver.find_element_by_class_name("eventText")
            # Click it to show the link
            elem.click()
            sleep(1)

            # Grab the zoom link from the popup window
            popup = driver.find_element_by_class_name("fb_popup")
            zoom_link = popup.find_element_by_partial_link_text('https://dfa.zoom.us')
            zoom_link =zoom_link.get_attribute('href')
            driver.close()
            driver.quit()

            # Add todays date to the known dates file
            print("Adding class date to file")
            f = open("Class_Dates.txt", "a")
            f.write(f'{today}\n')
            f.close()
            # Pass the homework description and link back to the Slack_Bot for posting
            return zoom_link

        


        
