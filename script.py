from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import NoSuchElementException
import logging
import time

# Reduce verbosity of chrome driver
LOGGER.setLevel(logging.ERROR)

class Event:
    def __init__(self, eventId, seats):
        self.eventId = eventId
        self.seats = seats

events = []

#Parsifal
# Diumenge 28
events.append(Event(46314, ['L0__46314_68_3_1', 'L0__46314_68_3_2', 'L0__46314_68_3_3', 'L0__46314_68_2_1', 'L0__46314_68_2_2', 'L0__46314_70_3_1', 'L0__46314_70_3_2', 'L0__46314_70_3_3']))

#Manon
# Diumenge 23
events.append(Event(46309, ['L0__46309_68_3_1', 'L0__46309_68_3_2', 'L0__46309_68_3_1', 'L0__46309_68_2_1', 'L0__46309_68_2_2']))


chromeDriverPath = '.\chromedriver_win32\chromedriver.exe'
chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--log-level=2")
chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
chromeOptions.binary_location = '.\chrome-win\chrome.exe'

print('Starting...')

baseUrl = 'https://liceubarcelona.koobin.com/index.php?action=PU_evento&Ev_id='

while 1:
    log = open('log.txt', 'a')
    log.write('Waking up: ' + str(datetime.now())+ '\n')
    ser = Service(chromeDriverPath)
    driver = webdriver.Chrome(service=ser, options=chromeOptions)
    for event in events:
        try:
            driver.get(baseUrl + str(event.eventId))
            time.sleep(10)  # Time to load web page
        
            cookies = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelectionWrapper')
            cookies.click()
            time.sleep(2)

        except NoSuchElementException as e:
            pass
        
        except Exception as e:
            log.write('Exception raised: ' + str(e) + '\n')
            print(e)

        # Check connection
        try:
            seats_reserved = []
            for seatId in event.seats:
                # Check seat availability
                seat = driver.find_element(By.ID, seatId)
                status = seat.get_attribute('class')
                if status == 'o':
                    # Seat is occupied
                    log.write(str(seatId) + ' is occupied\n')
                elif status != 'a':
                    # Seat in unknown state
                    log.write(str(seatId) + ' is in unknown state: ' + status + '\n')
                elif status == 'a':
                    # Click seat
                    seat.click()

                    # Confirm low visibility pop up
                    #ok_btn = driver.find_elements_by_tag_name('button').pop()
                    #ok_btn.click()
                    log.write(str(seatId) + '\t' + ' has been reserved at: ' + str(datetime.now()) + '\n')
                    seats_reserved.append(seatId)

            if len(seats_reserved) > 0:
                # Click on continue (with purchase)
                cont_btn = driver.find_element(By.CLASS_NAME, 'Lboto2')
                if cont_btn.is_displayed():
                    cont_btn.click()
                    print(str(datetime.now()), 'Reserved seats:', '\t'.join(str(x) for x in seats_reserved))
                else:
                    print('ERROR: Couldn\'t find buy button')
                time.sleep(5)

        except Exception as e:
            log.write('Exception raised: ' + str(e) + '\n')
            print(e)

    log.close()
    driver.quit()
    time.sleep(1)

print('Exiting...')