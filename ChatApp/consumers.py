from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync ## এর মাধ্যমে async এর সকল Proparty কে sync এ ব্যবহার করার যায়

from channels.db import database_sync_to_async ## মুলত Channel Layout Django ORM support করে না, তাই এর সাহায্যে তা support করানো হয়েছে।
from ChatApp.models import Group, Chat

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
## NOTE Channel Layer -> দুটি বা multiple Instance নিজেদের মধ্যে জাতে Communicate করতে পারে তার জন্যে Channel Layer ব্যবহার করা হয়।

class MyWebsocketConsumer(WebsocketConsumer):

    def connect(self):
        print("Connect...........")
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)

        ## To Accept Connection
        self.accept()

        ## To Reject Connection
        # self.close()

        ## Group name is receive from frontend
        self.groupName = self.scope['url_route']['kwargs']['group_name']
        # print("Group Name = ", self.groupName)

        ## NOTE Add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
            # 'Bangladesh',   # Group Name
            self.groupName,   # Group Name
            self.channel_name
        )



    def receive(self, text_data = None, bytes_data = None):
        print("------------------------------------")
        print("Receive...........")
        print("Msg Receive = ", text_data)
        print("------------------------------------")

        ## To send Maggage by Server
        # self.send(text_data= "Maggage is sent by server...")
        # self.send(bytes_data= data)    # send bynary data

        ## To Reject Connection
        # self.close(code=4045) # error show by custome code 

        ## Realtime data send by server
        # for i in range(10):
        #     self.send(str(i))
        #     sleep(1)

        python_dic = json.loads(text_data)
        # data = python_dic['msg']

        ## Find Group Object
        ## এখানে Group obj find করা হয়েছে জাগে আমরা সেই Group এর Chat Table এ ঐ massage গুলো save করাতে পারি।
        # if Group.objects.filter(name = self.groupName).exists():
        group = Group.objects.get(name = self.groupName)


        if self.scope['user'].is_authenticated:
            ## Create a new chat object
            chat = Chat(
                group = group,
                user = self.scope['user'],
                content = python_dic['msg'],
            ).save()

            ## username msg এর সাথে fontend এ show করানোর জন্যে একটি variable এ store করা হয়েছে
            python_dic['user'] = self.scope['user'].username
            # print("---------------------------")
            # print("Data = ", python_dic)
            # print("---------------------------")
            
            ## Display the massage in user chat page
            async_to_sync(self.channel_layer.group_send)(
                self.groupName,{
                    'type': 'chat.message',   # Chat Message Hendler টি নিচে Creat করা হয়েছে
                    'message': json.dumps(python_dic),
                }
            )
        else:
            self.send(text_data= json.dumps({
                "msg": "Login Required", 
                "user": "unknown",
                })
                )

        
    ## Chat Message Event Hendler টি Create করার জন্যে . এর যায়গায় শুধু _ দিতে হবে chat.message কে chat_message লিখতে হবে।
    def chat_message(self, event):  
        print('Event....', event)
        print('Data', event['message']) # Data type is string 

        # এখন আমাদের এই data টি কে Text area তে দেখাতে চাইলে তা Send করতে হবে
        self.send(text_data= json.dumps({
            'msg':event['message']
        }))




    def disconnect(self, close_code):
        print("Disconnect...........", close_code)
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)

        ## NOTE Add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_discard)(
            self.groupName,   # Group Name
            self.channel_name
        )
        # raise StopConsumer()












class MyAsyncWebsocketConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("Connect...........")
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)

        ## To Accept Connection
        await self.accept()

        ## To Reject Connection
        # await self.close()

        ## Group name is receive from frontend
        self.groupName = self.scope['url_route']['kwargs']['group_name']
        print("Group Name = ", self.groupName)

        ## NOTE Add a channel to a new or existing group
        await self.channel_layer.group_add(
            # 'Bangladesh',   # Group Name
            self.groupName,   # Group Name
            self.channel_name
        )



    async def receive(self, text_data = None, bytes_data = None):
        print("------------------------------------")
        print("Receive...........")
        print("Msg Receive = ", text_data)
        print("------------------------------------")

        ## To send Maggage by Server
        await self.send(text_data= "Maggage is sent by server...")
        # await self.send(bytes_data= data)    # send bynary data

        ## To Reject Connection
        # await self.close(code=4045) # error show by custome code 

        ## Realtime data send by server
        # for i in range(10):
        #     await self.send(str(i))
        #     await asyncio.sleep(1)

        python_dic = json.loads(text_data)
        # data = python_dic['msg']

        ## এখানে Group obj find করা হয়েছে জাগে আমরা সেই Group এর Chat Table এ ঐ massage গুলো save করাতে পারি।
        # if Group.objects.filter(name = self.groupName).exists():
        group = await database_sync_to_async(Group.objects.get)(name = self.groupName)

        if self.scope['user'].is_authenticated:
            chat = Chat(
                group = group,
                user = self.scope['user'],
                content = python_dic['msg'],
            )
            await database_sync_to_async(chat.save)()

            ## username msg এর সাথে fontend এ show করানোর জন্যে একটি variable এ store করা হয়েছে
            python_dic['user'] = self.scope['user'].username

            await self.channel_layer.group_send(
                self.groupName,{
                    'type': 'chat.message',   # Chat Message Hendler টি নিচে Creat করা হয়েছে
                    'message': json.dumps(python_dic),
                }
            )
        else:
            await self.send(text_data= json.dumps({
                "msg": "Login Required", 
                "user": "unknown",
                })
                )
    
    ## Chat Message Event Hendler টি Create করার জন্যে . এর যায় গায় শুধু _ দিতে হবে chat.message কে chat_message লিখতে হবে।
    async def chat_message(self, event):  
        # print('Event....', event)
        # print('Data', event['message']) # Data type is string 

        # এখন আমাদের এই data টি কে Text area তে দেখাতে চাইলে তা Send করতে হবে
        await self.send(text_data= json.dumps({
            'msg':event['message']
        }))



    async def disconnect(self, close_code):
        print("Disconnect...........", close_code)
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)

        ## NOTE Add a channel to a new or existing group
        await self.channel_layer.group_discard(
            self.groupName,   # Group Name
            self.channel_name
        )
        # raise StopConsumer()