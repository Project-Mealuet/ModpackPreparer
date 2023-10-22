class McOptions:
    def __init__(self):
        self._data_dict = {}

    def __getitem__(self, item):
        return self._data_dict[item]

    def __setitem__(self, key, value):
        self._data_dict[key] = value

    def load(
            self,
            file_path: str
    ):
        with open(file_path, 'r') as file:
            file_lines = file.readlines()
        for file_line in file_lines:
            data_pair = file_line.strip().split(':', 1)
            if len(data_pair) == 2:
                self._data_dict[data_pair[0]] = data_pair[1]

    def save(
            self,
            file_path: str
    ):
        with open(file_path, 'w') as file:
            for key in self._data_dict:
                file.write(f'{key}:{self._data_dict[key]}\n')
