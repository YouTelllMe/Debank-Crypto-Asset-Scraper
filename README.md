This program is a Python Selenium implemented crypto scraper. There are several changes that must be made
before this program can be ran on your local machine. Note that a virtual machine or an external computer/
server may be more suited for the purpose of this program since the data is scraped off of debank which
only renders when the selenium browser creates a window (it will open windows everytime you run it). This
program will scrape all data from each specified debank profile (in account.txt)

1. Config File

- The config file takes 3 paramters.
  - time.sleep is set to how often the program is ran in seconds(the default
    being everyday, or each 86370 seconds).
  - time.wait should not be changed and represents how much time the program
    waits before scraping the next crypto wallet (in case there are multiple)
  - time.preset is the delay of the program before it executes, which is ideal
    for adjusting the program to a schedule.

2. ChromeDriver

- This program will only run with google chrome.
- Currently, the chromedriver in this repository is a mac-64bit chrome version 97...
  driver. To use the program on your machine, please first check what chrome version you
  have in settings -> About Chrome of your chrome browser, then download the appropriate
  driver at "https://chromedriver.chromium.org/downloads".
- After downloading and extracting the driver, you must update the driver path in the
  program on line 116 of the file. Replace the existing driver path with your own. To be safe
  input the absolute path if possible.

3. Email Error Handling

- This is an optional function of the program. Once set up, the event handler will send
  an email to the specified receiver each time an error occurs to the program (ideal when
  you want to leave the program running). To set up this function, uncomment out the email
  function on line 96 and replace each content with [] around it with the instructed
  information (an email account and password is needed to send the email). The resulting
  message would likely result in the spam folder, make sure to allow emails from the sender
  email in the receiver email to prevent this.
- Make sure to also uncomment line 301 and lines 309-314 to implement the mechanism.
