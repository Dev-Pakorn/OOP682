#Bad Idea
#DIP = Dependency Inversion Principleq

class App:
    def __init__(self):
        self.db = MySQLDatabase()

class MySQLDatabase:
    def query(self):
        print("Querying MySQL Database")

app = App()
app.save_data("Some important Data")
