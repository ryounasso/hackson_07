import json
# from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

# ChatConsumerクラス: WebSocketから受け取ったものを処理するクラス


class ChatConsumer(AsyncWebsocketConsumer):
    # WebSocket接続時の処理
    async def connect(self):
        self.strGroupName = 'chat'
        await self.channel_layer.group_add(self.strGroupName, self.channel_name)

        # Websocket接続を受け入れる
        # accept()を呼び出さないと接続が拒否される
        await self.accept()

    async def disconnect(self, close_code):
        # グループから離脱
        await self.channel_layer.group_discard(self.strGroupName, self.channel_name)

    # WebSocketからのデータ受信時の処理
    # （ブラウザ側のJavaScript関数のsocketChat.send()の結果、WebSocketを介してデータがChatConsumerに送信され、本関数で受信処理します）
    async def receive(self, text_data):
        # 受信データをJSONデータに復元
        text_data_json = json.loads(text_data)

        # メッセージの取り出し
        message = text_data_json['message']
        data = {
            'type': 'chat_message',  # 受信処理関数名
            'message': message,  # メッセージ
        }
        await self.channel_layer.group_send(self.strGroupName, data)

    # 拡散メッセージ受信時の処理
    async def chat_message(self, data):
        data_json = {
            'message': data['message'],
        }

        # WebSocketにメッセージを送信
        await self.send(text_data=json.dumps(data_json))
