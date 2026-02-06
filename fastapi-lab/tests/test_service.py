from app.services import TaskService
from app.repositories import InMemoryTaskRepository
from app.models import TaskCreate

def test_create_task():
    # Arrange
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    task_data = TaskCreate(title="Test Task")

    # Act
    created_task = service.create_task(task_data)

    # Assert
    assert created_task.title == "Test Task"
    assert created_task.id == 1
    assert len(repo.get_all()) == 1