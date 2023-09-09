"""
Here is all the functional of selenium driver that will parse the site
"""
import time
import datetime

from selenium.common import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions

import database
from DataBaseDataClasses import DataDate
from logger import logger


class GovDriver(Chrome):
    def __init__(self):
        self.options = ChromeOptions()
        self.options.add_experimental_option('prefs', {
            'profile': {'profileName': 'Profile 1'}})
        self.options.add_argument('user-data-dir=C:/Users/uavla/AppData/Local/Google/Chrome/User Data')

        super().__init__(options=self.options, use_subprocess=True)

        self.get('https://online.mfa.gov.ua/application/')

        while True:
            try:
                self.find_element(By.ID, "countries")
                break
            except NoSuchElementException:
                pass

        try:
            popup_button = self.find_element(By.CSS_SELECTOR, "[class ='MuiButtonBase-root MuiButton-root "
                                                              "MuiButton-text MuiButton-textPrimary']")
            popup_button.click()

            logger().info("Closed info popup.")
        except NoSuchElementException:
            pass

        time.sleep(.5)

        self.__set_basic_inputs_value()

    def __set_basic_inputs_value(self):
        countries_input = self.find_element(By.ID, "countries")
        countries_input.send_keys('.Канада')
        # countries_input.send_keys('.Бразилія')

        self.submit_option()

        while True:
            try:
                self.find_element(By.CSS_SELECTOR,
                                  '.captcha-solver').click()

                break
            except Exception:
                pass

        while True:
            try:
                self.find_element(By.CSS_SELECTOR,
                                  "[class='MuiPaper-root MuiDialog-paper MuiDialog-paperScrollPaper "
                                  "MuiDialog-paperWidthSm MuiPaper-elevation24 MuiPaper-rounded']")

            except NoSuchElementException:
                logger().info("Captcha solved.")
                break

        countries_input = self.find_element(By.ID, "consulates")
        countries_input.send_keys('.ГКУ в Торонто')
        # countries_input.send_keys('.ПУ в Канаді')
        # countries_input.send_keys('.ПУ в Бразилії')

        self.submit_option()

        time.sleep(.5)

        countries_input = self.find_element(By.ID, "categories")
        countries_input.send_keys('.Паспортні дії')

        self.submit_option()

    def submit_option(self):
        try:
            option = self.find_element(By.CSS_SELECTOR, '[role=option]')
            option.click()
        except NoSuchElementException:
            logger().warning("Cannot submit option: element is not exists")

    def control_option(self, option_value: str):
        time.sleep(.15)

        services_input = self.find_element(By.ID, 'services')

        time_input = self.find_element(By.CSS_SELECTOR, '[placeholder=Час]')

        submit_button = self.find_element(By.CSS_SELECTOR, '[type=submit]')

        services_input.send_keys("." + option_value)
        self.submit_option()

        dates: list[datetime] = []
        try_n = 0
        while True:
            if try_n >= 50:
                break

            try_n += 1

            time.sleep(.15)

            self.update_option(option_value)

            date_input = self.find_element(By.CSS_SELECTOR, '[placeholder=Дата]')

            if not date_input.get_property('readonly') and not date_input.get_property('disabled'):
                date_input.click()

                try:
                    rdt_picker = self.find_element(By.CLASS_NAME, 'rdtPicker')
                    rdt_days = rdt_picker.find_elements(By.CSS_SELECTOR,
                                                        'td:not(.rdtDisabled):not(.rdtSel):not(.rdtOld):not(.rdtNew)')

                    rdt_day = rdt_days[0]

                    data_day = rdt_day.get_attribute('data-value')
                    data_month = rdt_day.get_attribute('data-month')
                    data_year = rdt_day.get_attribute('data-year')

                    _date = datetime.date(day=int(data_day),
                                          month=int(data_month),
                                          year=int(data_year))

                    logger().info(str(_date))

                    dates.append(_date)

                    rdt_day.click()

                    time.sleep(.1)

                    time_input.click()

                    dialog_content = self.find_element(By.CSS_SELECTOR, ".MuiDialogContent-root.jss92")

                    buttons = dialog_content.find_elements(By.CSS_SELECTOR, "button")

                    button = buttons[0]
                    from_time_text = button.find_element(By.CSS_SELECTOR,
                                                         'span.MuiButton-label').text.split('-')[0]

                    _time = datetime.time(hour=int(from_time_text.split(':')[0]),
                                          minute=int(from_time_text.split(':')[1]))

                    client = database.get_unreg_clients()[0]

                    button.click()

                    submit_button.click()

                    time.sleep(1.5)

                    surname_input = self.find_element(By.CSS_SELECTOR, '[name=lastName]')
                    name_input = self.find_element(By.CSS_SELECTOR, '[name=firstName]')
                    thirdname_input = self.find_element(By.CSS_SELECTOR, '[name=middleName]')
                    phone_input = self.find_element(By.CSS_SELECTOR, '[name=phoneNumber]')
                    email_input = self.find_element(By.CSS_SELECTOR, '[name=email]')
                    email2_input = self.find_element(By.CSS_SELECTOR, '[name=re_email]')
                    submit_input = self.find_element(By.CSS_SELECTOR, '[type=submit]')

                    name_input.send_keys(client.name)
                    surname_input.send_keys(client.surname)
                    thirdname_input.send_keys(client.thirdname)
                    phone_input.send_keys(client.phone)
                    email_input.send_keys(client.email)
                    email2_input.send_keys(client.email)

                    while True:
                        try:
                            submit_input.click()
                            break
                        except ElementClickInterceptedException:
                            ...

                    self.get_screenshot_as_file(
                        f'./screens/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}'
                        f'({datetime.datetime.combine(_date, _time).strftime("%Y-%m-%d_%H-%M")}).png')

                    database.write_date(DataDate(bdid=-1,
                                                 datetime=datetime.datetime.combine(_date, _time),
                                                 client_id=client.bdid))

                    client.registered = True
                    database.update_client(client)

                    while True: ...
                except NoSuchElementException:
                    logger().error("Cannot get .rdtPicker (calendar).")

    def update_option(self, option_value: str):
        __option_value_to_switch: str = "Постійний КО"
        # __option_value_to_switch: str = "Посвідчення на повернення в Україну"

        services_input = self.find_element(By.ID, 'services')

        services_input.click()
        services_input.send_keys('\b' * (len(option_value) + 15))

        time.sleep(.15)

        services_input.send_keys(f'{__option_value_to_switch}')
        self.submit_option()

        time.sleep(.15)

        services_input.click()
        services_input.send_keys('\b' * (len(__option_value_to_switch) + 15))

        time.sleep(.15)

        services_input.send_keys(f'{option_value}')
        self.submit_option()
