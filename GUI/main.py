import dearpygui.dearpygui as dpg
from web_scraping.scraper import Scraper
scrap = Scraper()


dpg.create_context()

def change_text(sender, app_data, user_data):

    for tag, FII in user_data.items():
        if dpg.is_item_hovered(tag):
            dpg.set_item_label(9000, FII["name"])
            dpg.set_value(9000, FII["performance"])

FII_dpg = {}

with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=change_text, user_data=FII_dpg)



dpg.create_viewport(title='Custom Title', width=1200, height=900)

with dpg.window(label="Example Window", menubar=True,  no_close=True, width=1500):
    
    with dpg.menu_bar():
        with dpg.menu(label="File"):        
            pass
        with dpg.menu(label="Settings"):
            pass
    

    dpg.add_text("Top FIIs")
    dpg.add_separator()


    dpg.add_simple_plot(label="AAGR11", default_value=scrap.get_performance("AAGR11"), height=300, histogram=True, tag = 9000)

    FII_list = ["AAGR11", "AAZQ11", "HDEL11", "ABCP11"]

    for idx, FII in enumerate(FII_list):
        FII_dpg[dpg.add_text(FII,tag=idx+100)] = {"name": FII, "performance":scrap.get_performance(FII)}
        #with dpg.tooltip(idx+100):
        #    dpg.add_simple_plot(label=FII, default_value=scrap.get_performance(FII), height=300, histogram=True)
        #    dpg.add_separator()

    
    






dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
