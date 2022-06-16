import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import date, datetime
import sqlite3


# NOTE sleep times are needed to wait for page elements to load before sending next command
class Populi_Bot():
    # Post new assignments
    def assignment_checker(username,password,options):
        driver = webdriver.Firefox(firefox_options=options)

        # Navigate to assignments page
        # print("Opening Populi")
        driver.get("line-to-populi-assignments-page")
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
        
        # Grab known assignments from database
        db = sqlite3.connect('class.db')
        command = db.cursor()
        db_assignments = command.execute("SELECT link FROM assignments; ").fetchall()
        # Save (commit) the changes
        db.commit()
        # Close the connection
        db.close()

        # For every assignment link on Populi
        for item in found_assignments:
            flag = True
            # See if it exists in the database
            for assignment in db_assignments:
                title = item[0]
                link = item[1]
                # If it already exists, move to the next link on Populi
                if link in assignment:
                    flag = False
                    break
            # If a Populi assignment link is not in the database
            if flag == True:
                print('Posting New Assignment')
                # Writing assignment to database
                db = sqlite3.connect('class.db')
                command = db.cursor()
                # Get today
                log_day = date.today().strftime("%m/%d/%y")
                # Get time
                now = datetime.now()
                log_time = now.strftime("%H:%M:%S")
                # Insert a row of data
                command.execute("INSERT INTO assignments VALUES (?,?,?,?)", (log_time, log_day, title, link))
                # Save (commit) the changes
                db.commit()
                # Close the connection
                db.close()
                # Pass the homework description and link back to the Slack_Bot for posting
                return title,link


    # Post link to class
    def todays_zoom_link(username,password,options):
        # Grab known assignments from database
        db = sqlite3.connect('class.db')
        command = db.cursor()
        class_days = command.execute("SELECT date FROM class_sessions; ").fetchall()
        # Save (commit) the changes
        db.commit()
        # Close the connection
        db.close()
        # Get today
        today = date.today().strftime("%m/%d/%y")
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
            driver.get("link-to-populi-calendar-page")
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

            # Grab zoom link from the popup window
            popup = driver.find_element_by_class_name("fb_popup")
            zoom_link = popup.find_element_by_partial_link_text('https://dfa.zoom.us')
            zoom_link =zoom_link.get_attribute('href')
            driver.close()
            driver.quit()
            
            # Writing class session data to database
            db = sqlite3.connect('class.db')
            command = db.cursor()
            # Get today
            today = date.today()
            entry_day = date.today().strftime("%m/%d/%y")
            # Get time
            now = datetime.now()
            entry_time = now.strftime("%H:%M:%S")
            # Insert a row of data
            command.execute("INSERT INTO class_sessions VALUES (?,?,?,?)", (entry_time, entry_day, 'title', 'zoom-session-link-here'))
            # Save (commit) the changes
            db.commit()
            # Close the connection
            db.close()

            # Pass the homework description and link back to the Slack_Bot for posting
            return zoom_link
