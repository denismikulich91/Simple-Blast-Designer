class CsvDataHandler:
    """Consists of functions for import and farther handling of the csv data"""

    def __init__(self, file_path, id_field, data_id):
        self.__allStringCoords = dict()
        self.file_path = file_path
        if id_field in self.get_csv_file_fields:
            self.id_field_index = self.get_csv_file_fields.index(id_field)
            self.data_id = data_id if data_id != '' else None
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
            raise CsvParamError

        with open(self.file_path, encoding="utf-8") as csv_file_data:
            csv_file_data_list = csv_file_data.readlines()
        if self.id_field_index is not None:
            for line in csv_file_data_list[1:]:
                if line[self.id_field_index] not in self.__allStringCoords.keys():
                    self.__allStringCoords[line[self.id_field_index]] = [[float(line.split(', ')[x_coord_index]),
                                                                          float(line.split(', ')[y_coord_index])]]
                else:
                    self.__allStringCoords[line[self.id_field_index]].append([float(line.split(', ')[x_coord_index]),
                                                                              float(line.split(', ')[y_coord_index])])
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

    @property
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
            return self.__allStringCoords[self.data_id]

    def prepare_data_to_draw_in_canvas(self, draw_func, par_1, par_2, layer):
        if self.data_id is None and self.id_field_index is not None:
            for data in self.get_data:
                draw_func(data, color=par_1, thickness=par_2, parent=layer)
        else:
            draw_func(self.get_data, color=par_1, thickness=par_2, parent=layer)


class CsvParamError(Exception):
    def __str__(self):
        return 'X or Y import fields are empty!'


if __name__ == "__main__":
    csv_file = CsvDataHandler(r'Source\lines_from_csv.csv', 'string', '6')
    csv_file.import_csv_data('', 'y')

