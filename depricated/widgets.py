import dearpygui.dearpygui as dpg
import str_settings
from csv_settings import CsvDataHandler


class ImportSettings:
    def __init__(self, label, tag):
        self.sketch_color = [255, 255, 255]
        self.sketch_line_type = 'Solid'
        self.sketch_line_width = 1
        self.sketchCoordinates = [[10, 40], [25, 60], [100, 80], [180, 30], [150, 15], [10, 40]]
        self.label = label
        self.tag = tag

    @staticmethod
    def create_file_dialog(data_type):
        with dpg.file_dialog(directory_selector=False, tag="file_dialog_id", show=False,
                             callback=AppButtons.get_file_name, user_data=data_type, height=300, modal=True):
            if data_type == 'surpac':
                dpg.add_file_extension(".str", color=(0, 255, 255, 255))
                dpg.add_file_extension(".sdm", color=(0, 255, 255, 255))
            elif data_type == 'csv':
                dpg.add_file_extension(".csv", color=(0, 255, 255, 255))

    def add_specific_data_to_window(self):
        with dpg.group(parent=self.tag, before='group'):
            with dpg.group(horizontal=True):
                dpg.add_input_text(width=300, default_value='', tag='file_name_input')
                dpg.add_button(callback=lambda: dpg.show_item("file_dialog_id"), label='Choose file', width=-1)
            with dpg.group(horizontal=True):
                dpg.add_input_text(width=300, tag='string_number', default_value='')
                dpg.add_text('Enter string number')

    def create_main_import_window(self, function_on_ok):
        with dpg.window(label=self.label, width=500, height=-1, pos=(400, 150), tag=self.tag):
            with dpg.group(horizontal=True, tag='group'):
                dpg.add_slider_int(min_value=1, max_value=10, width=300, callback=self.update_sketch_polygon,
                                   tag='string_width_slider')
                dpg.add_text('Choose line width')
            with dpg.group(horizontal=True):
                with dpg.group():
                    dpg.add_radio_button(items=['Solid', 'Dashed', 'Dotted', 'DashDotted'], horizontal=False,
                                         tag='sketch_line_type', default_value='Solid')
                dpg.add_color_picker(no_small_preview=True, no_inputs=True, no_side_preview=True, width=150,
                                     display_rgb=True, tag='color_picker', callback=self.update_sketch_polygon, default_value=[255, 255, 255])
                with dpg.group():
                    with dpg.drawlist(width=300, height=100, tag='sketch_list'):
                        dpg.draw_polygon(self.sketchCoordinates, color=self.sketch_color,
                                         thickness=self.sketch_line_width, tag='sketch_polygon')
                        dpg.draw_text([125, 70], 'sketch', size=20)

            with dpg.group():
                with dpg.group(horizontal=True):
                    dpg.add_button(label='Default values', width=240)
                    dpg.add_button(label='Save as default', width=-1)
                with dpg.group(horizontal=True):
                    dpg.add_button(label='OK', width=240, callback=function_on_ok)
                    dpg.add_button(label='Cancel', width=-1, callback=AppButtons.click_cancel, user_data=self.tag)

    def update_sketch_polygon(self):
        dpg.delete_item('sketch_polygon')
        dpg.draw_polygon(self.sketchCoordinates, color=self.sketch_color, thickness=self.sketch_line_width,
                         parent='sketch_list', tag='sketch_polygon')
        self.sketch_color = dpg.get_value('color_picker')
        self.sketch_line_type = dpg.get_value('sketch_line_type')
        self.sketch_line_width = dpg.get_value('string_width_slider')


