from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

class Event:
    def __init__(self, eventId, seats):
        self.eventId = eventId
        self.seats = seats

events = []
## Don Giovani
events.append(Event(45514, ['L0__45514_70_3_2', 'L0__45514_70_3_3']))

## Figaro
events.append(Event(45442, ['L0__45442_38_2_1', 'L0__45442_38_2_2']))

## Fan Tutte
events.append(Event(45497, ['L0__45497_69_3_3', 'L0__45497_69_3_2']))

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
        driver.get(baseUrl + str(event.eventId))
        time.sleep(10)  # Time to load web page
        try:
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
                    log.write(seatId + ' is occupied\n')
                elif status != 'a':
                    # Seat in unknown state
                    log.write(seatId + ' is in unknown state: ' + status + '\n')
                elif status == 'a':
                    # Click seat
                    seat.click()

                    # Confirm low visibility pop up
                    #ok_btn = driver.find_elements_by_tag_name('button').pop()
                    #ok_btn.click()
                    log.write(seatId + ' has been reserved at: ' + datetime.now().__str__() + '\n')

            # Click on continue (with purchase)
            cont_btn = driver.find_element(By.CLASS_NAME, 'Lboto2')
            cont_btn.click()
            print('Reserved seats correctly')
            time.sleep(5)

        except Exception as e:
            log.write('Exception raised: ' + str(e) + '\n')

    log.close()
    driver.quit()
    time.sleep(20)

print('Exiting...')