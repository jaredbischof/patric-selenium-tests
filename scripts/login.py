#!/usr/bin/env python

import argparse
import os
import string
import sys
import timeit

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

VERSION = '0.5'
SITE_URL = 'https://www.patricbrc.org'
PAGE_LOAD_TIMEOUT = 120  # seconds
FIREFOX_PATH = os.environ.get('FIREFOX_PATH', '/usr/bin/firefox')
FIREBUG_XPI = os.environ.get('FIREBUG_XPI', 'extras/firebug-2.0.9.xpi')

def main(args):
    parser = argparse.ArgumentParser(description="Test to login to PATRIC web interface.")
    parser.add_argument("user", metavar="user", help="Patric login username.")
    parser.add_argument("passwd", metavar="passwd", help="Patric login password.")
    parser.add_argument("--firebug", action="store_true", help="Open Firebug during test.")
    parser.add_argument("--verbose", action="store_true", help="Print informational messages.")
    parser.add_argument("--screenshots", action="store_true", help="Take screenshots during test execution.")
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
    if args.verbose:
        print "Created virtual display"

    # Create webdriver and retrieve url
    driver = webdriver.Firefox(firefox_profile=fp, firefox_binary=FirefoxBinary(FIREFOX_PATH))
    url = "https://www.patricbrc.org/portal/portal/patric/Home"
    start = timeit.default_timer()
    driver.get(url)
    if args.verbose:
        print "Retrieved login url: " + url

    # Wait for dashboardnav div to a2ddppear
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.presence_of_element_located((By.ID, "dashboardnav")))
    stop = timeit.default_timer()
    patric_login_load = int((stop - start) * 1000 + 0.5)

    # Execute js function to open login iframe
    driver.execute_script("doLogin();")

    # Wait for login iframe to appear
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))

    # Wait for username field to appear
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.presence_of_element_located((By.ID, "dijit_form_TextBox_0")))

    # Set username and password, click login button
    userElement = driver.find_element_by_id("dijit_form_TextBox_0")
    pwdElement = driver.find_element_by_id("dijit_form_TextBox_1")
    userElement.send_keys(args.user)
    pwdElement.send_keys(args.passwd)
    loginElement = driver.find_element_by_id("dijit_form_Button_1")
    start = timeit.default_timer()
    loginElement.click()

    # Wait for dashboardnav div to a2ddppear
    WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(EC.presence_of_element_located((By.ID, "dashboardnav")))
    stop = timeit.default_timer()
    patric_login_run = int((stop - start) * 1000 + 0.5)
    dashboardnav = driver.find_element_by_id("dashboardnav")
    dashboardhtml = dashboardnav.get_attribute('innerHTML')

    if string.find(dashboardhtml, 'Welcome'):
        if args.screenshots:
            driver.set_window_size(1400, 950)
            driver.execute_script("window.scrollTo(0,0);")
            jpg = "homepage_after_login.jpg"
            driver.get_screenshot_as_file(jpg)
            print "Saved screenshot to: " + jpg
        sys.stdout.write("patric_login_load\t%d\n" % patric_login_load)
        sys.stdout.write("patric_login_run\t%d\n" % patric_login_run)
    else:
        sys.stderr.write("[error]: unsuccessful login\n")
        return 1

    driver.quit()
    display.stop()
    return 0

if __name__ == "__main__":
    sys.exit( main(sys.argv) )
