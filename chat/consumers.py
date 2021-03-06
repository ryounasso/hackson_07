import json
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
import datetime

# ChatConsumerクラス: WebSocketから受け取ったものを処理するクラス

USERNAME_SYSTEM = '*system*'


class ChatConsumer(AsyncWebsocketConsumer):

    # ルーム管理
    rooms = None

    # コンストラクタ

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if ChatConsumer.rooms is None:
            ChatConsumer.rooms = {}
        self.strGroupName = ''
        self.strUserName = ''

    # WebSocket接続時の処理
    async def connect(self):
        # WebSocket接続を受け入れます。
        # ・connect()でaccept()を呼び出さないと、接続は拒否されて閉じられます。
        # 　たとえば、要求しているユーザーが要求されたアクションを実行する権限を持っていないために、接続を拒否したい場合があります。
        # 　接続を受け入れる場合は、connect()の最後のアクションとしてaccept()を呼び出します。
        await self.accept()

    # WebSocket切断時の処理
    async def disconnect(self, close_code):
        # チャットからの離脱
        await self.leave_chat()

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）

    async def receive(self, text_data):
        # 受信データをJSONデータに復元
        text_data_json = json.loads(text_data)

        # チャットへの参加時の処理
        if('join' == text_data_json.get('data_type')):
            # ユーザー名をクラスメンバー変数に設定
            self.strUserName = text_data_json['username']
            # ルーム名の取得
            strRoomName = text_data_json['roomname']
            # チャットへの参加
            await self.join_chat(strRoomName)

        # チャットからの離脱時の処理
        elif('leave' == text_data_json.get('data_type')):
            # チャットからの離脱
            await self.leave_chat()
        # メッセージ受信時の処理
        else:
            if text_data_json['message'] != 'null':
                # メッセージの取り出し
                message = text_data_json['message']
                countMember = text_data_json['member']
                data = {
                    'type': 'chat_message',  # 受信処理関数名
                    'message': message,  # メッセージ
                    'username': self.strUserName,  # ユーザー名
                    'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
                    'image': 'null',
                    'member': countMember,
                }
            else:
                image = text_data_json['image']
                countMember = text_data_json['member']
                data = {
                    'type': 'chat_message',
                    'message': 'null',
                    'username': self.strUserName,
                    'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
                    'image': image,
                    'member': countMember,
                }
            await self.channel_layer.group_send(self.strGroupName, data)

    # 拡散メッセージ受信時の処理

    async def chat_message(self, data):
        data_json = {
            'message': data['message'],
            'username': data['username'],
            'datetime': data['datetime'],
            'image': data['image'],
            'member': data['member'],
        }

        # WebSocketにメッセージを送信
        await self.send(text_data=json.dumps(data_json))

    # チャットへの参加
    async def join_chat(self, strRoomName):
        # グループに参加
        self.strGroupName = 'chat_%s' % strRoomName
        await self.channel_layer.group_add(self.strGroupName, self.channel_name)

        # 参加者数の更新
        room = ChatConsumer.rooms.get(self.strGroupName)
        numMember = 0
        if(None == room):
            # ルーム管理にルーム追加
            ChatConsumer.rooms[self.strGroupName] = {'participants_count': 1}
            numMember += 1
        else:
            room['participants_count'] += 1
            numMember = room['participants_count']
        # システムメッセージの作成
        strMessage = ""+self.strUserName+' joined.there are ' + \
            str(ChatConsumer.rooms[self.strGroupName]
                ['participants_count'])+' participants'
        strMessage = ""
        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        data = {
            'type': 'chat_message',  # 受信処理関数名
            'message': strMessage,  # メッセージ
            'username': USERNAME_SYSTEM,  # ユーザー名
            'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
            'image': 'null',
            'member': numMember,
        }
        await self.channel_layer.group_send(self.strGroupName, data)

    # チャットからの離脱

    async def leave_chat(self):
        if("" == self.strGroupName):
            return

        # グループから離脱
        await self.channel_layer.group_discard(self.strGroupName, self.channel_name)

        numMember = 0

        # 参加者数の更新
        ChatConsumer.rooms[self.strGroupName]['participants_count'] -= 1
        numMember = ChatConsumer.rooms[self.strGroupName]['participants_count']
        # システムメッセージの作成
        strMessage = '"' + self.strUserName + '" left. there are ' + \
            str(ChatConsumer.rooms[self.strGroupName]
                ['participants_count']) + ' participants'
        strMessage = ""
        # グループ内の全コンシューマーにメッセージ拡散送信（受信関数を'type'で指定）
        data = {
            'type': 'chat_message',  # 受信処理関数名
            'message': strMessage,  # メッセージ
            'username': USERNAME_SYSTEM,  # ユーザー名
            'datetime': datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),  # 現在時刻
            'image': 'null',
            'member': numMember,
        }
        await self.channel_layer.group_send(self.strGroupName, data)

        # 参加者がゼロのときは、ルーム管理からルームの削除
        if(0 == ChatConsumer.rooms[self.strGroupName]['participants_count']):
            del ChatConsumer.rooms[self.strGroupName]

        # ルーム名をからに
        self.strGroupName = ""
