from redis import Redis
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from backtasks import processing_request, CELERY_RESPONSE
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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    id = tasks_list.pop()
    if id is None:
        await websocket.send_text("Нет данных")
    else:
        r = Redis("uni_redis", 6379)
        for sym in CELERY_RESPONSE:
            if r.set(id, sym):
                data = r.get((r.keys(pattern=f"*{id}*"))[0])
                await websocket.send_text(f"{data}")
