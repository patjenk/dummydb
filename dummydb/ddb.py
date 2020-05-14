from json import loads


class DummyDB():
    filehandle = None
    data = None
    dirty = None

    def __init__(self, filename=None):
        if filename is not None:
            self.filehandle = open(filename, "r")
            self.data = self.load_from_disk()

    def load_from_disk(self):
        self.filehandle.seek(0)
        self.data = json.loads(self.filehandle.read())
        self.dirty = False
