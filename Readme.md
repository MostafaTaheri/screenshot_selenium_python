# Take A Screenshot Using Python & Selenium

In this Python Selenium screenshot tutorial, we are going to explore different ways of taking screenshots using Selenium’s Python bindings. 

we need a driver to proceed with clicking Python Selenium screenshots of webpages.

You can choose any browser of your choice, and you can download the drivers from the following links :

[Chrome](https://sites.google.com/a/chromium.org/chromedriver/)

[Firefox](https://github.com/mozilla/geckodriver/releases)

[Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

[Internet Explorer](https://selenium-release.storage.googleapis.com/index.html)

</br>

#
## Code Walkthrough
Let’s understand what we are doing here.

<span style="color: red"> from selenium import webdriver</span> >> This line imports the WebDriver which we use to fire-up a browser instance and use APIs to interact with web elements.

<span style="color: red"> from time import sleep </span> >> his line imports the sleep function from Python’s ‘time’ module. This accepts integer arguments which equals the number of seconds. The script waits for the specified number of seconds before executing the next line of code.

<span style="color: red"> browser = webdriver.chrome(executable_path) </span> This line is equivalent to saying, use the keyword ‘browser’ as you would use ‘webdriver.chrome(executable_path)’.

browser.get(“https://www.python.org/”)

<span style="color: red">browser.quit() </span> >> Lastly, the browser needs to be closed and this line does the same.

</br>

## Requirements
selenium

PyYAML

lazy-load

</br>

## Capturing Python Selenium Screenshots Of A Particular Element
We now demonstrate how we can use the screen_by_xpath() method to capture any element on the page.

</br>

```python
from screenshot import ScreenShot
from datetime import datetime


if __name__ == '__main__':

    screen = ScreenShot()

    image_name = "{}.png".format(
        datetime.now().strftime('%Y-%m-%d%H-%M-%S'))

    screen.screen_by_xpath(url='https://python.org/',
                           xpath='//*[@id="touchnav-wrapper"]/header',
                           image_name=image_name, save_path='.')

```

<br/>


## Capturing full page screenshots
We can use the full_screenshot() method to capture ful page screenshots.

</br>

```python
from screenshot import ScreenShot
from datetime import datetime


if __name__ == '__main__':

    screen = ScreenShot()  

    image_name = "{}.png".format(
        datetime.now().strftime('%Y-%m-%d%H-%M-%S'))

    screen.full_screenshot(url='https://python.org',
                           image_name=image_name)

```