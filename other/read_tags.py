class Read_tags:

    def __init__(self, filename):
        self.file = open(filename, "r", encoding="utf-8")

    def get_tags_list(self):
        return list(self.file.readlines())