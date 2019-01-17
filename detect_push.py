from keras.models import Sequential, load_model
import tensorflow as tf
import cv2
import numpy as np
from linebot import LineBotApi
from linebot.models import TextSendMessage, ImageSendMessage
from linebot.exceptions import LineBotApiError
import sys, os, time


SAVE_PATH = "./input/"
filepath = SAVE_PATH + "face.jpg"
# filepath2 = "http://127.0.0.1:5000/uploads/face.jpg"
# filepath3 = "https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2F1.bp.blogspot.com%2F-RslsA3JLAIE%2FVD71dZGoseI%2FAAAAAAAEBDo%2FVdY50Qf82FI%2Fs1600%2FLINE%252Bfor%252BiPad-02.png&f=1"
#filepath4 =

model = load_model('soshoku_CNN_4.h5')#学習済みモデルをロードする
#face_detect_count = 0

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
line_bot_api = LineBotApi(channel_access_token)

def make_img_message():
    messages = ImageSendMessage(original_content_url=filepath, preview_image_url=filepath)
    return messages
messages = make_img_message()

# global graph
graph = tf.get_default_graph()
with graph.as_default():
#以下、送信された画像をモデルに入れる
    image = cv2.imread(filepath)
    image = cv2.resize(image,(32,32)) #image_sizeはloadするモデルが学習した画像のサイズにそろえる
    data = np.array([image])#ここでリストとして渡す。np.arrayはリストをnumpy配列に変換する。
    result = model.predict(data)#出力層のニューロンの値が入っている。
    predicted = result.argmax()#このモデルの出力層は12なので、predictedは０or１or...
    members = {0:"あかり",1:"あやみ",2:"はるか",3:"かいせい",4:"けいたろう",5:"こうりゅう",6:"まや",7:"ももか",8:"りょうご",9:"りょうこ",10:"かな",11:"ともか",12:"やたこ",13:"ゆーすけ"}

    try:                            #メッセージを送信したい相手のIDを入力
        line_bot_api.push_message("R3c632537651ba924d66158844d8c4848", TextSendMessage(text = members[predicted] + "が４番を開けました"))
        line_bot_api.push_message("U90270fbcc310d31bb0c7bdbaa1e4b01c", messages)
    except LineBotApiError as e:
        # error handle
        ...
#R3c632537651ba924d66158844d8c4848
