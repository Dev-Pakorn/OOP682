from models.person import Person

class Student(Person):
    def __init__(self, pid, name, age, student_id):
        super().__init__(pid, name, age, student_id)
        self.student_id = student_id

        
    def __str__(self):
        return f"Student : [{self.pid} , {self.student_id} , {self.name} , {self.age}]"