class ImportSettingsCSV(ImportSettings):
    def __init__(self, label, tag):
        super().__init__(label, tag)

    def add_specific_data_to_window(self):
        with dpg.group(parent=self.tag, before='group'):
            with dpg.group(horizontal=True):
                dpg.add_input_text(width=300, tag='file_name_input')
                dpg.add_button(callback=lambda: dpg.show_item("file_dialog_id"), label='Choose file', width=-1)
            with dpg.group(horizontal=True):
                dpg.add_combo(['Choose file first'], width=230, tag='csv_string_column')
                dpg.add_input_text(width=55, tag='csv_string_number')
                dpg.add_text('Line ID name')
            with dpg.group(horizontal=True):
                dpg.add_combo(['Choose file first'], width=300, tag='csv_x_field')
                dpg.add_text('X coordinate')
            with dpg.group(horizontal=True):
                dpg.add_combo(['Choose file first'], width=300, tag='csv_y_field')
                dpg.add_text('Y Coordinate')


class AppButtons:
    def __init__(self, label):
        self.id = dpg.add_button(label=label)

    def set_callback(self, callback):
        dpg.set_item_callback(self.id, callback)

    @staticmethod
    def import_from_surpac():
        surpac_import_window = ImportSettings('Import from Surpac', 'surpac_import_window')
        ImportSettings.create_file_dialog('surpac')
        surpac_import_window.create_main_import_window(AppButtons.get_surpac_import_data)
        surpac_import_window.add_specific_data_to_window()

    @staticmethod
    def import_from_csv():
        csv_import_window = ImportSettingsCSV('Import from CSV', 'csv_import_window')
        ImportSettings.create_file_dialog('csv')
        csv_import_window.create_main_import_window(AppButtons.get_csv_import_data)
        csv_import_window.add_specific_data_to_window()

    @staticmethod
    def click_cancel(sender, app_data, user_data):
        dpg.delete_item(user_data)
        dpg.delete_item('file_dialog_id')

    @staticmethod
    def get_file_name(sender, app_data, user_data):
        dpg.configure_item('file_name_input', default_value=app_data['file_path_name'])
        if user_data == 'csv':
            with open(app_data['file_path_name'], encoding="utf-8") as importedFile:
                FileDataList = importedFile.readlines()
            csv_header_list = FileDataList[0].split(', ')
            for tag in ['csv_string_column', 'csv_x_field', 'csv_y_field']:
                dpg.configure_item(tag, items=csv_header_list)

    @classmethod
    def get_surpac_import_data(cls):
        imported_data = str_settings.SurpacDataHandler()
        imported_data.read_str_file(dpg.get_value('file_name_input'), dpg.get_value('string_number'))
        imported_data.get_line_coordinates()
        # imported_data.print_all_string_coordinates()
        cleared_imported_string = imported_data.get_2d_coords_for_single_sting(dpg.get_value('string_number'))

        if dpg.get_value('string_number') == '':
            for str_string in cleared_imported_string:
                str_settings.SurpacDataHandler.drawing_depending_on_string_type(str_string,
                    dpg.get_value('color_picker'), float(dpg.get_value('string_width_slider')))
        elif dpg.get_value('string_number').isdigit():
            str_settings.SurpacDataHandler.drawing_depending_on_string_type(cleared_imported_string,
                                                                     dpg.get_value('color_picker'),
                                                                     float(dpg.get_value('string_width_slider')))

        dpg.delete_item('file_dialog_id')
        dpg.delete_item('surpac_import_window')

    @classmethod
    def get_csv_import_data(cls):
        imported_csv_data = CsvDataHandler(dpg.get_value('file_name_input'),
                                           dpg.get_value('csv_string_column'),
                                           dpg.get_value('csv_string_number'))

        imported_csv_data.import_csv_data(dpg.get_value('csv_x_field'),
                                          dpg.get_value('csv_y_field'))

        imported_csv_data.prepare_data_to_draw_in_canvas(dpg.draw_polyline,
                                                         dpg.get_value('color_picker'),
                                                         float(dpg.get_value('string_width_slider')),
                                                         'base_layer')
        dpg.delete_item('file_dialog_id')
        dpg.delete_item('csv_import_window')










