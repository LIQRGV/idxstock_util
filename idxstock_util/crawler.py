import requests
from bs4 import BeautifulSoup
from io import StringIO
import csv

from time import (
  mktime,
  strptime
)

def get_all_downloadable_link():
  response = requests.get("http://dataharianbei.com")
  soup = BeautifulSoup(response.text, 'html.parser')

  all_downloadable = filter(
    lambda a: a.attrs['href'].find('download.php') != -1, 
    soup.find_all('a')
  )

  all_link = map(lambda a: a.attrs['href'], all_downloadable)

  return tuple(all_link)

def get_last_downloadable_link():
  all_downloadable = get_all_downloadable_link()
  last_downloadable = [all_downloadable[len(all_downloadable) - 1]]

  return tuple(last_downloadable)

def process_link_to_csv(raw_data):
  result = []
  reader = csv.reader(StringIO(raw_data))
  header = ['date', 'ticker', 'open', 'high', 'low', 'close', 'volume']
  result.append(header)
  reader.__next__()
  for row in reader:
    date_string = row[0]
    row[0] = mktime(strptime(date_string, '%m/%d/%y'))
    result.append(row)
  return result