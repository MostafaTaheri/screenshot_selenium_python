import yaml
import os

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from time import sleep
from lazy_load import lazy_func
from typing import Any, Optional
from PIL import Image


class ScreenShot:
    def __init__(self):
        self.config = self._load_config()
        self.driver = self._load_driver(self.config)

    @lazy_func
    def _load_config(self) -> Any:
        """Loads the all information from config file."""
        return yaml.load(open("config.yml"), Loader=yaml.FullLoader)

    @lazy_func
    def _load_driver(self, config_file: yaml) -> webdriver:
        """Loads the Selenium driver depending on the browser.

        Edge and Safari are not running yet.

        Arg:
            config_file: That is a yaml file.

        Returns:
            An object of webdriver.
        """
        driver = None
        if config_file['driver']['name'].lower() == 'firefox':
            firefox_profile = webdriver.FirefoxProfile(
                config_file['driver']['location'])
            driver = webdriver.Firefox(firefox_profile)
        elif config_file['driver']['name'].lower() == 'edge':
            pass
        elif config_file['driver']['name'].lower() == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument(
                "user-data-dir=" + config_file['driver']['location'])
            chrome_options.add_argument("--start-maximized")
            driver = webdriver.Chrome(
                executable_path=config_file['driver']['location'])
        elif config_file['driver']['name'].lower() == 'safari':
            pass

        return driver

    def screen_by_xpath(self, url: str, xpath: str, save_path: Optional[str] = '.', image_name: Optional[str] = 'screenshot.png') -> str:
        """ Saves a screenshot of the current window to a PNG image file.

        Args:
            url: The URL of the current page.
            xpath: The choosen part for obtain screen.
            save_path: The path where to store screenshot.
            image_name: The name of screenshot image.

        Returns:
            The path of image

        Usages:
            driver.screen_by_xpath(url='https://python.org', xpath='//div/td[1]')
        """
        try:
            self.driver.maximize_window()
            self.driver.get(url)
            sleep(2)
            image_name = os.path.abspath(save_path + '/' + image_name)
            
            self.driver.find_element_by_xpath(xpath).screenshot(image_name)
            self.driver.quit()
        except IOError:
            return None
        return image_name

    def full_screenshot(self, url: str, save_path: Optional[str] = '.', image_name: Optional[str] = 'selenium_full_screenshot.png',
                        elements: list = None, is_load_at_runtime: bool = False, load_wait_time: int = 5) -> str:
        """
        Take full screenshot of web page.

        Args:
            url: The page that should be observed.
            save_path: The path where to store screenshot.
            image_name: The name of screenshot image.
            elements: List of Xpath of elements to hide from web pages.
            is_load_at_runtime: Page Load at runtime.
            load_wait_time: The Wait time while loading full screen.

        Returns:
            The path of image
        """
        image_name = os.path.abspath(save_path + '/' + image_name)

        final_page_height = 0
        original_size = self.driver.get_window_size()

        self.driver.maximize_window()
        self.driver.get(url)

        if is_load_at_runtime:
            while True:
                page_height = self.driver.execute_script(
                    "return document.body.scrollHeight")
                if page_height != final_page_height and final_page_height <= 10000:
                    self.driver.execute_script(
                        "window.scrollTo(0, {})".format(page_height))
                    sleep(load_wait_time)
                    final_page_height = page_height
                else:
                    break

        if isinstance(self.driver, webdriver.Ie):
            self.hide_elements(self.driver, elements)
            required_width = self.driver.execute_script(
                'return document.body.parentNode.scrollWidth')
            self.driver.set_window_size(required_width, final_page_height)
            self.driver.save_screenshot(image_name)
            self.driver.set_window_size(
                original_size['width'], original_size['height'])
            return image_name

        else:
            total_width = self.driver.execute_script(
                "return document.body.offsetWidth")
            total_height = self.driver.execute_script(
                "return document.body.parentNode.scrollHeight")
            viewport_width = self.driver.execute_script(
                "return document.body.clientWidth")
            viewport_height = self.driver.execute_script(
                "return window.innerHeight")
            self.driver.execute_script("window.scrollTo(0, 0)")
            sleep(2)
            rectangles = []

            self.hide_elements(self.driver, elements)
            i = 0
            while i < total_height:
                ii = 0
                top_height = i + viewport_height
                if top_height > total_height:
                    top_height = total_height
                while ii < total_width:
                    top_width = ii + viewport_width
                    if top_width > total_width:
                        top_width = total_width
                    rectangles.append((ii, i, top_width, top_height))
                    ii = ii + viewport_width
                i = i + viewport_height
            stitched_image = Image.new('RGB', (total_width, total_height))
            previous = None
            part = 0

            for rectangle in rectangles:
                if not previous is None:
                    self.driver.execute_script(
                        "window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                    sleep(3)
                file_name = "part_{0}.png".format(part)
                self.driver.get_screenshot_as_file(file_name)
                screenshot = Image.open(file_name)
                if rectangle[1] + viewport_height > total_height:
                    offset = (rectangle[0], total_height - viewport_height)
                else:
                    offset = (rectangle[0], rectangle[1])
                stitched_image.paste(screenshot, offset)
                del screenshot
                os.remove(file_name)
                part = part + 1
                previous = rectangle
            save_path = os.path.abspath(os.path.join(save_path, image_name))
            stitched_image.save(save_path)
            return save_path

    @staticmethod
    def hide_elements(driver: WebDriver, elements: list) -> None:
        """
         Usage:
             Hide elements from web page
         Args:
             driver : The path of chromedriver
             elements : The element on web page to be hide
         Returns:
             N/A
         Raises:
             N/A
         """
        if elements is not None:
            try:
                for e in elements:
                    sp_xpath = e.split('=')
                    if 'id=' in e.lower():
                        driver.execute_script(
                            "document.getElementById('{}').setAttribute('style', 'display:none;');".format(
                                sp_xpath[1]))
                    elif 'class=' in e.lower():
                        driver.execute_script(
                            "document.getElementsByClassName('{}')[0].setAttribute('style', 'display:none;');".format(
                                sp_xpath[1]))
                    else:
                        print(
                            'For Hiding Element works with ID and Class Selector only')
            except Exception as Error:
                print('Error : ', str(Error))
