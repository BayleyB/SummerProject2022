import PySimpleGUI as psg

def run_about_window(large_font, small_font, bg_color, menu_button_color, window_width, window_height):
    about_layout = [[psg.Text("This game is really fun", justification='center', font=small_font, background_color=bg_color)],
                    [psg.Button("Close", button_color=menu_button_color)]]

    about_window = psg.Window("About", about_layout,
                              background_color=bg_color,
                              size=(window_width, window_height))

    while True:
        about_event, _ = about_window.read()

        if (about_event == psg.WIN_CLOSED) or (about_event == "Close"):
            break
    about_window.close()
    return