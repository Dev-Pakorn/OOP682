from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Task, TaskCreate
from sqlalchemy.orm import Session
from . import models_orm

class ITaskRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def create(self, task: TaskCreate) -> Task:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        pass

    # เพิ่มใหม่สำหรับ Challenge 1
    @abstractmethod
    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        pass

    # เพิ่มใหม่สำหรับ Challenge 2
    @abstractmethod
    def get_by_title(self, title: str) -> Optional[Task]:
        pass


class InMemoryTaskRepository(ITaskRepository):
    def __init__(self):
        self.tasks = []
        self.current_id = 1

    def get_all(self) -> List[Task]:
        return self.tasks

    def create(self, task_in: TaskCreate) -> Task:
        task = Task(id=self.current_id, **task_in.dict())
        self.tasks.append(task)
        self.current_id += 1
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if task:
            for key, value in kwargs.items():
                setattr(task, key, value)
        return task

    def get_by_title(self, title: str) -> Optional[Task]:
        for task in self.tasks:
            if task.title == title:
                return task
        return None


class SqlTaskRepository(ITaskRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(models_orm.TaskORM).all()

    def create(self, task_in: TaskCreate):
        db_task = models_orm.TaskORM(**task_in.model_dump())
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)
        return db_task

    def get_by_id(self, id: int):
        return self.db.query(models_orm.TaskORM).filter(models_orm.TaskORM.id == id).first()

    def update(self, task_id: int, **kwargs):
        db_task = self.get_by_id(task_id)
        if db_task:
            for key, value in kwargs.items():
                setattr(db_task, key, value)
            self.db.commit()
            self.db.refresh(db_task)
        return db_task

    def get_by_title(self, title: str):
        return self.db.query(models_orm.TaskORM).filter(models_orm.TaskORM.title == title).first()