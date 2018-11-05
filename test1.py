import requests

from datetime import datetime

from pandas import DataFrame

from idxstock_util import (
  crawler,
  util
)

all_link = crawler.get_all_downloadable_link()

dataframes = []

for link in all_link:
  response = requests.get(link)
  link_data = crawler.process_link_to_csv(response.text)
  header = link_data[0]
  link_data.remove(header)
  link_removed_header = link_data
  dataframes.append(DataFrame(link_removed_header, columns=header))

concated = pandas.concat(dataframes)
# concated.to_pickle("/home/septian/dataframes-harian-bei.pkl")

all_ticker = list(concated.ticker.unique())

# tics = []
for ticker in all_ticker:
  ticker_data = concated.loc[concated["ticker"] == ticker]
  # ticker_data.to_pickle("/home/septian/ticker_data/" + ticker + ".pkl")
  ticker_list = list(map(lambda x: float(x), list(ticker_data.close)))
  last19 = ticker_list[-19:]
  last4 = ticker_list[-4:]
  last = ticker_list[-1]

  if util.get_nearest_possible_price(last) != last: # some odd index, like IHSG or ISSI
    continue

  cross_price = (sum(last19) - 4 * sum(last4)) / 3 # use little math to simplify computation

  (ara, arb) = util.get_auto_reject_limit(last)
  if cross_price > last:
    (tick_function, target_cross_price) = (util.get_next_tick, util.get_nearest_possible_price(cross_price))
  else:
    (tick_function, target_cross_price) = (util.get_prev_tick, util.get_nearest_possible_price(cross_price, True))
  
  tick_counter = 0
  price_holder = last

  while(price_holder != target_cross_price):
    price_holder = tick_function(price_holder)
    tick_counter += 1
  
  cross_type = "Golden Cross" if last < cross_price else "Dead Cross"
  possible = True if (cross_type == "Golden Cross" and cross_price < ara) or (cross_type == "Dead Cross" and cross_price > arb) else False

  # if possible:
    # tics.append(tick_counter)
  
  if 5 < tick_counter < 10 and cross_type == "Golden Cross":
    print("""
Ticker: {0}
Cross price: {1}
Prev price: {2}
Tick before cross: {3}
Cross type: {4}
Possible: {5}
""".format(ticker, cross_price, last, tick_counter, cross_type, possible))