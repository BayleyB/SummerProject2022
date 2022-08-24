import game as rps
import menu_resources as mr
import PySimpleGUI as psg

large_font = ("Arial", 30)
small_font = ("Arial", 10)
bg_color = 'black'
menu_button_color = 'blue'
window_width = 500
window_height = 300

menu_layout = [[psg.Text("Rock, Paper, Scissors", font=large_font, background_color=bg_color)], 
               [psg.Text("By: Bayley Barreuther", font=small_font, background_color=bg_color)],
               [psg.Text("Summer 2022\n", font=small_font, background_color=bg_color)],
               [psg.Button("Start Game", button_color=menu_button_color)],
               [psg.Button("About", button_color=menu_button_color)],
               [psg.Button("Close", button_color=menu_button_color)]]

menu_window = psg.Window("Rock, Paper, Scissors", menu_layout,
                         background_color=bg_color,
                         size=(window_width, window_height),
                         element_justification='c')

while True:
    event, _ = menu_window.read()

    if event == "Start Game":
        rps.run_game()
    elif event == "About":
        mr.run_about_window(large_font, small_font, bg_color, menu_button_color, window_width, window_height)
    elif (event == psg.WIN_CLOSED) or (event == "Close"):
        break
menu_window.close()