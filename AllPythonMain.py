from Libs.GuiLib.gui_helpers import *
from App_3500ParkingLogin.ParkingLoginApp import *


if __name__ == '__main__':
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)

    # NAVIGATION FRMAE
    nav_frame = NavigableTkFrame(root)
    nav_frame.grid(row=0, column=0, sticky='nsew')

    # APPS
    app_parking_login = ParkingLoginApp(nav_frame)

    # SET APPS
    nav_frame.add_content_frame(0, app_parking_login)

    root.mainloop()
