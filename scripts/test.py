#!/usr/bin/env python

import sys
import time
import argparse

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

VERSION = '0.5'
SITE_URL = 'https://www.patricbrc.org'
PAGE_LOAD_TIMEOUT = 120  # seconds

def main(args):
    parser = argparse.ArgumentParser(description="Program for running tests on the PATRIC web interface.")
    parser.add_argument("user", metavar="user", help="Patric login username.")
    parser.add_argument("passwd", metavar="passwd", help="Patric login password.")
    parser.add_argument("--firebug", action="store_true", help="Open Firebug during test.")
    args = parser.parse_args()

    fp = webdriver.FirefoxProfile()
    if args.firebug:
        fp.add_extension(extension='extras/firebug-2.0.9.xpi')
        fp.set_preference("extensions.firebug.currentVersion", "2.0.9") #Avoid startup screen
        fp.set_preference("extensions.firebug.console.enableSites", "true")
        fp.set_preference("extensions.firebug.net.enableSites", "true")
        fp.set_preference("extensions.firebug.script.enableSites", "true")
        fp.set_preference("extensions.firebug.allPagesActivation", "on")

    # Create virtual display
    display = Display(visible=0, size=(1400, 950))
    display.start()

    # Create webdriver and retrieve url
    driver = webdriver.Firefox(firefox_profile=fp)
    driver.get(SITE_URL + '/login')

    # Wait for username input box to appear
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.presence_of_element_located((By.ID, "dijit_form_TextBox_0")))

    # Set username and password, click login button
    userElement = driver.find_element_by_id("dijit_form_TextBox_0")
    pwdElement = driver.find_element_by_id("dijit_form_TextBox_1")
    userElement.send_keys(args.user)
    pwdElement.send_keys(args.passwd)
    loginElement = driver.find_element_by_id("dijit_form_Button_1")
    loginElement.click()
    time.sleep(3)

    # Retrieve home page, wait for an expected page element to load, take a screenshot
    driver.get(SITE_URL + '/portal/portal/patric/Home')
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.presence_of_element_located((By.ID, "cart")))
    driver.set_window_size(1400, 950)
    driver.execute_script("window.scrollTo(0,0);")
    driver.get_screenshot_as_file("homepage_after_login.jpg")
    print "Saved screenshot to: homepage_after_login.jpg\n"

    # Retrieve ws url, wait for create folder button to appear
    ws_url = SITE_URL + '/workspace/' + args.user + '@patricbrc.org/home'
    driver.get(ws_url)
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "ActionButtonContainer")))
    time.sleep(5)

    # Have to reload page, because often time the workspace is empty on first load
    driver.get(ws_url)
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.presence_of_element_located((By.CLASS_NAME, "ActionButtonContainer")))
#    createFolderButton = driver.find_element_by_class_name("ActionButton fa icon-folder-plus fa-2x")
#    createFolderButton.click()
    time.sleep(30)

    driver.quit()
    display.stop()
    return 0

if __name__ == "__main__":
    sys.exit( main(sys.argv) )
