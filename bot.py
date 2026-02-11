import requests
import telegram
import time
import random

TOKEN = "8229598243:AAE6LA3Ej_n3Qdwl-ibvy40Wt5hKHtcYOws"
CHANNEL_ID = "@RAJAGAMEVIPPREDICTION9"

bot = telegram.Bot(token=TOKEN)

B_POOL = [5,6,7,8,9]
S_POOL = [0,1,2,3,4]

last_issue = None
saved_prediction = None
saved_opposites = []

def get_data():
    url = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json"
    r = requests.get(url)
    return r.json()["data"]["list"]

while True:
    try:
        data = get_data()
        latest = data[0]
        issue = latest["issueNumber"]
        number = int(latest["number"])
        size = "BIG" if number >= 5 else "SMALL"

        # Check WIN / LOSS
        if last_issue and issue != last_issue:
            is_win = (saved_prediction == size) or (number in saved_opposites)

            result_text = "WIN 🐯" if is_win else "LOSS 🖤"

            result_msg = f"""
🎯 RESULT UPDATE

🆔 PERIOD: {last_issue}
📊 PREDICTION: {saved_prediction}
🔢 RESULT NUMBER: {number}
🏆 STATUS: {result_text}
"""
            bot.send_message(chat_id=CHANNEL_ID, text=result_msg)

        # NEW PREDICTION LOGIC
        last5 = data[:5]
        sizes = ["BIG" if int(x["number"]) >= 5 else "SMALL" for x in last5]

        if sizes.count("BIG") > 2:
            next_pred = "BIG"
            pool = S_POOL
        else:
            next_pred = "SMALL"
            pool = B_POOL

        opposites = random.sample(pool, 2)

        # Send Prediction
        pred_msg = f"""
🔥 WANTEDSCARY VIP AUTO 🔥

🆔 NEXT PERIOD: {int(issue)+1}
📊 PREDICTION: {next_pred}
🎯 OPPOSITE NUMS: {opposites[0]}, {opposites[1]}
"""
        bot.send_message(chat_id=CHANNEL_ID, text=pred_msg)

        # Save For Next Round Check
        last_issue = issue
        saved_prediction = next_pred
        saved_opposites = opposites

    except Exception as e:
        print("Error:", e)

    time.sleep(60)  # Check every 1 minute
