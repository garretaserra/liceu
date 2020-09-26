from _datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

url = 'https://liceubarcelona.koobin.com/index.php?action=PU_evento&Ev_id=40616'
chromeDriverPath = 'C:\Program Files\ChromeDriver\chromedriver.exe'
chromeOptions = Options()
chromeOptions.add_argument("--headless")
ids = ['L0__40616_69_3_3', 'L0__40616_69_3_2']

while 1:
    log = open('log.txt', 'a')
    log.write('Waking up: ' + datetime.now().__str__() + '\n')
    driver = webdriver.Chrome(chromeDriverPath, options=chromeOptions)
    driver.get(url)
    time.sleep(5)  # Time to load web page

    # Check connection
    try:
        for idSeat in ids:
            print(idSeat)
            text = driver.find_element_by_tag_name('h1')

            # Check seat availability
            seat = driver.find_element_by_id(idSeat)
            print(seat)
            status = seat.get_attribute('class')
            if status == 'o':
                # Seat is occupied
                log.write('Seat is occupied\n')
            elif status != 'a':
                # Seat in unknown state
                log.write('Seat is in unknown state: ' + status + '\n')
            elif status == 'a':
                # Click seat
                seat.click()

                # Confirm low visibility pop up
                ok_btn = driver.find_elements_by_tag_name('button').pop()
                ok_btn.click()

                # Click on continue (with purchase)
                cont_btn = driver.find_element_by_class_name('Lboto2')
                cont_btn.click()
                time.sleep(5)
                log.write('Seat has been reserved at: ' + datetime.now().__str__() + '\n')

    except Exception as e:
        log.write('Exception raised: ' + str(e) + '\n')

    finally:
        log.close()
        driver.quit()
        time.sleep(10)








