import dearpygui.dearpygui as dpg
import SurPy
from gui_settings import Settings


class ImportSettings:
    def __init__(self, label, tag, optional_widgets):
        self.sketch_color = [255, 255, 255]
        self.sketch_line_type = 'Solid'
        self.sketch_line_width = 1
        self.sketchCoordinates = [[10, 40], [25, 60], [100, 80], [200, 30], [150, 15], [10, 40]]
        self.label = label
        self.tag = tag
        self.optional_widgets = optional_widgets
        if optional_widgets:
            with dpg.file_dialog(directory_selector=False, tag="file_dialog_id", show=False,
                                 callback=AppButtons.get_file_name, height=300, modal=True):
                dpg.add_file_extension(".str", color=(0, 255, 255, 255))
                dpg.add_file_extension(".sdm", color=(0, 255, 255, 255))

            with dpg.window(label=self.label, width=500, height=-1, pos=(300, 300), tag=self.tag):
                with dpg.group():
                    with dpg.group(horizontal=True):
                        dpg.add_input_text(width=300, default_value='', tag='file_name_input')
                        dpg.add_button(callback=lambda: dpg.show_item("file_dialog_id"), label='Choose file', width=-1)
                    with dpg.group(horizontal=True):
                        dpg.add_input_text(width=300, tag='string_number')
                        dpg.add_text('Enter string number')
                    with dpg.group(horizontal=True):
                        dpg.add_input_text(width=300)
                        dpg.add_text('Enter segment number')

                    with dpg.group(horizontal=True):
                        dpg.add_slider_int(min_value=1, max_value=10, width=300, callback=self.update_sketch_polygon,
                                           tag='string_width_slider')
                        dpg.add_text('Choose line width')
                    with dpg.group(horizontal=True):
                        with dpg.group():
                            dpg.add_radio_button(items=['Solid', 'Dashed', 'Dotted', 'DashDotted'], horizontal=False,
                                                 tag='sketch_line_type', default_value='Solid')
                        dpg.add_color_picker(no_small_preview=True, no_inputs=True, no_side_preview=True, width=150,
                                             display_rgb=True, tag='color_picker', callback=self.update_sketch_polygon)
                        with dpg.group():
                            with dpg.drawlist(width=300, height=100, tag='sketch_list'):
                                dpg.draw_polygon(self.sketchCoordinates, color=self.sketch_color,
                                                 thickness=self.sketch_line_width, tag='sketch_polygon')
                                dpg.draw_text([150, 80], 'sketch', size=20)

                    with dpg.group():
                        with dpg.group(horizontal=True):
                            with dpg.group():
                                dpg.add_text('Color: ')
                                dpg.add_text('Line style: ')
                                dpg.add_text('Line width: ')

                        with dpg.group(horizontal=True):
                            dpg.add_button(label='Default values', width=240)
                            dpg.add_button(label='Save as default', width=-1)
                        with dpg.group(horizontal=True):
                            dpg.add_button(label='OK', width=240, callback=AppButtons.get_surpac_import_data)
                            dpg.add_button(label='Cancel', width=-1)

    def update_sketch_polygon(self):
        dpg.delete_item('sketch_polygon')
        dpg.draw_polygon(self.sketchCoordinates, color=self.sketch_color, thickness=self.sketch_line_width,
                         parent='sketch_list', tag='sketch_polygon')
        self.sketch_color = dpg.get_value('color_picker')
        self.sketch_line_type = dpg.get_value('sketch_line_type')
        self.sketch_line_width = dpg.get_value('string_width_slider')


class ImportSettingsCSV(ImportSettings):
    def __init__(self, label, tag, optional_widgets):
        super().__init__(label, tag, optional_widgets)
        with dpg.file_dialog(directory_selector=False, tag="file_dialog_id", show=False,
                             callback=AppButtons.get_file_name, height=300, modal=True):
            dpg.add_file_extension(".csv", color=(0, 255, 255, 255))
        with dpg.window(label=self.label, width=500, height=-1, pos=(300, 300), tag=self.tag):
            with dpg.group(parent=self.tag, before='string_width_slider'):
                with dpg.group(horizontal=True):
                    dpg.add_input_text(width=300, default_value='', tag='file_name_input')
                    dpg.add_button(callback=lambda: dpg.show_item("file_dialog_id"), label='Choose file', width=-1)
                with dpg.group(horizontal=True):
                    dpg.add_input_text(width=150, tag='string_number')
                    dpg.add_text('Choose field for string number')
                with dpg.group(horizontal=True):
                    dpg.add_input_text(width=150)
                    dpg.add_text('Choose field for segment number')
                with dpg.group(horizontal=True):
                    dpg.add_input_text(width=150)
                    dpg.add_text('X coordinate')
                with dpg.group(horizontal=True):
                    dpg.add_input_text(width=150)
                    dpg.add_text('Y coordinate')


class AppButtons:
    def __init__(self, label):
        self.id = dpg.add_button(label=label)

    def set_callback(self, callback):
        dpg.set_item_callback(self.id, callback)

    @staticmethod
    def import_from_surpac():
        ImportSettings('Import from Surpac', 'surpac_import_window', True)

    @staticmethod
    def import_from_csv():
        ImportSettingsCSV('Import from CSV', 'csv_import_window', False)

    @staticmethod
    def get_file_name(sender, app_data):
        dpg.configure_item('file_name_input', default_value=app_data['file_path_name'])
        with open(app_data['file_path_name'], encoding="utf-8") as csvFile:
            csvFileDataList = csvFile.readlines()
        for line in csvFileDataList:
            print(line)

    @classmethod
    def get_surpac_import_data(cls, user_data=False):
        imported_data = SurPy.SurpacDataHandler()
        imported_data.read_str_file(dpg.get_value('file_name_input'), dpg.get_value('string_number'))
        imported_data.get_line_coordinates()
        imported_data.print_all_string_coordinates()
        cleared_imported_string = imported_data.get_2d_coords_for_single_sting(int(dpg.get_value('string_number')))
        # TODO set up a multi-string import. In case number is '' it should iterate and draw all strings

        SurPy.SurpacDataHandler.drawing_depending_on_string_type(
                cleared_imported_string, dpg.get_value('color_picker'), float(dpg.get_value('string_width_slider')))
        dpg.delete_item('file_dialog_id')
        dpg.delete_item('surpac_import_window')









