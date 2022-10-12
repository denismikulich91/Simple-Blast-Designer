import dearpygui.dearpygui as dpg
from math import *
from depricated.gui_settings import Settings
from depricated.widgets import AppButtons

dpg.create_context()


class Window:
    def __init__(self, label, base_layer):
        self._children = []
        self.axis_scale = 1
        self.translationCoordinates = [0, 0]
        self.color = [255, 255, 255]
        self.scale = dpg.create_scale_matrix([self.axis_scale, self.axis_scale, self.axis_scale])
        self.rotation = dpg.create_rotation_matrix(pi / 2, [0, 0, -1])
        self.translation = dpg.create_translation_matrix(self.translationCoordinates)
        self.dragging_initial_coordinates = [0, 0]
        self.dragging_final_coordinates = [0, 0]
        self.relative_coordinates = [0, 0]

        with dpg.window(tag='main_window', label="Tutorial"):
            with dpg.group(horizontal=True):
                import_surpac_button = AppButtons('Import from Surpac')
                import_surpac_button.set_callback(AppButtons.import_from_surpac)
                import_csv_button = AppButtons('Import from CSV')
                import_csv_button.set_callback(AppButtons.import_from_csv)
                draw_button = AppButtons('Draw a block')
                clear_canvas_button = AppButtons('Clear Canvas')
            with dpg.drawlist(width=1400, height=700):
                with dpg.draw_layer(tag="canvas"):
                    with dpg.draw_node(parent='canvas', tag='base_layer'):
                        pass

    def zoom(self, sender, app_data):
        if app_data == -1:
            self.axis_scale *= 0.9
        else:
            self.axis_scale *= 1.1
        self.update_canvas()

    def move(self, sender, app_data):
        self.update_canvas()
        self.translationCoordinates[0] = app_data[1] + self.relative_coordinates[0]
        self.translationCoordinates[1] = app_data[2] + self.relative_coordinates[1]

    def update_canvas(self):
        self.scale = dpg.create_scale_matrix([my_window.axis_scale, my_window.axis_scale, my_window.axis_scale])
        self.translation = dpg.create_translation_matrix(my_window.translationCoordinates)
        dpg.apply_transform("base_layer", self.translation * self.scale * self.rotation)

    def restore_screen_view(self):
        self.relative_coordinates = [0, 0]
        self.axis_scale = 1
        self.translationCoordinates = [0, 0]
        self.update_canvas()

    def choose_color(self, sender, app_data):
        self.color = [int(i * 255) for i in app_data[:-1]]

    def button_2_release(self):
        dragging_final_coordinates = dpg.get_mouse_pos()
        self.relative_coordinates[0] -= (self.dragging_initial_coordinates[0] - dragging_final_coordinates[0])
        self.relative_coordinates[1] -= (self.dragging_initial_coordinates[1] - dragging_final_coordinates[1])

    def button_2_down(self):
        self.dragging_initial_coordinates[0] = dpg.get_mouse_pos()[0]
        self.dragging_initial_coordinates[1] = dpg.get_mouse_pos()[1]


my_window = Window("Tutorial", 'main_window')
my_window.update_canvas()

with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=my_window.zoom)
    dpg.add_mouse_drag_handler(callback=my_window.move)
    dpg.add_mouse_double_click_handler(button=2, callback=my_window.restore_screen_view)
    dpg.add_mouse_release_handler(button=2, callback=my_window.button_2_release)
    dpg.add_mouse_click_handler(button=2, callback=my_window.button_2_down)


dpg.create_viewport(title='Simple Blast Designer', width=1500, height=800, x_pos=20, y_pos=20)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
settings_set_1 = Settings()
dpg.bind_theme(settings_set_1.global_theme)
# dpg.show_debug()
# dpg.show_style_editor()
# import dearpygui.demo as demo
# demo.show_demo()
dpg.start_dearpygui()
dpg.destroy_context()

# TODO: 1. Check localization problems
# TODO: 2. Find out how to change file dialog style settings
# TODO: 3. Fix physics in the Canvas in translation
# TODO: 5. Prepare icons
# TODO: 6. Transfer all visualized data into Window class as dictionary
# TODO: 7. Cover all in tests


