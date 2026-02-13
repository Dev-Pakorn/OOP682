# SRP = Single Responsibility Principle

#Bad Idea
class ReportGenerator:
    def __init__(self, data):
        self.data = data
    def generate_report(self):
        pass
    def save_to_file(self, filename):
        pass
    def send_via_email(self, email_address):
        pass

