import snscrape.modules.twitter as sntwitter
import MetaTrader5 as mt5
import time

def get_tweets():

    # The search query you want to search for
    search_query1 = "pair: #"
    search_query2 = "trade: "
    search_query3 = "entry: "
    search_query4 = "sl: "
    search_query5 = "tp: "

    # Using TwitterSearchScraper to scrape data and append tweets to list
    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterProfileScraper("fxcanli").get_items()):
        if i > 10:  # You can change the number of tweets you want to scrape here
            break
        tweets_list.append(tweet)

    # Filtering tweets that contain the specific word and grabbing the 5 characters that come after it
    filtered_tweets = []
    for tweet in tweets_list:
        if search_query1 in tweet.rawContent.lower():
            index1 = tweet.rawContent.lower().index(search_query1)
            index2 = tweet.rawContent.lower().index(search_query2)
            index3 = tweet.rawContent.lower().index(search_query3)
            index4 = tweet.rawContent.lower().index(search_query4)
            index5 = tweet.rawContent.lower().index(search_query5)
            extracted_text1 = tweet.rawContent[index1 + len(search_query1):index1 + len(search_query1) + 6]
            extracted_text2 = tweet.rawContent[index2 + len(search_query2):index2 + len(search_query2) + 4]
            extracted_text3 = tweet.rawContent[index3 + len(search_query3):index3 + len(search_query3) + 7]
            extracted_text4 = tweet.rawContent[index4 + len(search_query4):index4 + len(search_query4) + 7]
            extracted_text5 = tweet.rawContent[index5 + len(search_query5):index5 + len(search_query5) + 7]
            filtered_tweets.append(extracted_text1)
            filtered_tweets.append(extracted_text2)
            filtered_tweets.append(extracted_text3)
            filtered_tweets.append(extracted_text4)
            filtered_tweets.append(extracted_text5)
            if len(filtered_tweets) == 5:
                break

    return filtered_tweets

def send_order(filtered_tweets):
    # Connect to the MetaTrader 5 terminal
    if not mt5.initialize():
        print("initialize() failed, error code =", mt5.last_error())

    if "Sell" in filtered_tweets:

        # prepare a trade request
        symbol = filtered_tweets[0]
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            mt5.shutdown()

        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol, True):
                print("symbol_select({}}) failed, exit", symbol)
                mt5.shutdown()

        lot = 0.1
        point = mt5.symbol_info(symbol).point
        price = round(float(filtered_tweets[2]), 3)
        sl = round(float(filtered_tweets[3]), 3)
        tp = round(float(filtered_tweets[4]), 3)
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": 234000,
            "comment": "Serdar Python Bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # send a trading request
        result = mt5.order_send(request)
        print(result);
        mt5.shutdown()

    else:
        # Place a buy order
        symbol = filtered_tweets[0]
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(symbol, "not found, can not call order_check()")
            mt5.shutdown()

        if not symbol_info.visible:
            print(symbol, "is not visible, trying to switch on")
            if not mt5.symbol_select(symbol, True):
                print("symbol_select({}}) failed, exit", symbol)
                mt5.shutdown()

        lot = 0.1
        point = mt5.symbol_info(symbol).point
        price = round(float(filtered_tweets[2]), 3)
        sl = round(float(filtered_tweets[3]), 3)
        tp = round(float(filtered_tweets[4]), 3)
        deviation = 20
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": deviation,
            "magic": 234000,
            "comment": "Serdar Python Bot",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        # send a trading request
        result = mt5.order_send(request)
        print(result);

        mt5.shutdown()

while True:
    filtered_tweets1 = get_tweets()
    time.sleep(180)
    filtered_tweets2 = get_tweets()
    if filtered_tweets2 == filtered_tweets1:
        print("No new tweet data.")
        pass
    else:
        send_order(filtered_tweets2)


