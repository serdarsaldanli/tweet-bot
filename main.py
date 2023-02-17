import snscrape.modules.twitter as sntwitter
import MetaTrader5 as mt5

# The search query you want to search for
search_query1 = "pair: #"
search_query2 = "trade: "
search_query3 = "entry: "
search_query4 = "sl: "

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
        extracted_text1 = tweet.rawContent[index1 + len(search_query1):index1 + len(search_query1) + 6]
        extracted_text2 = tweet.rawContent[index2 + len(search_query2):index2 + len(search_query2) + 4]
        extracted_text3 = tweet.rawContent[index3 + len(search_query3):index3 + len(search_query3) + 7]
        extracted_text4 = tweet.rawContent[index4 + len(search_query4):index4 + len(search_query4) + 7]
        filtered_tweets.append(extracted_text1)
        filtered_tweets.append(extracted_text2)
        filtered_tweets.append(extracted_text3)
        filtered_tweets.append(extracted_text4)
        if len(filtered_tweets) == 4:
            break

print(filtered_tweets)


# Connect to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

if "Sell" in filtered_tweets:

    # prepare a trade request
    symbol = None
    for i, text in enumerate(filtered_tweets):
        if i % 4 == 0 and text.startswith("#"):
            symbol = text
            break

    if symbol:
        action = mt5.TRADE_ACTION_DEAL
        type = mt5.ORDER_TYPE_SELL
        volume = 0.10
        price = mt5.symbol_info_tick(symbol).bid
        request = {
            "action": action,
            "symbol": symbol,
            "type": type,
            "volume": volume,
            "price": price,
            "sl": price + 10 * mt5.symbol_info(symbol).point,
            "tp": price - 30 * mt5.symbol_info(symbol).point,
            "deviation": 10,
            "magic": 123456,
            "comment": "Python sell order",
        }
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Failed to send trade request: ", result.comment)
        else:
            print("Trade request sent successfully: ", result)

else:
    # Place a buy order
    symbol = None
    for i, text in enumerate(filtered_tweets):
        if i % 4 == 0 and text.startswith("#"):
            symbol = text
            break

    if symbol:
        action = mt5.TRADE_ACTION_DEAL
        type = mt5.ORDER_TYPE_BUY
        volume = 0.10
        price = mt5.symbol_info_tick(symbol).ask
        request = {
            "action": action,
            "symbol": symbol,
            "type": type,
            "volume": volume,
            "price": price,
            "sl": price - 10 * mt5.symbol_info(symbol).point,
            "tp": price + 30 * mt5.symbol_info(symbol).point,
            "deviation": 10,
            "magic": 123456,
            "comment": "Python buy order",
        }
        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("Failed to send trade request: ", result.comment)
        else:
            print("Trade request sent successfully: ", result)

    # Disconnect from the MetaTrader 5 terminal
    mt5.shutdown()

    print(filtered_tweets[1])
