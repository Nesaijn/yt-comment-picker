#!/usr/bin/python3

from selenium import webdriver
#from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import random
import argparse
import re

parser = argparse.ArgumentParser(description="Pick a random winner from YouTube comments.")
parser.add_argument("url", help="A link to a YouTube video")

args = parser.parse_args()

url = args.url

# Check if the given URL is valid or not
regex = ("^((http|https)://)?(www.)?youtu(.be|be.de|be.com)/")
pattern = re.compile(regex)

valid = pattern.match(url)

if valid == None:
  print("Not a valid URL")
  quit()


options = Options()
options.add_argument("--headless")

#driver = webdriver.Chrome(executable_path=r"C:\path\to\chromedriver.exe", options=options)
driver = webdriver.Firefox(options=options)

# If a DOM element is asked for but is not present yet wait at least the given amount of seconds before throwing an error
driver.implicitly_wait(5)

driver.get(url)
#driver.find_element_by_xpath('//yt-formatted-string[text()="I Agree"]').click()


comments = {}
i = 0

print("Getting all the comments...")
while True:
  # Scroll down to load more comments
  driver.execute_script("window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight))")

  # Wait until more comments are loaded
  WebDriverWait(driver,30).until(EC.invisibility_of_element((By.CSS_SELECTOR,"div.active.style-scope.paper-spinner")))

  length = len(driver.find_elements_by_xpath("(//*[@id='content-text'])"))
  if length == 0:
    print("Couldn't find any comments")
    break
  elif i == length:
    break
  
  try:
    while i < length:
      author = driver.find_elements_by_xpath("//a[@id='author-text']/span")[i].text
      comment = driver.find_elements_by_xpath("(//*[@id='content-text'])")[i].text
      
      if author not in comments:
        comments[author] = []

      comments[author].append(comment)
      i += 1
  except Exception as err:
    print(err)
    driver.quit()
    quit()


again = ""

while again != "n":
  print()
  winner = random.choice(list(comments.keys()))
  
  print(f"The winner is: {winner}")
  print()
  print("Comments:")
  for comment in comments[winner]:
    print(comment)
    print()


  print()
  again = input("Do you want to run it again? (Y/n): ")
  

driver.quit()
quit()
