import dearpygui.dearpygui as dpg

dpg.create_context()

def callback(sender, app_data):
    print("Sender: ", sender)
    print("App Data: ", app_data)


with dpg.font_registry():
    with dpg.font(r"C:\MDA\Scripts\Others\Fonts\Manrope.ttf", 20) as font1:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.bind_font(font1)

with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 15, 15)
        dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 4)

        dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, [100, 150, 200])
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, [200, 100, 20])
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, [12, 55, 0])
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [110, 120, 110])
        dpg.add_theme_color(dpg.mvThemeCol_Text, [230, 230, 230])
        dpg.add_theme_color(dpg.mvThemeCol_Button, [200, 100, 20])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [100, 150, 200])


    with dpg.file_dialog(directory_selector=False, show=False, callback=callback, tag="file_dialog_tag"):

        dpg.add_file_extension(".*")
        dpg.add_file_extension("", color=(150, 255, 150, 255))
        dpg.add_file_extension(".cpp", color=(255, 255, 0, 255))
        dpg.add_file_extension(".h", color=(255, 0, 255, 255))
        dpg.add_file_extension(".py", color=(0, 255, 0, 255))


        with dpg.group(horizontal=True):
            dpg.add_button(label="fancy file dialog")
            dpg.add_button(label="file")
            dpg.add_button(label="dialog")
        dpg.add_date_picker()
        with dpg.child_window(height=100):
            dpg.add_selectable(label="bookmark 1")
            dpg.add_selectable(label="bookmark 2")
            dpg.add_selectable(label="bookmark 3")

    with dpg.window(label="Tutorial", width=800, height=300):
        dpg.add_button(label="File Selector", callback=lambda: dpg.show_item("file_dialog_tag"))


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.bind_theme(global_theme)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()