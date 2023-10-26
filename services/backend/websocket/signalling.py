from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect
import asyncio
import json

route = APIRouter()

# Map from topic-name to set of subscribed clients
topics = {}

async def send(websocket, message):
    try:
        await websocket.send_json(message)
    except WebSocketDisconnect:
        pass

async def on_connect(websocket: WebSocket):
    await websocket.accept()
    subscribed_topics = set()
    closed = False
    pong_received = True
    ping_interval = None

    try:
        async for message in websocket.iter_text():
            message = json.loads(message)
            if message and message.get("type") and not closed:
                message_type = message["type"]
                if message_type == "subscribe":
                    for topic_name in message.get("topics", []):
                        if isinstance(topic_name, str):
                            topic = topics.setdefault(topic_name, set())
                            topic.add(websocket)
                            subscribed_topics.add(topic_name)
                elif message_type == "unsubscribe":
                    for topic_name in message.get("topics", []):
                        subs = topics.get(topic_name)
                        if subs:
                            subs.discard(websocket)
                elif message_type == "publish" and "topic" in message:
                    receivers = topics.get(message["topic"])
                    if receivers:
                        message["clients"] = len(receivers)
                        await asyncio.gather(*[send(receiver, message) for receiver in receivers])
                elif message_type == "ping":
                    await send(websocket, {"type": "pong"})
    except WebSocketDisconnect:
        pass
    except Exception as exc:
        print("Connection Closed!!!")
    finally:
        for topic_name in subscribed_topics:
            subs = topics.get(topic_name)
            if subs:
                subs.discard(websocket)
                if not subs:
                    del topics[topic_name]
        closed = True
        if ping_interval:
            ping_interval.cancel()


@route.websocket("/signal")
async def websocket_endpoint(websocket: WebSocket):
    await on_connect(websocket)