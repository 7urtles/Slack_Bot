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
        print("Opening Populi")
        driver.get("https://dfa.populiweb.com/router/courseofferings/10734937/assignments/index")
        sleep(1)

        # Enter username in google login form
        print('Entering google user')
        elem = driver.find_element_by_id("identifierId")
        elem.send_keys(username)
        elem.send_keys(Keys.RETURN)
        sleep(2)

        # Enter password in google login form
        print('Entering google password')
        elem = driver.find_element_by_name("password")
        elem.send_keys(password)
        elem.send_keys(Keys.RETURN)
        sleep(5)

        # Grab all the <a></a> tags with a class name of 'remote_name' (assingment links have this class name)
        print('Finding Assignments')
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


        f = open("Assignment_List.txt", "r")
        assignments = f.readlines()
        f.close()

        
        # Check assignment file for already existing homework link
        for item in found_assignments:
            flag = True
            for assignment in assignments:
                title = item[0]
                link = item[1]
                # print(link, '\n', assignment)
                if link in assignment:
                    # print('Assignment already exists.')
                    flag = False
                    break
            if flag == True:
                # Add the new assignment to the assignments file
                print("Adding new assignment to file")
                f = open("Assignment_List.txt", "a")
                f.write(f'{title} {link}\n')
                f.close()

                # Pass the homework description and link back to the slack bot for posting
                return title,link
