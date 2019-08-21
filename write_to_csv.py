# Importing the modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import sys

# Loading the webdriver
driver = webdriver.Chrome()

# Loading the url
watch_id = sys.argv[1]
driver.get(f"https://youtube.com/watch?v={watch_id}")

# Wait for page load
time.sleep(2)

# Scroll to load comments
driver.execute_script("window.scrollTo(0,600)")
time.sleep(3)

# Calculating the number of scrolls required
num_comments = int(sys.argv[2])
n_scrolls = num_comments * 2 // 45

# Load all the comments by going to the bottom of the page for 10 iterations
for _ in range(n_scrolls):
    driver.execute_script("window.scrollTo(0,1e10);")
    time.sleep(3)

# Get all the comments
elements = driver.find_elements_by_tag_name("ytd-comment-thread-renderer")

# Save comments to a csv file
with open('comments.csv', 'w', encoding='utf-8', newline='') as csv_file:
    fieldnames = ['author', 'comment']
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    csv_writer.writeheader()
    for element in elements:
        author = element.find_element_by_id('author-text').text
        comment = element.find_element_by_id('content-text').text
        csv_writer.writerow({'author': author, 'comment': comment})

# Close the driver
driver.close()
