from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import models
from models import Todos
from typing import Annotated, Optional
from database import engine, SessionLocal
from router import auth

app = FastAPI()

# ---------------------------------------------------------
# Pydantic মডেল: নতুন Todo তৈরির জন্য
# id এখানে নেই, কারণ ডাটাবেস নিজে থেকে id জেনারেট করবে
# ---------------------------------------------------------
class TodoCreate(BaseModel):
    title: str
    description: str = Field(max_length=100)
    priority: int = Field(gt=0, lt=6)
    completed: bool = False


# ---------------------------------------------------------
# Pydantic মডেল: রেসপন্স হিসেবে ফেরত পাঠানোর জন্য (id সহ)
# from_attributes = True দিলে SQLAlchemy অবজেক্ট থেকে
# সরাসরি ডেটা কনভার্ট করা যায়
# ---------------------------------------------------------
class TodoOut(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    completed: bool

    class Config:
        from_attributes = True


# ---------------------------------------------------------
# Pydantic মডেল: Todo আপডেটের জন্য (সব ফিল্ড ঐচ্ছিক)
# ---------------------------------------------------------
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None, max_length=100)
    priority: Optional[int] = Field(default=None, gt=0, lt=6)
    completed: Optional[bool] = Field(default=None)


# ডাটাবেসে টেবিল না থাকলে তৈরি করে দেয়
models.Base.metadata.create_all(bind=engine)

# auth রাউটার যুক্ত করা হলো (লগইন/রেজিস্ট্রেশন ইত্যাদি)
app.include_router(auth.router)


# ---------------------------------------------------------
# প্রতিটা রিকোয়েস্টের জন্য আলাদা ডাটাবেস সেশন তৈরি করে,
# রিকোয়েস্ট শেষে সেশন বন্ধ করে দেয়
# ---------------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


# ---------------------------------------------------------
# সব Todo দেখা
# ---------------------------------------------------------
@app.get('/', response_model=list[TodoOut])
def read_todos(db: db_dependency):
    return db.query(Todos).all()


# ---------------------------------------------------------
# নির্দিষ্ট একটা Todo দেখা (id দিয়ে)
# ---------------------------------------------------------
@app.get('/todo/{todo_id}', response_model=TodoOut)
def read_specific_todo(db: db_dependency, todo_id: int):
    specific_todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if specific_todo is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    return specific_todo


# ---------------------------------------------------------
# নতুন Todo তৈরি করা
# ---------------------------------------------------------
@app.post('/create', status_code=201)
def create_todo(db: db_dependency, new_todo: TodoCreate):
    todo_model = Todos(**new_todo.model_dump())
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)  # নতুন id সহ আপডেটেড অবজেক্ট পাওয়ার জন্য

    return {'message': 'Todo created successfully', 'id': todo_model.id}


# ---------------------------------------------------------
# Todo আপডেট করা (আংশিক আপডেটও সম্ভব)
# ---------------------------------------------------------
@app.put('/edit/{todo_id}')
def update_todo(db: db_dependency, todo_id: int, update_todo: TodoUpdate):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    # exclude_unset=True -> শুধু যেসব ফিল্ড ইউজার পাঠিয়েছে সেগুলোই নেবে
    update_data = update_todo.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(todo, key, value)

    db.commit()
    return {'message': 'Todo updated successfully'}


# ---------------------------------------------------------
# Todo ডিলিট করা
# ---------------------------------------------------------
@app.delete('/delete/{todo_id}')
def delete_todo(db: db_dependency, todo_id: int):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo not found')

    db.delete(todo)  # আগে fetch করা অবজেক্ট সরাসরি delete করা হলো
    db.commit()
    return {'message': 'Todo deleted successfully'}