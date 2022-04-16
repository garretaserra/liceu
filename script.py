from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
import logging
import time

# Reduce verbosity of chrome driver
LOGGER.setLevel(logging.ERROR)
class Event:
    def __init__(self, eventId, seats):
        self.eventId = eventId
        self.seats = seats

events = []

# Flauta Magica
events.append(Event(45455, ['L0__45455_67_3_1', 'L0__45455_67_3_2', 'L0__45455_67_3_3', 'L0__45455_238_1_3', 'L0__45455_238_1_2', 'L0__45455_238_1_1']))

chromeDriverPath = 'C:\Program Files\ChromeDriver\chromedriver.exe'
chromeOptions = Options()
chromeOptions.add_argument("--headless")

print('Starting...')

baseUrl = 'https://liceubarcelona.koobin.com/index.php?action=PU_evento&Ev_id='

while 1:
    log = open('log.txt', 'a')
    log.write('Waking up: ' + datetime.now().__str__() + '\n')
    ser = Service(chromeDriverPath)
    driver = webdriver.Chrome(service=ser, options=chromeOptions)
    for event in events:
        try:
            driver.get(baseUrl + str(event.eventId))
            time.sleep(10)  # Time to load web page
        
            cookies = driver.find_element(By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelectionWrapper')
            cookies.click()
            time.sleep(2)
        
        except Exception as e:
            pass

        # Check connection
        try:
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
                    log.write(str(event.eventId) + '\t' + str(seatId) + ' has been reserved at: ' + datetime.now().__str__() + '\n')

            # Click on continue (with purchase)
            cont_btn = driver.find_element(By.CLASS_NAME, 'Lboto2')
            if cont_btn.is_displayed():
                cont_btn.click()
                print('Reserved seats correctly')
            else:
                print('ERROR: Couldn\'t find buy button')
            time.sleep(5)

        except Exception as e:
            log.write('Exception raised: ' + str(e) + '\n')

    log.close()
    driver.quit()
    time.sleep(1)

print('Exiting...')