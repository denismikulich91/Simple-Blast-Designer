from tkinter import Tk
import dearpygui.dearpygui as dpg
import dearpygui.demo

win = Tk()
viewport_width = win.winfo_screenwidth() - 100
viewport_height = win.winfo_screenheight() - 100

dpg.create_context()
# Contants below used to form an initial table shape. Column number - initial data based, row number - user based
PRE_DEFINED_COLUMNS = ['Type', 'Field Name', 'Calculation', 'Source', 'Destination', 'Material', 'Quality', 'More']
CUSTOM_COLUMN_NUMBER = 5
ROW_NUMBER = 1
TABLE_DATA = dict()
def add_row():
    global ROW_NUMBER
    ROW_NUMBER += 1
    with dpg.table_row(parent='table'):
        dpg.add_combo(('Data', 'Empty line', 'Free text'), default_value='Data', width=-1, tag=f'row_type{ROW_NUMBER}')
        dpg.add_input_text(width=-1, tag=f'row_name{ROW_NUMBER}')
        dpg.add_combo(('Sum', 'Average', 'Weighted', 'Custom...'), default_value='Sum', width=-1,
                      tag=f'calc_type{ROW_NUMBER}')
        dpg.add_combo(width=-1, tag=f'source{ROW_NUMBER}')
        dpg.add_combo(width=-1, tag=f'destination{ROW_NUMBER}')
        dpg.add_combo(width=-1, tag=f'material{ROW_NUMBER}')
        dpg.add_combo(width=-1, tag=f'quality{ROW_NUMBER}')
        with dpg.table_cell():
            with dpg.group(horizontal=True):
                dpg.add_image_button(texture_tag='add_row', width=20, height=20, callback=add_row)
                dpg.add_image_button(texture_tag='delete_row', width=20, height=20)
                dpg.add_image_button(texture_tag='row_down', width=20, height=20)
                dpg.add_image_button(texture_tag='row_up', width=20, height=20)
    dpg.set_value('row_number_text', f'Total rows: {ROW_NUMBER}')

def get_table_data():
    for row in range(ROW_NUMBER):
        TABLE_DATA[row + 1] = [dpg.get_value(f'row_type{row + 1}'), dpg.get_value(f'row_name{row + 1}'),
                                  dpg.get_value(f'calc_type{row + 1}'),
                                  dpg.get_value(f'source{row + 1}'), dpg.get_value(f'destination{row + 1}'),
                                  dpg.get_value(f'material{row + 1}'), dpg.get_value(f'quality{row + 1}')]
    return TABLE_DATA

with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("icons/add_row.png")
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="add_row")
    width, height, channels, data = dpg.load_image("icons/delete_row.png")
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="delete_row")
    width, height, channels, data = dpg.load_image("icons/row_down.png")
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="row_down")
    width, height, channels, data = dpg.load_image("icons/row_up.png")
    dpg.add_static_texture(width=width, height=height, default_value=data, tag="row_up")


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

with dpg.window(label="Welcome to Minesched Shaper!", width=int(viewport_width * 0.75),
                height=viewport_height - 100, no_move=True):
    with dpg.group(horizontal=True):
        dpg.add_text('Here you can create any report from Minesched you like.')
    with dpg.tab_bar():
        with dpg.tab(label='Table'):
            with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
               borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True, tag='table'):

                for j in PRE_DEFINED_COLUMNS:
                    dpg.add_table_column(label=j, tag=f'data{j}')
                with dpg.table_row(parent='table'):
                    dpg.add_combo(('Data', 'Empty line', 'Free text'), default_value='Data', width=-1, tag=f'row_type{ROW_NUMBER}')
                    dpg.add_input_text(width=-1, tag=f'row_name{ROW_NUMBER}')
                    dpg.add_combo(('Sum', 'Average', 'Weighted', 'Custom...'), default_value='Sum', width=-1, tag=f'calc_type{ROW_NUMBER}')
                    dpg.add_combo(width=-1, tag=f'source{ROW_NUMBER}')
                    dpg.add_combo(width=-1, tag=f'destination{ROW_NUMBER}')
                    dpg.add_combo(width=-1, tag=f'material{ROW_NUMBER}')
                    dpg.add_combo(width=-1, tag=f'quality{ROW_NUMBER}')
                    with dpg.table_cell():
                        with dpg.group(horizontal=True):
                            dpg.add_image_button(texture_tag='add_row', width=20, height=20, callback=add_row)
                            dpg.add_image_button(texture_tag='delete_row', width=20, height=20)
                            dpg.add_image_button(texture_tag='row_down', width=20, height=20)
                            dpg.add_image_button(texture_tag='row_up', width=20, height=20)


        with dpg.tab(label='Plot'):
            dpg.add_button(label='New Plot')
    with dpg.font_registry():
        with dpg.font(r"C:\MDA\Scripts\Others\Fonts\Manrope.ttf", 20) as font1:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
            dpg.bind_font(font1)

with dpg.window(label="Tools you need", width=int(viewport_width * 0.25), height=viewport_height - 100,
                pos=(int(viewport_width*0.75), 0), no_move=True, tag='tool_window'):
    with dpg.group(horizontal=True):
        dpg.add_button(label='Run report', callback=get_table_data)
        dpg.add_button(label='Save my settings')
    with dpg.group(horizontal=True):
        dpg.add_button(label='Load my settings')
        dpg.add_button(label='Transpose')
    dpg.add_text(f'Total rows: {ROW_NUMBER}', parent='tool_window', tag='row_number_text')
    dpg.add_text(f'Total columns: {len(PRE_DEFINED_COLUMNS + PRE_DEFINED_COLUMNS)}')

# dearpygui.demo.show_demo()
dpg.bind_theme(global_theme)
dpg.create_viewport(title='Minesched Shaper', width=viewport_width+15, height=viewport_height, x_pos=50, y_pos=50,
                    clear_color=(150, 150, 200))
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
