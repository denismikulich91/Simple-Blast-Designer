from shapely.geometry import LineString


class LinesAndPoints:
    """This class used to organize lines and points data.
    It has a dictionary which is populated by specific functions.
    It helps to add, delete and change any set of point or line data, also
    provides methods to calculate basic attributes e.g. Area or Length"""
    def __init__(self):
        self.lines_dict = dict()
        self.points_dict = dict()
        self.object_id = 0

    @property
    def get_unique_id(self):
        """Creates an object ID every time rising it by 1"""
        self.object_id += 1
        return self.object_id
    
    @staticmethod
    def get_2d_length(coordinates: list) -> float:
        # LineString is a Shapely object
        line = LineString(coordinates)
        return line.length
    
    @staticmethod
    def get_2d_area(coordinates: list) -> float:
        line = LineString(coordinates)
        return line.area

    def _add_new_line(self, coordinates, color, style, width, layer):
        """Used in outer functions, passing all attributes needed
        to create a new item in lines_dict"""
        self.object_id = self.get_unique_id
        self.lines_dict[self.object_id] = {}
        self.lines_dict[self.object_id]['coordinates'] = coordinates
        self.lines_dict[self.object_id]['color'] = color
        self.lines_dict[self.object_id]['style'] = style
        self.lines_dict[self.object_id]['width'] = width
        self.lines_dict[self.object_id]['layer'] = layer
        self.lines_dict[self.object_id]['2d_length'] = self.get_2d_length(coordinates)
        self.lines_dict[self.object_id]['closed'] = True if coordinates[0] == coordinates[-1] else False
        self.lines_dict[self.object_id]['area'] = self.get_2d_area(coordinates) if self.lines_dict[self.object_id]['closed'] else 0
        self.lines_dict[self.object_id]['comment'] = ''

    def add_new_line(self, is_multi: bool, coordinates: list | tuple, color: tuple, style: str, width: int, layer: str) -> None:
        """ Does an _add_new_line function but depending on if it is a nested
        list, runs function twice"""
        if is_multi:
            for line in coordinates:
                self._add_new_line(line, color, style, width, layer)
        else:
            self._add_new_line(coordinates, color, style, width, layer)


    def close_line(self, object_id: int):
        """Creates one more point with coordinates same as first point's"""
        self.lines_dict[object_id]['coordinates'].append(self.lines_dict[object_id]['coordinates'][0])

    def change_coordinates(self, object_id, coordinates):
        self.lines_dict[object_id]['coordinates'] = coordinates

    def change_line_color(self, object_id, new_color):
        self.lines_dict[object_id]['color'] = new_color

    def change_line_style(self, object_id, new_style):
        self.lines_dict[object_id]['style'] = new_style

    def change_line_width(self, object_id, new_width):
        self.lines_dict[object_id]['style'] = new_width

    def clear_all(self):
        self.lines_dict = {}

    def get_coordinates(self, object_id):
        return self.lines_dict[object_id]['coordinates']

    def get_color(self, object_id):
        return self.lines_dict[object_id]['color']

    def get_width(self, object_id):
        return self.lines_dict[object_id]['width']

    def get_style(self, object_id):
        return self.lines_dict[object_id]['style']

    def get_info(self, object_id=0):
        print(f'Line {object_id} has {self.get_color(object_id)} color, '
              f'{self.get_style(object_id)} style, {self.get_width(object_id)}, \n'
              f'coordinates are: {self.get_coordinates(object_id)}')
        