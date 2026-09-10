from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="To-Do App")
templates = Jinja2Templates(directory="templates")

# In-memory todo list only
todos = [
    {"id": 1, "text": "아침 운동하기", "done": False},
    {"id": 2, "text": "업무 메일 확인", "done": True},
    {"id": 3, "text": "오늘 계획 정리", "done": False},
]


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})


@app.post("/add")
async def add_todo(text: str = Form(...)):
    clean_text = text.strip()
    if clean_text:
        todos.append({"id": len(todos) + 1, "text": clean_text, "done": False})
    return RedirectResponse(url="/", status_code=303)


@app.post("/toggle/{todo_id}")
async def toggle_todo(todo_id: int):
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = not todo["done"]
            break
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{todo_id}")
async def delete_todo(todo_id: int):
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            del todos[index]
            break
    return RedirectResponse(url="/", status_code=303)
