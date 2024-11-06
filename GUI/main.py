import dearpygui.dearpygui as dpg
from ..web_scraping import scraper

scrap = scraper.Scraper()


dpg.create_context()
dpg.create_viewport(title='Custom Title', width=1200, height=900)

with dpg.window(label="Example Window", menubar=True,autosize=True, no_resize=True, no_close=True):
    
    with dpg.menu_bar():
        with dpg.menu(label="File"):        
            pass
        with dpg.menu(label="Settings"):
            pass
    

    dpg.add_text("Top FIIs")
    dpg.add_separator()

    dpg.add_simple_plot(label="Simpleplot1", default_value=scrap.get_performance("AAGR11"), height=300)





dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
