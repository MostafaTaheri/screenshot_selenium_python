from screenshot import ScreenShot
from datetime import datetime


if __name__ == '__main__':

    screen = ScreenShot()

    full_screen_name = "{}.png".format(
        datetime.now().strftime('%Y-%m-%d%H-%M-%S'))

    by_xpath_name = "{}.png".format(
        datetime.now().strftime('%Y-%m-%d%H-%M-%S'))

    screen.full_screenshot(url='https://python.org',
                           image_name=full_screen_name)

    screen.screen_by_xpath(url='https://python.org/',
                           xpath='//*[@id="touchnav-wrapper"]/header',
                           image_name=by_xpath_name, save_path='.')
