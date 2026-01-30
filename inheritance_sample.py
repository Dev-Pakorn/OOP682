from models.person import Person
from models.staff import Staff
from models.student import Student

person = Person(1234567890123, "John Doe",30)
student = Student(1234567890123,"Alice",20,"S123")
staff = Staff(2345678901234,"Bob",35,"ST456")
print(person)
print(student)
print(staff)

def get_person_info(Person):
    print(isinstance(person,Person))
    return f"Name : {person.name},Age : {person.age}"

get_person_info(student)
get_person_info(staff)

class Employee:
    pass

manager = Employee()
get_person_info(manager)