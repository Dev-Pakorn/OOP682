from fastapi import HTTPException  # นำเข้าเพื่อใช้ Raise Exception ตามโจทย์
from .repositories import ITaskRepository
from .models import TaskCreate

class TaskService:
    def __init__(self, repo: ITaskRepository):
        self.repo = repo

    def get_tasks(self):
        return self.repo.get_all()

    def create_task(self, task_in: TaskCreate):
        existing_task = self.repo.get_by_title(task_in.title)
        if existing_task:
            raise HTTPException(status_code=400, detail="Task title already exists")
        
        return self.repo.create(task_in)
    
    def mark_as_complete(self, task_id: int):
        task = self.repo.update(task_id, completed=True)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task