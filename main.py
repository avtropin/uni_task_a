from time import sleep

from redis import Redis
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from backtasks import processing_request
from my_html import my_html

tasks_list = []  # имитация хранения списка ключей запросов на стороне клиента

app = FastAPI(
    title="uni_task_a"
)


@app.get("/send_message")
def user_send_message(data):
    response = processing_request.delay(data)
    tasks_list.append(response.id)
    return HTMLResponse(my_html)


"""@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    id = tasks_list.pop()
    if id is None:
        await websocket.send_text("Нет данных")
    else:
        sym = ""
        r = Redis("uni_redis", 6379)
        while sym != "$":
            sleep(0.5)
            data = r.get((r.keys(pattern=f"*{id}*"))[0])
            sym = f"{data}"[-2]
            if sym != "$":
                await websocket.send_text(f"{data}")"""


"""@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    id = tasks_list.pop()
    if id is None:
        await websocket.send_text("Нет данных")
    else:
        sym = ""
        r = Redis("uni_redis", 6379)
        w = r.pubsub()
        w.subscribe(id)
        while sym != "$":
            message = w.get_message()
            sleep(0.5)
            if message is not None and len(f"{message['data']}") > 2:
                sym = f"{message['data']}"[-2]
                if sym != "$":
                    await websocket.send_text(f"{message['data']}"[2:-1])"""


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    id = tasks_list.pop()
    if id is None:
        await websocket.send_text("Нет данных")
    else:
        sym = ""
        num = 0
        r = Redis("uni_redis", 6379)
        while sym != "$":
            message = r.xread(streams={id: 0})
            if r.xlen(id) > num:
                sym = f"{message[0][1][num][1][b'value']}"[-2]
                if sym != "$":
                    await websocket.send_text(
                        f"{message[0][1][num][1][b'value']}"[2:-1])
                    num += 1
            sleep(0.5)
