
class Logger:
    def __init__(self, file_name: str):
        self.file_name = file_name

        with open(self.file_name, 'w') as file:
            file.write("")

    

    def log(self, text: str):
        with open(self.file_name, 'a') as file:
            file.write(text)


