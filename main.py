# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)

import numpy as np
from numpy import random

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
# channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)#環境変数を取得#デプロイするにあたり消去
# channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
# if channel_secret is None:
#     print('Specify LINE_CHANNEL_SECRET as environment variable.')
#     sys.exit(1)
# if channel_access_token is None:
#     print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
#     sys.exit(1)
#環境変数が上手く働いてないから、直接渡してる
line_bot_api = LineBotApi("U+AMWqgERs8D9PSxXCWb0pa3JBIfHr9YXTO6NUdDCCx9t4uhyfwVn+qU5iMaO49hdUd+3SG7gT6qc4LJreJ2kzajP+2h8s75nRtyco91aYuueA8XWY+E3g/mNC0cq95syaeOTFLV6sKnoPob75avXwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("3a50698d76d97d5f0705fb5e3995090b")

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise




@app.route("/")
def hello():
    return 'hello'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']


    # get request body as text
    body = request.get_data(as_text=True)   #ここにeventの情報がはいっている
    app.logger.info("Request body: " + body)    #これでコマンドラインに表示してる

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


count = 0   #開け閉め用の変数
@handler.add(MessageEvent, message=TextMessage)#Eventによりeventのもつattributeがそれぞれ違う。README参照
def handle_text_message(event):#userからのアクション（文字列の情報）がeventに代入される
    # print(type(event))#出力：class 'linebot.models.events.MessageEvent'
    # #おそらく@handler.add(MessageEvent, message=TextMessage)の中のeventは自動的にこのクラスになる
    # print(event)#出力：{"message": {"id": "8956345095646", "text": "\u3042", "type": "text"},       #辞書型
    #                    #"replyToken": "f62bdc97a9154a53ac1ef2cec8e7cecf",
    #                    #"source": {"type": "user", "userId": "U90270fb......"},
    #                    #"timestamp": 1543913681446,
    #                    #"type": "message"}
    # print(event.source)#出力：{"type": "user", "userId": "U90270fbcc310d31bb0c7bdbaa1e4b01c"}#eventの情報を取り出せる
    # print("type:{}, userId:{}".format(event.source.type, event.source.user_id)) #要素ごとに取り出せます
    # print(event.message)#出力：{"id": "8956223132859", "text": "\u3042", "type": "text"}ちなみに”あ”を送った.一文字ずつ割り振られてるらしい
    # print("id:{}, text:{}, type:{}".format(event.message.id, event.message.text, event.message.type))#要素ごとに取り出せます
    # print(event.reply_token)
    # print(event.timestamp)
    # print(event.type)
    text = event.message.text  #これで"text"を文字列に変換している
    print("handle_text_message")
    print(text)

    global count
    #print(count)

    #count = 0#ここにこれをおいておくとメッセージが来るたび初期化されてしまっていた
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    if text == 'profile':
        print(event.source.user_id)
        print(event.source)
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile("U90270fbcc310d31bb0c7bdbaa1e4b01c")#event.source.user_id)#第一引数のオブジェクトが、第二引数の型のインスタンス、またはサブクラスのインスタンスであればTrueを返す関数
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='Display name: ' + profile.display_name),
                    TextSendMessage(text='Status message: ' + profile.status_message)
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't use profile API without user ID"))
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    elif text == 'bye':#botがどこに属しているかでeventの属性が変わる
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            print(event.source)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='もう一緒に入れないんだね。。。\n今まで楽しかったよ。\nばいばい、げんきでね。'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
#たくさんのボタンを表示できる
    elif text == 'どこ？':
        buttons_template = ButtonsTemplate(
            title='What are you looking for?', text='Please pless buttons.', actions=[
                #URIAction(label='Go to line.me', uri='https://line.me'),
                #PostbackAction(label='ping', data='ping'),
                #PostbackAction(label='ping with text', data='a'),#dataに入ってる文字列がコマンドラインに出力される
                MessageAction(label='ビス', text='ビス'),
                MessageAction(label='さしがね', text='さしがね'),
                MessageAction(label='ちょうつがい', text='ちょうつがい'),
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)#alt_textはbotがボタンを送信したときの通知表示メッセージ
        line_bot_api.reply_message(event.reply_token, template_message)
        #print(postback.data)
        #if event.postback.data == 'a':
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    elif text == "ビス":
         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="みぎらへん"))

    elif text == "さしがね":
         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="ビスの近く"))

    elif text == "ちょうつがい":
         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="したのほう"))

    elif text == "やま":
         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="うみ"))

    elif text == "うみ":
         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="やま"))

    elif text == "あけ": #or "ひらけ" or "ひらけごま" or "あやみん":
        print(count)
        if count%2 == 0:    #偶数の時（開いているとき）のみ実行可能
            try:
                profile = line_bot_api.get_profile(event.source.user_id)
                line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                    TextSendMessage(text=profile.display_name + "が４番開けました"))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="あけたよ！"))
                count+=1
                print(count)
            except LineBotApiError as e:
                pass
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="もうあいてるよ"))
            print(count)

    elif text == "しめ":
        print(count)
        if count % 2 == 1:    #奇数の時（閉まっているとき）のみ実行可能
            try:
                profile = line_bot_api.get_profile(event.source.user_id)
                line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                    TextSendMessage(text=profile.display_name + "が４番閉めました"))
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text="しめたよ！"))
                count+=1
                print(count)
            except LineBotApiError as e:
                pass
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="もうしまってるよ"))
            print(count)

    elif text == "count":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=count))

    elif text == "あいてる？":
        if count%2 == 0:
            print(count)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="しまってるよ"))
        else:
            print(count)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="あいてるよ"))

    elif text == "🎲":
         dice = np.random.randint(1,7)
         line_bot_api.reply_message(event.reply_token, TextSendMessage(text=dice))

    elif text == "みんはや":
         line_bot_api.reply_message(event.reply_token, TextSendMessage(text="https://zt29q.app.goo.gl/H3Ed"))

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
#下にぴゅっと出てくるやつ
    elif text == 'どこ？？':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='選んでね',
                quick_reply=QuickReply(
                    items=[
                        #QuickReplyButton(
                        #    action=PostbackAction(label="label1", data="data1")
                        #),
                        QuickReplyButton(
                            action=MessageAction(label="ビス", text="ビス")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="さしがね", text="さしがね")
                        ),
                        QuickReplyButton(
                            action=MessageAction(label="ちょうつがい", text="ちょうつがい")
                        ),

                        #QuickReplyButton(
                        #    action=DatetimePickerAction(label="label3",
                        #                                data="data3",
                        #                                mode="date")
                        #),
                        #QuickReplyButton(
                        #    action=CameraAction(label="label4")
                        #),
                        #QuickReplyButton(
                        #    action=CameraRollAction(label="label5")
                        #),
                        #QuickReplyButton(
                        #    action=LocationAction(label="label6")
                        #),
                    ])))
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text))
        profile = line_bot_api.get_profile(event.source.user_id)
        line_bot_api.push_message("U90270fbcc310d31bb0c7bdbaa1e4b01c",
            TextSendMessage(text="{}が『{}』っていったよ".format(profile.display_name,event.message.text)))
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
#位置情報
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
#スタンプ
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
#ここに軍司クラシファーの実装部分を書く
# from keras.models import Sequential, load_model
# import tensorflow as tf
# from PIL import Image
# import keras
# import numpy as np
#
# graph = tf.get_default_graph()#add
# model = load_model('gunji_CNN_1.h5')#こっちに移した
# @handler.add(MessageEvent, message=(ImageMessage))
# def handle_content_message(event):
#     global graph#add
#     #model = load_model('gunji_CNN_1.h5')
#     with graph.as_default():#add　下全部インデント下げた
#         message_content = line_bot_api.get_message_content(event.message.id)#この辺でやっていることが謎.おそらく、ここで写真を保存してるはず
#         with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix="jpg" + '-', delete=False) as tf:
#             for chunk in message_content.iter_content():
#                 tf.write(chunk)
#                 tempfile_path = tf.name
#
#         dist_path = tempfile_path + '.' + "jpg"#ファイルに保存される名前はこの変数に入っている
#         dist_name = os.path.basename(dist_path)#dist_pathの中から、ファイルの名前だけを取り出すらしい
#         os.rename(tempfile_path, dist_path)#これでファイルに保存できている#のではなく、ファイルの名前を書き換えているだけ
#
#         filepath = os.path.join('static', 'tmp', dist_name)#これでwin mac 関係なく各引数をくっつけられる
#
# #以下main.pyと同じ
#         image = Image.open(filepath)
#         image = image.convert("RGB")
#         image = image.resize((100,100))
#         data = np.asarray(image)
#         X = []
#         X.append(data)
#         X = np.array(X)
#
#         result = model.predict([X])[0]
#         predicted = result.argmax()#このモデルの出力層は2だから、predictedは０or１
#
#         if predicted == 0:
#             line_bot_api.reply_message(
#             event.reply_token, [
#             TextSendMessage(text='ゲン')
#             ])
#         if predicted == 1:
#             line_bot_api.reply_message(
#             event.reply_token, [
#             TextSendMessage(text='どうみても軍司')
#             ])
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    print(event.message)


    if isinstance(event.message, ImageMessage):#event.messageのtypeがImageMessageだったら実行
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name



    dist_path = tempfile_path + '.' + ext  #これがフォルダに保存されるときのpath
    dist_name = os.path.basename(dist_path)#これがなくてもいけるぽい
    os.rename(tempfile_path, dist_path)

    print(dist_path)
    print(dist_name)

    #以下の部分がなくても、ファイルの保存はできてる
    line_bot_api.reply_message(
       event.reply_token, [
           TextSendMessage(text='Save content.'),
           TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
       ])

#ファイル
@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save file.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
@handler.add(FollowEvent)
def handle_follow(event):
    #誰が追加したかわかるように機能追加
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.push_message("U90270fbcc310d31bb0c7bdbaa1e4b01c",
        TextSendMessage(text="display_name:{}\nuser_id:{}\nstatus_message:{}\npicture_url:{}"\
        .format(profile.display_name, profile.user_id, profile.status_message, profile.picture_url)))

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
@handler.add(UnfollowEvent)
def handle_unfollow(event):

    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.push_message("U90270fbcc310d31bb0c7bdbaa1e4b01c",
        TextSendMessage(text="display_name:{}\nuser_id:{}\nstatus_message:{}\npicture_url:{}"\
        .format(profile.display_name, profile.user_id, profile.status_message, profile.picture_url)))

    app.logger.info("Got Unfollow event")#ここでコマンドラインに出力している

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(event.reply_token,
        TextSendMessage(text='何度でも蘇るさ！！')) #event.source.typeにはroomが入っている

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★



#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))

#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int, default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()
    app.debug = True
    app.run(port=options.port)
#debug=options.debug
