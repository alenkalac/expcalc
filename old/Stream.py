class Stream:
    id = 0
    opcode = 0
    data = ""

    def __init__(self, id):
        self.id = id

    def append_data(self, data):
        self.data = self.data + data

    def get_data(self):
        return self.data