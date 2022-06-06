# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:16:35 2021
@author: Ivan
版權屬於「行銷搬進大程式」所有，若有疑問，可聯絡ivanyang0606@gmail.com

Line Bot聊天機器人
第一章 Line Bot申請與串接
Line Bot機器人串接與測試
"""
#載入LineBot所需要的套件
import os
from flask import Flask, request, abort
#test
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('9pIVzQsUEI08RidYJzOwaZPDLNbneY9dIDHddgvx5MZu2PJkWH6nz9kue7wt56SNxogCf+p5D+WpmW0nrHZ1vY5LRnOytVROJ+8m0Q/cXMoRzi+8ZvkWuNeGokAYcOZhu4c/1M/fJTA7raGxPtV91wdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('21d57c590dcdfe2564cc65574fdc8724')

line_bot_api.push_message('Ud6ce2036c8854221694d3f33b3b796c3', TextSendMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text = event.message.text
    if re.match('開始', message):
        buttons_template_message = TemplateSendMessage(
            alt_text='這個看不到',
            template=ButtonsTemplate(
                title='Menu',
                text='請選擇類型',
                actions=[
                    PostbackTemplateAction(
                        label='酒吧',
                        text='酒吧'
                        data='A&酒吧'
                    ),
                    PostbackTemplateAction(
                        label='旅館',
                        text='旅館'
                        data='A&旅館'
                    ),
                    PostbackTemplateAction(
                        label='全都要',
                        text='全都要'
                        data='A&全都要'
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif message == '酒吧' or message == '旅館' or message == '全都要':
        bar_or_hotel = event.postback.data[2:]
        flex_message = TextSendMessage(text='請輸入台北市的任意地區（區或街道），或點擊下列的快捷鍵選擇地區',  # （暫時只能做到有選項，無法自由填入）
                                       quick_reply=QuickReply(items=[
                                            QuickReplyButton(action=PostbackAction(
                                                label="中正區", text="中正區", data='B&' + bar_or_hotel + '&中正區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="萬華區", text="萬華區", data='B&' + bar_or_hotel + '&萬華區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="大同區", text="大同區", data='B&' + bar_or_hotel + '&大同區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="中山區", text="中山區", data='B&' + bar_or_hotel + '&中山區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="松山區", text="松山區", data='B&' + bar_or_hotel + '&松山區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="大安區", text="大安區", data='B&' + bar_or_hotel + '&大安區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="信義區", text="信義區", data='B&' + bar_or_hotel + '&信義區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="內湖區", text="內湖區", data='B&' + bar_or_hotel + '&內湖區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="南港區", text="南港區", data='B&' + bar_or_hotel + '&南港區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="士林區", text="士林區", data='B&' + bar_or_hotel + '&士林區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="北投區", text="北投區", data='B&' + bar_or_hotel + '&北投區')),
                                            QuickReplyButton(action=PostbackAction(
                                                label="文山區", text="文山區", data='B&' + bar_or_hotel + '&文山區')),
                                       ]))
        line_bot_api.reply_message(event.reply_token, flex_message)
    else:
        result = event.postback.data[2:].split('&')


# 主程式
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
