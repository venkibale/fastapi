from sys import exit
from pyrogram import Client
from pyrogram.handlers import MessageHandler
import requests
import time
import re
import sys


class telegramapi:

    def __init__(self, api_id, api_hash, chat_id):

        self.result_dict = {}
        self.urlList = []
        self.text_array = []
        self.app = Client(
            "moviesllike",
            api_id=api_id,
            api_hash=api_hash
        )
        self.chat_id = chat_id

    async def sendMessage(self, movie):
        await self.app.start()
        print("Send message")
        await self.app.send_message(int(self.chat_id), movie)
        await self.app.stop()

    async def getmessages(self):
        await self.app.start()
        message = await self.app.get_history(self.chat_id, limit=1)
        if message:

            if message[0].entities:
                temp = re.sub(r'(.*)Found.\n', '', message[0]["text"])
                self.text_array = temp.split('\n\n')
                # print(self.text_array)
                for messages in message[0].entities:

                    self.urlList.append(messages['url'])
                # print(self.urlList)

                # message.forward("me")
                if len(self.urlList) == len(self.text_array):
                    for index, val in enumerate(self.urlList):
                        self.result_dict[self.text_array[index]
                                         ] = self.urlList[index]
                # print('1', self.result_dict)

                await self.app.stop()
                return self.result_dict

            else:
                await self.app.stop()
                return {}
