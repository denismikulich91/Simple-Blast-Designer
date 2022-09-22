class CsvDataHandler:
    """Consists of functions for import and farther handling csv data"""

    def __init__(self, file_path, id_field, data_id):
        self.__allStringCoords = dict()
        self.file_path = file_path
        self.data_id = data_id
        if id_field in self.get_csv_file_fields:
            self.id_field_index = self.get_csv_file_fields.index(id_field)
        else:
            self.id_field_index = None
            self.data_id = None

    def import_csv_data(self, x_coord_field: str, y_coord_field: str) -> None:
        """Imports from raw csv x, y coordinates and data ID, creates dict where ID used as a key and
        list of lists of floats (x, y) as values"""
        try:
            x_coord_index = self.get_csv_file_fields.index(x_coord_field)
            y_coord_index = self.get_csv_file_fields.index(y_coord_field)
        except ValueError:
            raise ValueError(f'There is no such field {x_coord_field} or {y_coord_field}')

        with open(self.file_path, encoding="utf-8") as csv_file_data:
            csv_file_data_list = csv_file_data.readlines()
        if self.id_field_index is not None:
            for line in csv_file_data_list[1:]:
                if line[self.id_field_index] not in self.__allStringCoords.keys():
                    self.__allStringCoords[line[self.id_field_index]] = [[float(line.split(', ')[x_coord_index]), float(line.split(', ')[y_coord_index])]]
                else:
                    self.__allStringCoords[line[self.id_field_index]].append([float(line.split(', ')[x_coord_index]), float(line.split(', ')[y_coord_index])])
        else:
            temp_list = []
            for line in csv_file_data_list[1:]:
                temp_list.append([float(line.split(', ')[x_coord_index]), float(line.split(', ')[y_coord_index])])
            self.__allStringCoords[999] = temp_list

    @property
    def get_csv_file_fields(self) -> list[str]:
        """Returns first line of CSV file as a list"""
        with open(self.file_path, encoding="utf-8") as csv_file_data:
            csv_file_fields = csv_file_data.readline()
        return csv_file_fields.split(', ')

    def get_data(self) -> list[list[float, float]] | list[list[list[float, float]]]:
        """Returns a dictionary with chosen ID if no ID provided, returns full import dictionary
        returns None and 'does not exist' message if ID not found"""
        if self.data_id is None and self.id_field_index is None:
            connected_list = []
            for data_i in self.__allStringCoords.values():
                for data_j in data_i:
                    connected_list.append(data_j)
            return connected_list
        elif self.data_id is None and self.id_field_index is not None:
            return list(self.__allStringCoords.values())
        else:
            return self.__allStringCoords.get(self.data_id, "ID does not exist")


if __name__ == "__main__":
    csv_file = CsvDataHandler(r'Source\lines_from_csv.csv', None, None)
    csv_file.import_csv_data('x', 'y')
    string_five = csv_file.get_data()
    print(string_five)


# TODO add a dpg.drawline function for this class