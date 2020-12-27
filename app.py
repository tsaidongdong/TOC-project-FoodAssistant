import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message,send_image_message

load_dotenv()


machine = TocMachine(
    states=["user","menu",
    "food_recommend","tainan_food","kaohsiung_food","chiayi_food",
    "cal_drink_calories", "tea_base","tea","yakult","milk","sugar_content","sugar_free","half_sugar","all_sugar","ingredients","fairy_grass",
    "coconut","pearl","all_calories",
    "cancel"],
    transitions=[
        {"trigger": "advance","source": "user","dest": "menu","conditions": "is_going_to_menu",},
        {"trigger": "advance","source": "menu","dest": "cal_drink_calories","conditions": "is_going_to_cal_drink_calories",},
        {"trigger": "advance","source": "cal_drink_calories","dest": "tea_base","conditions": "is_going_to_tea_base",},
        {"trigger": "advance","source": "tea_base","dest": "cancel","conditions": "is_going_to_cancel",},
        {"trigger": "advance","source": "tea_base","dest": "tea","conditions": "is_going_to_tea",},
        {"trigger": "advance","source": "tea_base","dest": "yakult","conditions": "is_going_to_yakult",},
        {"trigger": "advance","source": "tea_base","dest": "milk","conditions": "is_going_to_milk",},
        {"trigger": "advance","source": ["milk","yakult","tea"],"dest": "sugar_content","conditions": "is_going_to_sugar_content",},
        {"trigger": "advance","source": "sugar_content","dest": "cancel","conditions": "is_going_to_cancel",},
        {"trigger": "advance","source": "sugar_content","dest": "sugar_free","conditions": "is_going_to_sugar_free",},
        {"trigger": "advance","source": "sugar_content","dest": "half_sugar","conditions": "is_going_to_half_sugar",},
        {"trigger": "advance","source": "sugar_content","dest": "all_sugar","conditions": "is_going_to_all_sugar",},
        {"trigger": "advance","source": ["sugar_free","half_sugar","all_sugar"],"dest": "ingredients","conditions": "is_going_to_ingredients",},
        {"trigger": "advance","source": "ingredients","dest": "cancel","conditions": "is_going_to_cancel",},
        {"trigger": "advance","source": "ingredients","dest": "fairy_grass","conditions": "is_going_to_fairy_grass",},
        {"trigger": "advance","source": "ingredients","dest": "coconut","conditions": "is_going_to_coconut",},
        {"trigger": "advance","source": "ingredients","dest": "pearl","conditions": "is_going_to_pearl",},
        {"trigger": "advance","source": ["fairy_grass","coconut","pearl"],"dest": "all_calories","conditions": "is_going_to_all_calories",},
        {"trigger": "advance","source": "menu","dest": "food_recommend","conditions": "is_going_to_food_recommend",},
        {"trigger": "advance","source": "food_recommend","dest": "tainan_food","conditions": "is_going_to_tainan_food",},
        {"trigger": "advance","source": "food_recommend","dest": "kaohsiung_food","conditions": "is_going_to_kaohsiung_food",},
        {"trigger": "advance","source": "food_recommend","dest": "chiayi_food","conditions": "is_going_to_chiayi_food",},
        {"trigger": "go_back", "source": ["all_calories","tainan_food","kaohsiung_food","chiayi_food","cancel"], "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')
        
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, 'https://i.imgur.com/mhOz55s.png') 
            elif machine.state == 'user' and event.message.text.lower() != 'fsm':
                send_text_message(event.reply_token, '輸入『menu』即可開始使用卡路里小幫手。\n隨時輸入『fsm』可以得到當下的狀態圖。')
            else:
                send_text_message(event.reply_token, "請按照指示操作")

    return "OK"


""""@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")"""


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
