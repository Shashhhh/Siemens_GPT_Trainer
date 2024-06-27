from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import json
from openai import AsyncOpenAI
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
class Handler(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.assistant_id = "asst_Mn4aCCQPzF5dJJD80Paq5uRU"
        self.thread = await self.client.beta.threads.create()

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        user_input = text_data.strip()
        message = await self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content= user_input
                )
        stream = await self.client.beta.threads.runs.create(
                assistant_id="asst_Mn4aCCQPzF5dJJD80Paq5uRU",
                thread_id=self.thread.id,
                stream=True
                )
        async for chunk in stream:
            if isinstance(chunk, ThreadMessageDelta):
                await self.send(text_data=json.dumps({'delta': chunk.data.delta.content[0].text.value}))
