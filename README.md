# patric-tests

Requirements:  

1. Python (tested on version 2.7.6)  
2. Selenium (tested on version 2.45.0)  
3. Firefox (tested on version 37.0.1)  
4. pyvirtualdisplay (tested on version 0.1.5)  

Installation instructions for Ubuntu 14.04:

    # You probably already have python and can skip the first step.
    sudo apt-get install python
    sudo pip install selenium
    sudo apt-get install firefox
    sudo pip install pyvirtualdisplay

To run login test:

    git clone https://github.com/jaredbischof/patric-tests.git
    cd patric-tests/
    ./scripts/login.py --firebug [username] [password]

To run workspace test:

    git clone https://github.com/jaredbischof/patric-tests.git
    cd patric-tests/
    ./scripts/test.py --firebug [username] [password]
