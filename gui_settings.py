import dearpygui.dearpygui as dpg


class Settings:
    def __init__(self):

        with dpg.font_registry():
            with dpg.font(r"C:\MDA\Scripts\Others\Fonts\Manrope.ttf", 18) as font1:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                dpg.bind_font(font1)

        with dpg.theme() as self.global_theme:
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
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, [150, 150, 200])

        dpg.bind_theme(self.global_theme)
