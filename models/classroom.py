class ClassRoom:
    def __init__(self, name):
        self.students = []
        self.name = name
    
    def add_student(self, student):
        self.students.append(student)
    
    def __len__(self):
        return len(self.students)
    
    def __getitem__(self, index):
        return self.students[index]
    