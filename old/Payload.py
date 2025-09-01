
class Payload:
    pos = 0
    payload = ""

    def __init__(self, payload):
        self.payload = payload

    def read_byte(self):
        try:
            d = self.payload[self.pos:self.get_and_update_pos(1)]
            return d
        except ValueError:
            return -1

    def read_short(self):
        d = self.payload[self.pos:self.get_and_update_pos(4)]
        return d

    def skip(self, by_bytes):
        d = self.payload[self.pos:self.get_and_update_pos(by_bytes)]
        return d

    def read_string_to_end(self):
        d_str = self.payload[self.pos:]
        self.pos = len(self.payload)
        return d_str

    def get_and_update_pos(self, by):
        if self.pos+by > len(self.payload):
            raise ValueError("Invalid Value - trying to read from " , self.pos, " by ", by, " but length is ", len(self.payload))
        self.pos = self.pos+by
        return self.pos

    def size(self):
        return len(self.payload)