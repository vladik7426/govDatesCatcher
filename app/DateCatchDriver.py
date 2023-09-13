"""
Here is all the functional of selenium driver that will parse the site
"""
import os
import time
import datetime
from os import path

from selenium.common import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from undetected_chromedriver import Chrome, ChromeOptions

import gdc_gmail
from app.logger import MyLogger
from gdc_database import db_clients, db_dates
from gdc_database.db_clients import DataClient
from gdc_database.db_dates import DataDate


class DateCatchDriver(Chrome):
    def __init__(self):
        options = ChromeOptions()
        options.add_experimental_option('prefs', {
            'profile': {'profileName': 'Profile 1'}})
        options.add_argument('--disable-application-cache')
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('user-data-dir=C:/Users/uavla/AppData/Local/Google/Chrome/User Data')

        super().__init__(options=options, use_subprocess=True)

    def set_basic_inputs_values(self, consulate: str):
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

            MyLogger.logger().info("Closed info popup.")
        except NoSuchElementException:
            pass

        countries_input = self.find_element(By.ID, "countries")
        self.__send_keys(countries_input, '.Канада')
        # self.__send_keys(countries_input, '.Бразилія')

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
                MyLogger.logger().info("Captcha solved.")
                break

        countries_input = self.find_element(By.ID, "consulates")
        self.__send_keys(countries_input, '.' + consulate)

        self.submit_option()

        countries_input = self.find_element(By.ID, "categories")
        self.__send_keys(countries_input, '.Паспортні дії')

        self.submit_option()

    @staticmethod
    def __send_keys(element, keys: str):
        while True:
            try:
                element.send_keys(keys)
                break
            except ElementNotInteractableException:
                pass

    def catch_date_for_client(self, client: DataClient) -> bool:
        time.sleep(.15)

        services_input = self.find_element(By.ID, 'services')
        time_input = self.find_element(By.CSS_SELECTOR, '[placeholder=Час]')

        self.__send_keys(services_input, "." + client.category)
        self.submit_option()

        try_n = 0

        while True:
            min_str = datetime.datetime.now().strftime('%M:%S')
            if min_str == '29:56' or min_str == '59:56':
                break

        while True:
            if try_n >= 50:
                break

            try_n += 1

            time.sleep(.15)

            self.update_category(client.category)

            date_input = self.find_element(By.CSS_SELECTOR, '[placeholder=Дата]')

            if not date_input.get_property('readonly') and not date_input.get_property('disabled'):
                date_input.click()

                try:
                    rdt_picker = self.find_element(By.CLASS_NAME, 'rdtPicker')

                    rdt_day = rdt_picker.find_element(By.CSS_SELECTOR,
                                                      'td:not(.rdtDisabled):not(.rdtSel):not(.rdtOld):not(.rdtNew)')

                    data_day = rdt_day.get_attribute('data-value')
                    data_month = rdt_day.get_attribute('data-month')
                    data_year = rdt_day.get_attribute('data-year')

                    _date = datetime.date(day=int(data_day),
                                          month=int(data_month),
                                          year=int(data_year))

                    rdt_day.click()

                    time.sleep(.1)

                    time_input.click()

                    dialog_content = self.find_element(By.CSS_SELECTOR, ".MuiDialogContent-root.jss92")
                    time_button = dialog_content.find_element(By.CSS_SELECTOR, "button")

                    from_time_text = time_button.find_element(By.CSS_SELECTOR,
                                                              'span.MuiButton-label').text.split('-')[0]

                    _time = datetime.time(hour=int(from_time_text.split(':')[0]),
                                          minute=int(from_time_text.split(':')[1]))

                    time_button.click()

                    self.find_element(By.CSS_SELECTOR, '[type=submit]').click()

                    time.sleep(.3)

                    surname_input = self.find_element(By.CSS_SELECTOR, '[name=lastName]')
                    name_input = self.find_element(By.CSS_SELECTOR, '[name=firstName]')
                    thirdname_input = self.find_element(By.CSS_SELECTOR, '[name=middleName]')
                    phone_input = self.find_element(By.CSS_SELECTOR, '[name=phoneNumber]')
                    email_input = self.find_element(By.CSS_SELECTOR, '[name=email]')
                    email2_input = self.find_element(By.CSS_SELECTOR, '[name=re_email]')

                    name_input.send_keys(client.name)
                    surname_input.send_keys(client.surname)
                    thirdname_input.send_keys(client.thirdname)
                    phone_input.send_keys(client.phone)
                    email_input.send_keys(client.email)
                    email2_input.send_keys(client.email)

                    while True:
                        try:
                            self.find_element(By.CSS_SELECTOR, '[type=submit]').click()
                            break
                        except ElementClickInterceptedException:
                            ...

                    if not path.exists('screens'):
                        os.mkdir('screens')

                    dir_name = f'screens/{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")}'
                    os.mkdir(dir_name)

                    self.get_screenshot_as_file(f'{dir_name}/'
                                                f'{datetime.datetime.combine(_date, _time).strftime("%Y-%m-%d_%H-%M")}'
                                                f'.png')

                    db_dates.write_date(DataDate(bdid=-1,
                                                 datetime=datetime.datetime.combine(_date, _time),
                                                 client_id=client.bdid))

                    client.registered = True
                    db_clients.update_client(client)

                    while True:
                        try:
                            self.find_element(By.CSS_SELECTOR, '[type=submit]').click()
                            break
                        except ElementClickInterceptedException:
                            ...

                    while True:
                        try:
                            self.find_elements(By.CSS_SELECTOR, '[type=button][class="MuiButtonBase-root '
                                                                'MuiButton-root MuiButton-text '
                                                                'MuiButton-textPrimary"]')[1].click()
                            break
                        except Exception:
                            pass

                    self.get_screenshot_as_file(
                        f'{dir_name}/'
                        f'{datetime.datetime.combine(_date, _time).strftime("%Y-%m-%d_%H-%M")}-2.png')

                    while True:
                        try:
                            book_number = int(self.find_element(By.CSS_SELECTOR, '.jss143 h5').text.split(': ')[1])
                            book_submit_url = gdc_gmail.get_book_submit_url_by_number(book_number)

                            if book_submit_url is None:
                                raise ValueError("URL is None")

                            while True:
                                try:
                                    self.get(book_submit_url)
                                    self.find_element(By.CSS_SELECTOR, 'button').click()
                                    break
                                except Exception as ex:
                                    print("Submit form from gmail error:", ex)

                            break
                        except IndexError:
                            pass

                        except ValueError:
                            pass

                    time.sleep(5)

                    self.get_screenshot_as_file(
                        f'{dir_name}/'
                        f'{datetime.datetime.combine(_date, _time).strftime("%Y-%m-%d_%H-%M")}-submitted.png')

                    return True
                except NoSuchElementException:
                    MyLogger.logger().error("Cannot get .rdtPicker (calendar).")
                    return False

                finally:
                    return False

        return False

    def submit_option(self):
        try:
            option = self.find_element(By.CSS_SELECTOR, '[role=option]')
            option.click()
        except NoSuchElementException:
            MyLogger.logger().warning("Cannot submit option: element is not exists")

    def update_category(self, category: str):
        __option_value_to_switch: str = "Постійний КО"

        services_input = self.find_element(By.ID, 'services')

        services_input.click()
        self.__send_keys(services_input, '\b' * (len(category) + 15))

        time.sleep(.15)

        self.__send_keys(services_input, f'{__option_value_to_switch}')
        self.submit_option()

        time.sleep(.15)

        services_input.click()
        self.__send_keys(services_input, '\b' * (len(__option_value_to_switch) + 15))

        time.sleep(.15)

        self.__send_keys(services_input, f'{category}')
        self.submit_option()
