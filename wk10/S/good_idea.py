# SRP = Single Responsibility Principle

# Good Idea 
class PDFReportGenerator:
    def __init__(self, data):
        self.data = data

    def generate_report(self):
        pass

class ExcelReportGenerator:
    def __init__(self, data):
        self.data = data

    def generate_report(self):
        pass

class EmailSender:
    def __init__(self, recipient):
        self.recipient = recipient

    def send(self, content):
        pass