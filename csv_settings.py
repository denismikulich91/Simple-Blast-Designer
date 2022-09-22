class CsvDataHandler:

    def __init__(self, file_path):
        self.__allStringCoords = dict()
        self.file_path = file_path

    def import_csv_data(self, x_coord_index: int, y_coord_index: int, id_field_index=0) -> None:
        """Imports from raw csv x, y coordinates and data ID, creates dict where ID used as a key and
        list of lists of floats (x, y) as values"""
        with open(self.file_path, encoding="utf-8") as csv_file_data:
            csv_file_data_list = csv_file_data.readlines()
        for line in csv_file_data_list[1:]:
            if line[id_field_index] not in self.__allStringCoords.keys():
                self.__allStringCoords[line[id_field_index]] = [[float(line.split(', ')[x_coord_index]), float(line.split(', ')[y_coord_index])]]
            else:
                self.__allStringCoords[line[id_field_index]].append([float(line.split(', ')[x_coord_index]), float(line.split(', ')[y_coord_index])])

    @property
    def get_csv_file_fields(self) -> list[str]:
        """Returns first line of CSV file as a list"""
        with open(self.file_path, encoding="utf-8") as csv_file_data:
            csv_file_fields = csv_file_data.readline()
        return csv_file_fields.split(', ')

    def get_data(self, data_id=None) -> list[list[float, float]] | str:
        """Returns a dictionary with chosen ID if no ID provided, returns full import dictionary
        returns None and 'does not exist' message if ID not found"""
        if data_id is None:
            connected_list = []
            for data_i in self.__allStringCoords.values():
                for data_j in data_i:
                    connected_list.append(data_j)
            return connected_list
        else:
            return self.__allStringCoords.get(data_id, "ID does not exist")


if __name__ == "__main__":
    csv_file = CsvDataHandler(r'Source\lines_from_csv.csv')
    csv_file.import_csv_data(2, 3, 0)
    string_five = csv_file.get_data('5')
    print(string_five)

