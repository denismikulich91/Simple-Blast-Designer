import dearpygui.dearpygui as dpg
import math

axe_scale = 1
def zoom(sender, app_data):
    global axe_scale
    if app_data == -1:
        axe_scale -= 0.5
    else:
        axe_scale += 0.5

transCoords = [0, 0]
def move(sender, app_data):
    global transCoords
    if app_data[0] == 2:
        transCoords[0] += app_data[1]/10
        transCoords[1] += app_data[2]/10

def restore_screen_view():
    global transCoords, axe_scale
    axe_scale = 1
    transCoords = [0, 0]


color = [255, 255, 255]
def choose_color(sender, app_data):
    global color
    color = [int(i*255) for i in app_data[:-1]]


dpg.create_context()
dpg.configure_app(docking=True)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Text, [200, 200, 200])
        dpg.add_theme_color(dpg.mvThemeCol_Button, [200, 100, 20])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [150, 150, 200])
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, [200, 100, 200])
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, [200, 100, 20])
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [12, 35, 0])
        dpg.add_theme_color(dpg.mvThemeCol_Tab, [150, 150, 200])
        dpg.add_theme_color(dpg.mvThemeCol_TabHovered, [150, 150, 200])
        dpg.add_theme_color(dpg.mvThemeCol_TabActive, [200, 100, 20])
        dpg.add_theme_color(dpg.mvThemeCol_TableRowBg, [20, 20, 200])
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [12, 35, 0])

def toggle_layer(sender, app_data, user_data):
    show_value = dpg.get_value(sender)
    dpg.configure_item(user_data, show=show_value)

with dpg.font_registry():
    with dpg.font(r"../Source/Manrope.ttf", 16) as font1:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.bind_font(font1)

with dpg.window(tag='main_window', label="Tutorial"):

    with dpg.drawlist(width=1000, height=730):

        with dpg.draw_layer(tag="canvas"):
            with dpg.draw_node(tag="base_layer", show=True):
                dpg.draw_polygon([[0,0], [2,2], [5,5], [50,50], [25, 0], [0,0]])


with dpg.window(tag = 'toolWindow', label="Tools", pos=[920, 0], min_size=[80,50]):
    dpg.add_button(label='Zoom All', width=70, callback=restore_screen_view)
    dpg.add_button(label='Draw Line', width=70)
    dpg.add_button(label='New segment', width=70)
    dpg.add_checkbox(label="Import", user_data="base_layer", callback=toggle_layer, default_value=False)
    # TODO Fix a gap on the right
    dpg.add_color_picker(callback=choose_color, default_value=(255, 255, 255), no_alpha=True, no_side_preview=True,
    no_small_preview=True)


with dpg.handler_registry():
    dpg.add_mouse_wheel_handler(callback=zoom)
    dpg.add_mouse_drag_handler(callback=move)
    dpg.add_mouse_double_click_handler(button=2, callback=restore_screen_view)


scale = dpg.create_scale_matrix([axe_scale, axe_scale, axe_scale])
rotation = dpg.create_rotation_matrix(math.pi/2, [0, 0, -1])
translation = dpg.create_translation_matrix(transCoords)

dpg.create_viewport(title='Simple Blast Designer', width=1000, height=800, x_pos=20, y_pos=20)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)
dpg.bind_theme(global_theme)
while dpg.is_dearpygui_running():
    scale = dpg.create_scale_matrix([axe_scale, axe_scale, axe_scale])
    translation = dpg.create_translation_matrix(transCoords)
    dpg.apply_transform("base_layer", scale * translation)
    dpg.render_dearpygui_frame()

dpg.destroy_context()
