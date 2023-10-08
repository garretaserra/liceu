from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.common.exceptions import NoSuchElementException
import logging
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Reduce verbosity of chrome driver
LOGGER.setLevel(logging.ERROR)


class Seat:
    def __init__(self, seatId: str) -> None:
        self.seatId = seatId
        self.nextUpdate: datetime = datetime.now()
        self.historic: list[datetime] = []


class Event:
    def __init__(self, eventId: int, seats: list[Seat]):
        self.eventId = eventId
        self.seats = seats


events: list[Event] = []

events.append(
    Event(
        46314,
        [
            Seat("L0__46314_174_1_1"),
            Seat("L0__46314_174_1_2"),
            Seat("L0__46314_174_1_3"),
            Seat("L0__46314_174_1_4"),
            Seat("L0__46314_174_1_5"),
            Seat("L0__46314_174_1_6"),
        ],
    )
)

# Bones
events.append(
    Event(
        46314,
        [
            Seat("L0__46314_68_1_1"),
            Seat("L0__46314_68_1_2"),
            Seat("L0__46314_68_1_3"),
            Seat("L0__46314_68_3_1"),
            Seat("L0__46314_68_3_2"),
            Seat("L0__46314_68_2_1"),
            Seat("L0__46314_68_2_2"),
            Seat("L0__46314_70_3_1"),
            Seat("L0__46314_70_3_2"),
            Seat("L0__46314_70_3_3"),
            Seat("L0__46314_66_3_1"),
            Seat("L0__46314_66_3_2"),
            Seat("L0__46314_66_3_3"),
        ],
    )
)

# Check environment variables
chrome_location = os.getenv("CHROME_LOCATION")
chromeDriverPath = os.getenv("CHROME_DRIVER_LOCATION")
if chrome_location is None:
    print("CHROME_LOCATION environment variable is missing")
    exit(1)
if chromeDriverPath is None:
    print("CHROME_DRIVER_LOCATION environment variable is missing")
    exit(1)

chromeOptions = Options()
chromeOptions.add_argument("--headless")
chromeOptions.add_argument("--log-level=2")
chromeOptions.add_experimental_option("excludeSwitches", ["enable-logging"])
chromeOptions.binary_location = chrome_location


print("Starting...")

baseUrl = "https://liceubarcelona.koobin.com/index.php?action=PU_evento&Ev_id="

while 1:
    log = open("log.txt", "a")
    log.write("Waking up: " + str(datetime.now()) + "\n")
    chromeDriverService = Service(chromeDriverPath)
    driver = webdriver.Chrome(service=chromeDriverService, options=chromeOptions)
    for event in events:
        try:
            driver.get(baseUrl + str(event.eventId))
            time.sleep(10)  # Time to load web page
            cookies = driver.find_element(
                By.ID,
                "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowallSelectionWrapper",
            )
            cookies.click()
            time.sleep(2)

        except NoSuchElementException as e:
            pass

        except Exception as e:
            log.write("Exception raised: " + str(e) + "\n")
            print(e)

        # Check connection
        try:
            seats_reserved = []
            for seat in event.seats:
                # Check seat availability
                seatElement = driver.find_element(By.ID, seat.seatId)
                status = seatElement.get_attribute("class")
                if status == "o":
                    # Seat is occupied
                    log.write(str(seat.seatId) + " is occupied\n")
                elif status != "a":
                    # Seat in unknown state
                    log.write(str(seat.seatId) + " is in unknown state: " + status + "\n")
                elif status == "a":
                    # Click seat
                    seatElement.click()

                    # Confirm low visibility pop up
                    # ok_btn = driver.find_element(By.TAG_NAME, 'button')
                    # ok_btn.click()
                    log.write(
                        str(seat.seatId)
                        + "\t"
                        + " has been reserved at: "
                        + str(datetime.now())
                        + "\n"
                    )
                    seats_reserved.append(seat.seatId)

            if len(seats_reserved) > 0:
                # Click on continue (with purchase)
                cont_btn = driver.find_element(By.CLASS_NAME, "Lboto2")
                if cont_btn.is_displayed():
                    cont_btn.click()
                    print(
                        str(datetime.now()),
                        "Reserved seats:",
                        "\t".join(str(x) for x in seats_reserved),
                    )
                else:
                    print("ERROR: Couldn't find buy button")
                time.sleep(5)

        except Exception as e:
            log.write("Exception raised: " + str(e) + "\n")
            print(e)

    log.close()
    driver.quit()
    time.sleep(1)

print("Exiting...")
