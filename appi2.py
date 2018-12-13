# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributedfrom sense_hat import SenseHat


#  under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
import subprocess
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

from sense_hat import SenseHat
import time
import picamera
import cv2
from keras.models import Sequential, load_model
import tensorflow as tf
import keras
import numpy as np

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable


#channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
#channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
#if channel_secret is None:
#    print('Specify LINE_CHANNEL_SECRET as environment variable.')
#   sys.exit(1)
#if channel_access_token is None:
#    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
#    sys.exit(1)

line_bot_api = LineBotApi("U+AMWqgERs8D9PSxXCWb0pa3JBIfHr9YXTO6NUdDCCx9t4uhyfwVn+qU5iMaO49hdUd+3SG7gT6qc4LJreJ2kzajP+2h8s75nRtyco91aYuueA8XWY+E3g/mNC0cq95syaeOTFLV6sKnoPob75avXwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("3a50698d76d97d5f0705fb5e3995090b")

static_tmp_path = os.path.jimage = Image.open(filepath)
#         image = image.convert("RGB")
#         image = image.resize((100,100))
#         data = np.asarray(image)
#         X = []
#         X.append(data)
#         X = np.array(X)
#
#         result = model.predict([X])[0]
#         predicted = result.argmax()oin(os.path.dirname(__file__), 'static', 'tmp')


# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise
#-----------------------------------------------------------------------------------------
sense = SenseHat()
#while True:
acceleration = sense.get_accelerometer_raw()
x = acceleration['x']
    #y = acceleration['y']
    #z = acceleration['z']
 
x=round(x, 0)
    #y=round(y, 0)
    #z=round(z, 0)
 
    #print("x=%s, y=%s, z=%s" % (x, y, z))
time.sleep(1)

if x == -1:
    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                  TextSendMessage(text="４番開けました"))
#-----------------------------------------------------------------------------------------
#import time
#import picamera
#number = 0
#while True:
#    with picamera.PiCamera() as camera:
#     camera.resolution = (1024, 1024)
#     camera.start_preview()
 # Camera warm-up time
#     time.sleep(2)
      
#     save_path = "./inputs/" + str(number) + ".jpg"
#     camera.capture(save_path)
                    #image = Image.open(filepath)
#         image = image.convert("RGB")
#         image = image.resize((100,100))
#         data = np.asarray(image)
#         X = []
#         X.append(data)
#         X = np.array(X)
#
#         result = model.predict([X])[0]
#         predicted = result.argmax()
#     number += 1
    
    
    
    
    
    
    
    
#-----------------------------------------------------------------------------------------

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
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

count = 0
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)
    global count

    

    
#-----------------------------------------------------------------------------------------
    if text == 'bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='Leaving group'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Bot can't leave from 1:1 chat"))
#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------

    elif text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping'),
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
#-----------------------------------------------------------------------------------------
    elif text == '点灯':
        subprocess.check_call(['python','LpikaON.py'])
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='点灯しました。'))
    elif text == '消灯':
        subprocess.check_call(['python','LpikaOFF.py'])
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='消灯しました。'))
#-----------------------------------------------------------------------------------------
    elif text == "pion":
        
        sense = SenseHat()
        while True:
            acceleration = sense.get_accelerometer_raw()
            x = acceleration['x']
            y = acceleration['y']
              #z = acceleration['z']
 
            x=round(x, 0)
            y=round(y, 0)
            #z=round(z, 0)
 
            #print("x=%s, y=%s, z=%s" % (x, y, z))
            time.sleep(1)

            if x == -1 and count%2 == 0:
                line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                    TextSendMessage(text="４番開けました"))
                count += 1
                print(count)
            if y == -1 and count%2 == 1:
                line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                    TextSendMessage(text="４番閉めました"))
                count += 1
                print(count)
#-----------------------------------------------------------------------------------------
    elif text == "pion2":
        
        graph = tf.get_default_graph()#add
        model = load_model('soshoku_CNN_4.h5')

        number = 0
        while True:
            global graph
            with picamera.PiCamera() as camera:
                camera.resolution = (1024, 1024)
                camera.start_preview()
 # Camera warm-up time
                time.sleep(2)      
                save_path = "./inputs/" + str(number) + ".jpg"
                camera.capture(save_path)                    
                number += 1
    
                image = cv2.imread(save_path)
                 
                #image = image.convert("RGB")
                image = cv2.resize(image,(32,32))
                data = np.asarray(image)
                X = []
                X.append(data)
                X = np.array(X)

                result = model.predict([X])[0]
                predicted = result.argmax()
                
                if predict == 0:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="1が４番閉めました"))
                if predict == 1:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="2が４番閉めました"))
                if predict == 2:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="3が４番閉めました"))
                if predict == 3:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="4が４番閉めました"))
                if predict == 4:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="5が４番閉めました"))
                if predict == 5:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="6が４番閉めました"))
                if predict == 6:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="7が４番閉めました"))
                if predict == 7:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="8が４番閉めました"))
                if predict == 8:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="9が４番閉めました"))
                if predict == 9:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="10が４番閉めました"))
                if predict == 10:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="11が４番閉めました"))
                if predict == 11:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="12が４番閉めました"))
                if predict == 12:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="12が４番閉めました"))
                if predict == 13:
                    line_bot_api.push_message("R3c632537651ba924d66158844d8c4848",
                            extSendMessage(text="13が４番閉めました"))

#-----------------------------------------------------------------------------------------

    elif text == "あけ": 
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


#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------

    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
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

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


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


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow event")


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


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


@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


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
    app.run(debug=options.debug, port=options.port)