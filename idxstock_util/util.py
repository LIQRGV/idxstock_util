def get_price_fraction(price, negative=False):
  if not negative:
    if price < 200:
      fraction = 1
    elif price < 500:
      fraction = 2
    elif price < 2000:
      fraction = 5
    elif price < 5000:
      fraction = 10
    elif price >= 5000:
      fraction = 25
  else:
    if price <= 200:
      fraction = 1
    elif price <= 500:
      fraction = 2
    elif price <= 2000:
      fraction = 5
    elif price <= 5000:
      fraction = 10
    elif price > 5000:
      fraction = 25

  return fraction

def get_next_tick(price):
  possible_price = get_nearest_possible_price(price)
  return possible_price + get_price_fraction(possible_price)

def get_prev_tick(price):
  possible_price = get_nearest_possible_price(price)
  return possible_price - get_price_fraction(possible_price, True)

def get_nearest_possible_price(price, round_up=False):
  fraction = get_price_fraction(price)
  
  return (price // fraction + (1 if price % fraction != 0 and round_up else 0)) * fraction

def get_auto_reject_limit(price):
  if price < 200:
    limit = 0.35
  elif 200 <= price < 5000:
    limit = 0.25
  elif price >= 5000:
    limit = 0.20

  return (
    get_nearest_possible_price(price * (1 + limit)),
    get_nearest_possible_price(price * (1 - limit), True),
  )