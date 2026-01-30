class Dog:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def info(self):
        print(f"{self.name} is {self.age} years old.")

    def __str__(self):
        return f"{self.name} is {self.age} years old."

def main():
    my_dog = Dog("Buddy",3)
    your_dog = Dog("Paulie",5)
    print(my_dog)
    print(your_dog)

if __name__ == "__main__":
    main()
