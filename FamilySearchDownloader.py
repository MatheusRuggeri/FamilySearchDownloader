from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time 
import csv
import os

# chromeLoad loads the navegator, it is required for any other function
# loadImages keep pressing the right arrow without downloading the image
# exportList exports all the images URL as a CSV file to download latter
# downImages downloads all the images in CSV file URL.
chromeLoad = True
loadImages = True
exportList = False
downImages = False

# Chrome default download path, and the directory that I want to move my files
DEFAULT_PATH = 'C:/Users/matheus/Downloads'
COPY_TO_PATH = 'C:/Users/matheus/Downloads/Family'

# Put here the first page in the book that you want to download
BOOK_FIRST_PAGE = 'https://www.familysearch.org/ark:/61903/3:1:3Q9M-CS8W-V946-8?cat=2656262'

if (chromeLoad):
    # Uses webdriver_manager to create a chrome session
    browser = webdriver.Chrome(ChromeDriverManager().install())
    
    # The Family Search film first page adress 
    browser.get(BOOK_FIRST_PAGE)
    
    # To maximize the browser window 
    browser.maximize_window() 
    
    # Family Search will open login page, those are the fields ID
    username = browser.find_element_by_id("userName")
    password = browser.find_element_by_id("password")
    
    # Put my user and pass in the elements
    username.send_keys("YOUR_USER_NAME")
    password.send_keys("YOUR_USER_PASSWORD")
    
    # Click to login
    browser.find_element_by_id("login").click()

# This block just keep pressing the button with the Right Arrow without downloading, just load the image
if (loadImages):
    browser.get(BOOK_FIRST_PAGE)
    
    # Waits until page loads the image viewer
    time.sleep(3)
    
    # The lastImage will check if we reach the last page
    lastImage = ''
    while (True):
        # It will sleep for 1 second and click next, sleep 1 second and check the image
        # To my internet (200 mbps) it was ok, if your is slower, just increase the time
        time.sleep(1)
        browser.find_element_by_class_name('next').click()   
        time.sleep(1)
        image = browser.find_element_by_class_name('actionToolbarSaveButton').get_attribute("href");
        
        # If this image is equals the last one, this means that we reach the last page
        if (lastImage == image):
            break
        
        # Exports the image list to a CSV file
        with open('MyBook.csv', 'a+', newline='') as exportlist:
            writer = csv.writer(exportlist, delimiter=',')
            writer.writerow([image])
            
        # Update the last image URL
        lastImage = image

# This block exports a CSV file with all the images URL
# It is almost like the loadImages, but this didn't wait until the image is loaded
# This block is much faster, but it can be identified as a robot and block your user for 1 hour
if (exportList):  
    # Waits until page loads the image viewer
    time.sleep(3)
    
    # The lastImage will check if we reach the last page
    lastImage = ''
    
    # Save all the images as a CSV file (sometimes Family Search don't load, so this loop only saves the URL)
    while (True):
        # Get the href from SaveButton, this is the image path to download
        image = browser.find_element_by_class_name('actionToolbarSaveButton').get_attribute("href");
        #browser.get(image)
        print(image)
        
        #time.sleep(1)
        browser.find_element_by_class_name('next').click()
        
        # If this image is equals the last one, this means that we reach the last page
        if (lastImage == image):
            break
        
        # Exports the image list to a CSV file
        with open('MyBook.csv', 'a+', newline='') as exportlist:
            writer = csv.writer(exportlist, delimiter=',')
            writer.writerow([image])
            
        # Update the last image URL
        lastImage = image

# This block takes a CSV file and download all the images from your family book
# Since all the images are saved as record-image_.jpg, this code changes the path and rename to 1, 2, 3...
# IMPORTANT: It is very common to Family Search to be offline for some minutes, so this code will be waiting,
#            you should wait some minutes and update the page, if it downloads a file, the code will detect and run again.
if (downImages):
    # Start the download in a new tab
    time.sleep(3)
    print('Starting the downloads...')
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't') 
    
    # Open the CSV file and set the image number to One
    downList = open('Book.csv')
    imgNumber = 1

    # Iterate the download list
    for imageLink in downList:
        # Creates 2 paths, the original file download name and the new file name
        copyFrom = DEFAULT_PATH + '/record-image_.jpg'
        copyTo = COPY_TO_PATH + "/" + str(imgNumber) + '.jpg'
        
        # If the file already exists, just skip this one
        # Since sometimes the Family Search page identify this code as a robot, you can close and open again and this loop will ignore the downloaded images
        if(not os.path.isfile(copyTo)):
            browser.get(imageLink)
            time.sleep(2)
            
            # While there the file is not downloaded, keep waiting, if your connection is too slow or the page is offline this will prevent any error
            while (not os.path.isfile(copyFrom)):
                time.sleep(1)
            
            # This moves and rename the file
            os.rename(copyFrom, copyTo)
            print("Downloaded " + str(imgNumber) + ".jpg")
        else:
            print("File " + str(imgNumber) + ".jpg already exists")
            
        # Increase the image number
        imgNumber += 1
        
# When it's all done, close the browser
#browser.close() 
    