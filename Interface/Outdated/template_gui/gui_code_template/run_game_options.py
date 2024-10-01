import PySimpleGUI as psg
import aiohttp
import asyncio
import numpy as np
import pickle
import time
from declutter2.run_user_study import run_single_game
# from declutter2.run_trial import  run_single_game
# from  critical_states.play_single_game import play_single_round_game
import subprocess
loop = None


def wait_between_games():
    l1 = psg.Text('Please select a game....', key='-OUT-', font=('Arial Bold', 20), expand_x=True, justification='center')
    b1 = psg.Button('Declutter', key='declutter', font=('Arial Bold', 20), visible=True)
    b2 = psg.Button('Treasure', key='treasure', font=('Arial Bold', 20), visible=True)
    b3 = psg.Button('Social Navigation', key='social', font=('Arial Bold', 20), visible=True)
    layout = [[l1], [b1, b2, b3]]
    window = psg.Window('SELECT', layout, size=(750, 150))
    # window['OK'].update(visible=False)
    game_selected = None
    while (True):

        event, values = window.read()

        if event == 'declutter':
            game_selected = 'declutter'
            break
        if event == 'treasure':
            game_selected = 'treasure'
            break
        if event == 'social':
            game_selected = 'social'
            break
    window.close()
    return game_selected



if __name__ == "__main__":
    mode = 'joystick'
    name = 'mike'
    save_data = True
    while True:
        game_selected = wait_between_games()
        if game_selected == 'declutter':
            run_single_game()
            # process = subprocess.Popen(
            #     "conda run -n py35pybullet python declutter/run_user_study.py".split(), stdout=subprocess.PIPE
            # )
            # output, error = process.communicate()
        if game_selected == 'treasure':
            # play_single_round_game()
            process = subprocess.Popen(
                "conda run -n cogail python critical_states/play_single_game.py".split(), stdout = subprocess.PIPE
            )
            output, error = process.communicate()
        if game_selected == 'social':
            process = subprocess.Popen(
                "conda run -n cogail python social_nav/play_single_game.py".split(), stdout=subprocess.PIPE
            )
            output, error = process.communicate()
