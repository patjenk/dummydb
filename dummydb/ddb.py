from .serializer import dumps, loads

class DummyDBException(Exception):
    pass


class DummyDB():
    data = None

    def __init__(self, filename=None):
        if filename is not None:
            self.data = self.load_from_disk(filename)
        else:
            self.data = {}

    def load_from_disk(self, filename):
        filehandle = open(filename, "r")
        self.load_from_filehandle(filehandle)
        filehandle.close()

    def load_from_filehandle(self, filehandle):
        filehandle.seek(0)
        self.data = loads(filehandle.read())

    def write_to_disk(self, filename):
        filehandle = open(filename, "w")
        self.write_to_filehandle(filehandle)
        filehandle.close()

    def write_to_filehandle(self, filehandle):
        filehandle.write(dumps(self.data))

    def create_table(self, table_name, columns):
        """
        Create an empty table.
        """
        if table_name in self.data:
            raise DummyDBException("Table named '{}' already exists.".format(table_name))
        self.data[table_name] = {
            'definitions': columns,
            'data': [],
        }

    def insert(self, table_name, **kwargs):
        """
        Add data to a table.
        """
        if table_name not in self.data:
            raise DummyDBException("Table '{}' does not exist.".format(table_name))

        for key, val in self.data[table_name]['definitions'].items():
            if key not in kwargs:
                raise DummyDBException("Cannot insert into table '{}' without column {}.".format(table_name), key)
            if not isinstance(kwargs[key], val):
                raise DummyDBException("Table '{}' column {} requires type {}, not type {}.".format(table_name), key, val, type(kwargs[key]))

        self.data[table_name]['data'].append(kwargs)


    def select(self, table_name, **kwargs):
        """
        Get data from a table. Returns a list of dicts.
        """
        if table_name not in self.data:
            raise DummyDBException("Table '{}' does not exist.".format(table_name))
        for key, val in kwargs.items():
            if key not in self.data[table_name]['definitions']:
                raise DummyDBException("Table '{}' does not have a column '{}'.".format(table_name, key))

            if not isinstance(val, self.data[table_name]['definitions'][key]):
                raise DummyDBException("Table '{}' column is type {}, not type {}".format(table_name, self.data[table_name]['definitions'][key], type(val)))

        result = []
        for row in self.data[table_name]['data']:
            all_match = True
            for key, val in kwargs.items():
                if row[key] != val:
                    all_match = False
                    break
            if all_match:
                result.append(row)
        return result
