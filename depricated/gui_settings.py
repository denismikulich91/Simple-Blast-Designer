import dearpygui.dearpygui as dpg


class Settings:
    def __init__(self):

        with dpg.font_registry():
            with dpg.font(r"C:\MDA\Scripts\Others\Fonts\Manrope.ttf", 20) as font1:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                dpg.bind_font(font1)

        with dpg.theme() as self.global_theme:
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
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [100, 150, 200])  # 100, 150, 200

        dpg.bind_theme(self.global_theme)
