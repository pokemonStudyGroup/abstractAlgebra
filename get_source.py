import requests

from selenium import webdriver
from time import sleep

"""
This script uses phantomJS to navigate to the sharelatex project just to
populate it's cookies, so that requests can download the source.
"""

read_only_link = 'https://www.sharelatex.com/read/wmrdfswtqpxw'
source_link =\
  'https://www.sharelatex.com/project/5b32f53b79d56f2f44fed382/download/zip'

while True:
  try:
    driver = webdriver.PhantomJS()
    driver.get(read_only_link)
    break
  except:
    # Failed to connect (this happened a few times while testing)
    # ignoring it seems to work
    sleep(1)

sleep(5) # sleeping 5s incase there's server-side stuff loading

session = requests.Session()
cookies = driver.get_cookies()
for cookie in cookies: 
  session.cookies.set(cookie['name'], cookie['value'])
response = session.get(source_link)

if not response.ok:
  open('logfile', 'a').write("Failed to download source, not retrying")
  exit(1)

open('/tmp/source.zip', 'wb').write(response.content)
