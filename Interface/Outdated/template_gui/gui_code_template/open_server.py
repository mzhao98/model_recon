
from aiohttp import web
import PySimpleGUI as sg
import aiohttp

LIGHT = 0
HEAVY = 1

INCOMPLETE = 0
DONE = 1


BLUE = 0
GREEN = 1
RED = 2
YELLOW = 3
COLOR_LIST = [BLUE, GREEN, RED, YELLOW]
COLOR_TO_TEXT = {BLUE: 'blue', GREEN:'green', RED:'red', YELLOW:'yellow', None:'white'}
loop = None
# human_rew = {(BLUE, HEAVY): 0, (BLUE, LIGHT): 0, (RED, HEAVY): 0, (RED, LIGHT): 0}
# robot_rew = {(BLUE, HEAVY): 0, (BLUE, LIGHT): 0, (RED, HEAVY): 0, (RED, LIGHT): 0}
human_rew = {
            # (BLUE, LIGHT): 0,
            (RED, LIGHT):0,
            (BLUE, HEAVY): 0,
            (RED, HEAVY): 0,
        }
robot_rew = {
            # (BLUE, LIGHT): 0,
            (RED, LIGHT): 0,
            (BLUE, HEAVY): 0,
            (RED, HEAVY): 0,
        }

def func(message):
    print(message)

window = None
changing_text = ''
changing_episode_index = 0
changing_num_timesteps_available = 0
total_num_episodes = 3
current_timesteps_left = 0

async def handle_old(request):
    font = ('Helvetica', 12, 'bold italic')
    sg.theme('Dark')
    sg.set_options(font=font)
    colors = (sg.theme_background_color(), sg.theme_background_color())

    layout = [[sg.Text('Number of Timesteps Remaining: '+ str(current_timesteps_left), enable_events=True,
                       key='-TEXT-', font=('Arial Bold', 20),
                       expand_x=True, justification='center')],
              [
                  sg.Button('Heavy\nBlue', key='HB', font=('Helvetica', 12), button_color=colors, image_size=(1, 1),
                            image_filename='declutter/gui_imgs/large_blue_2.png', border_width=0),
                  sg.Button('Heavy\nRed', key='HR', button_color=colors, image_size=(1, 1),
                            image_filename='declutter/gui_imgs/large_red_2.png', border_width=0),
                  # sg.Button('Light\nBlue', key='LB', button_color=colors, image_size=(1, 1),
                  #           image_filename='gui_imgs/small_blue_2.png', border_width=0),
                  sg.Button('Light\nRed', key='LR', button_color=colors, image_size=(1, 1),
                            image_filename='declutter/gui_imgs/small_red_2.png', border_width=0),
                  sg.Button('No Action', key='None'),
                  # sg.Exit()
              ]]
    global window
    window = sg.Window('GAME').Layout(layout)

    s = 'No button'
    while True:  # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'HB':
            func('Pressed button 1')
            s = 'heavy blue'
            break
        elif event == 'HR':
            func('Pressed button 2')
            s = 'heavy red'
            break
        elif event == 'LB':
            func('Pressed button 1')
            s = 'light blue'
            break
        elif event == 'LR':
            func('Pressed button 2')
            s = 'light red'
            break
        elif event == 'None':
            func('Pressed button 2')
            s = 'None'
            break
    window.Close()
    return web.json_response(s)


async def handle(request):
    font = ('Helvetica', 12, 'bold italic')
    # psg.theme('Dark')
    sg.set_options(font=font)
    # colors = (psg.theme_background_color(), psg.theme_background_color())
    colors = ('#000000', sg.theme_background_color())

    layout = [[sg.Text('Number of Timesteps Remaining: ', enable_events=True,
                       key='-TEXT-', font=('Arial Bold', 20),
                       expand_x=True, justification='center')],
              [sg.Text(str(current_timesteps_left), enable_events=True,
                       key='-TEXT-', font=('Arial Bold', 40), text_color='red',
                       expand_x=True, justification='center')],

              [sg.Text('Your Rewards: ', enable_events=True,
                        key='-TEXT-', font=('Arial Bold', 20),
                        expand_x=True, justification='center'),
               sg.Button(str(human_rew[(BLUE, HEAVY)]), key='HB', button_color=colors, image_size=(1, 1),
                         image_filename='declutter/gui_imgs/large_blue_2.png', font=('Helvetica', 32), border_width=0),
               sg.Button(str(human_rew[(RED, HEAVY)]), key='HR', font=('Helvetica', 32), button_color=colors,
                         image_size=(1, 1),
                         image_filename='declutter/gui_imgs/large_red_2.png', border_width=0),
               # sg.Button(str(human_rew[(BLUE, LIGHT)]), key='LB', font=('Helvetica', 32), button_color=colors,
               #            image_size=(1, 1),
               #            image_filename='gui_imgs/small_blue_2.png', border_width=0),
               sg.Button(str(human_rew[(RED, LIGHT)]), key='LR', font=('Helvetica', 32), button_color=colors,
                         image_size=(1, 1),
                         image_filename='declutter/gui_imgs/small_red_2.png', border_width=0),
               sg.Button('No Action', key='None'),
               ],
              [sg.Text('Robot Rewards: ', enable_events=True,
                        key='-TEXT-', font=('Arial Bold', 20),
                        expand_x=True, justification='center'),
               sg.Button(str(robot_rew[(BLUE, HEAVY)]), key='rHB', font=('Helvetica', 32),
                         button_color=colors, image_size=(1, 1),
                         image_filename='declutter/gui_imgs/large_blue_2.png', border_width=0),
               sg.Button(str(robot_rew[(RED, HEAVY)]), key='rHR', button_color=colors,
                         image_size=(1, 1), font=('Helvetica', 32),
                         image_filename='declutter/gui_imgs/large_red_2.png', border_width=0),
               # sg.Button(str(robot_rew[(BLUE, LIGHT)]), key='rLB', button_color=colors,
               #            image_size=(1, 1), font=('Helvetica', 32),
               #            image_filename='gui_imgs/small_blue_2.png', border_width=0),
               sg.Button(str(robot_rew[(RED, LIGHT)]), key='rLR', button_color=colors,
                         image_size=(1, 1), font=('Helvetica', 32),
                         image_filename='declutter/gui_imgs/small_red_2.png', border_width=0),
               ],
              [sg.Text('Click the object you wish to pick up. ', enable_events=True,
                       key='-TEXT-', font=('Arial Bold', 20),
                       expand_x=True, justification='center')],
              ]
    global window
    # window = sg.Window('GAME').Layout(layout)
    window = sg.Window('Action Selection', layout, size=(950, 450))

    s = 'No button'
    while True:  # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'HB':
            func('Pressed button 1')
            s = 'heavy blue'
            break
        elif event == 'HR':
            func('Pressed button 2')
            s = 'heavy red'
            break
        elif event == 'LB':
            func('Pressed button 1')
            s = 'light blue'
            break
        elif event == 'LR':
            func('Pressed button 2')
            s = 'light red'
            break
        elif event == 'None':
            func('Pressed button 2')
            s = 'None'
            break
    window.Close()
    return web.json_response(s)


async def handle_first_time(request):
    font = ('Helvetica', 12, 'bold italic')
    sg.theme('Dark')
    sg.set_options(font=font)
    colors = (sg.theme_background_color(), sg.theme_background_color())

    # layout = [
    #     [sg.Button('Blue\nCircle', button_color=colors, image_filename='gui_imgs/large_blue.png', border_width=0)]
    # ]
    layout = [[sg.Text('Hello World', enable_events=True,
   key='-TEXT-', font=('Arial Bold', 20),
   expand_x=True, justification='center')],
        [
         sg.Button('Blue\nCircle', key='HB', button_color=colors, image_size=(1,1), image_filename='declutter/gui_imgs/large_blue_2.png', border_width=0),
         sg.Button('Heavy Blue\n1'), sg.Button('Heavy Red\n2'), sg.Button('Light Blue\n3'), sg.Button('Light Red\n4'),
         sg.Exit()]]
    global window
    window = sg.Window('GAME').Layout(layout)

    s = 'No button'
    while True:  # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'HB':
            func('Pressed button 1')
            s = 'heavy blue'
            break
        elif event == 'Heavy Red\n2':
            func('Pressed button 2')
            s = 'heavy red'
            break
        elif event == 'Light Blue\n3':
            func('Pressed button 1')
            s = 'light blue'
            break
        elif event == 'Light Red\n4':
            func('Pressed button 2')
            s = 'light red'
            break
    # window.Close()
    return web.json_response(s)

async def handle_with_close(request):
    layout = [[sg.Button('Heavy Blue\n1'), sg.Button('Heavy Red\n2'), sg.Button('Light Blue\n3'), sg.Button('Light Red\n4'), sg.Exit()]]

    window = sg.Window('GAME').Layout(layout)
    s = 'No button'
    while True:  # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Heavy Blue\n1':
            func('Pressed button 1')
            s = 'heavy blue'
            break
        elif event == 'Heavy Red\n2':
            func('Pressed button 2')
            s = 'heavy red'
            break
        elif event == 'Light Blue\n3':
            func('Pressed button 1')
            s = 'light blue'
            break
        elif event == 'Light Red\n4':
            func('Pressed button 2')
            s = 'light red'
            break
    window.Close()
    return web.json_response(s)


async def setup_practice_window(request):
    font = ('Helvetica', 12, 'bold italic')
    # sg.theme('Dark')
    sg.set_options(font=font)
    # colors = (sg.theme_background_color(), sg.theme_background_color())

    layout = [[sg.Text('We will begin a Practice Round. ', enable_events=True,
                       key='-TEXT-', font=('Arial', 20),
                       expand_x=True, justification='center')],
              [sg.Text('\nThere will be ' + str(changing_num_timesteps_available) + ' timesteps available during this round.',
                       enable_events=True,
                       key='-TEXT-', font=('Arial', 20),
                       expand_x=True, justification='center')],
              [sg.Button('Click to begin game!')]]
    global window
    window = sg.Window('GAME').Layout(layout)


    to_play = '0'
    while True:  # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Click to begin game!':
            func('Pressed button 1')
            to_play = '1'
            break

    window.Close()
    return web.json_response(to_play)

async def setup_window(request):
    font = ('Helvetica', 12, 'bold italic')
    # sg.theme('Dark')
    sg.set_options(font=font)
    # colors = (sg.theme_background_color(), sg.theme_background_color())

    layout = [[sg.Text('We will begin Round '+str(changing_episode_index+1) + ' of ' + str(total_num_episodes), enable_events=True,
                       key='-TEXT-', font=('Arial', 20),
                       expand_x=True, justification='center')],
              [sg.Text('\nThere will be ' + str(changing_num_timesteps_available) + ' timesteps available during this round.',
                       enable_events=True,
                       key='-TEXT-', font=('Arial', 20),
                       expand_x=True, justification='center')],
              [sg.Button('Click to begin game!')]]
    global window
    window = sg.Window('GAME').Layout(layout)


    to_play = '0'
    while True:  # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Click to begin game!':
            func('Pressed button 1')
            to_play = '1'
            break

    window.Close()
    return web.json_response(to_play)

async def setup_window_last_episode(request):
    font = ('Helvetica', 12, 'bold italic')
    # sg.theme('Dark')
    sg.set_options(font=font)
    # colors = (sg.theme_background_color(), sg.theme_background_color())

    layout = [
              [sg.Text('We will begin Round ' + str(changing_episode_index + 1) + ' of ' + str(total_num_episodes),
                       enable_events=True,
                       key='-TEXT-', font=('Arial', 20),
                       expand_x=True, justification='center')],
                [sg.Text('This is the FINAL ROUND. You and the robot will be evaluated based on this round.',
                 enable_events=True,
                 key='-TEXT-', font=('Arial Bold', 25),
                 expand_x=True, justification='center', text_color='red')],
              [sg.Text('\nThere will be ' + str(changing_num_timesteps_available) + ' timesteps available during this round.',
                       enable_events=True,
                       key='-TEXT-', font=('Arial', 20),
                       expand_x=True, justification='center')],
              [sg.Button('Click to begin game!')]]
    global window
    window = sg.Window('GAME').Layout(layout)


    to_play = '0'
    while True:  # Event Loop
        event, values = window.Read()
        if event in (None, 'Exit'):
            break
        if event == 'Click to begin game!':
            func('Pressed button 1')
            to_play = '1'
            break

    window.Close()
    return web.json_response(to_play)

async def close_window(request):
    # layout = [[sg.Exit()]]
    global window
    # window = sg.Window('GAME').Layout(layout)
    #
    # while True:  # Event Loop
    #     event, values = window.Read()
    #     if event in (None, 'Exit'):
    #         break
    #

    window.Close()
    return

async def timestep_update_websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            # if msg.data == 'close':
            #     await ws.close()
            # else:
            new_text = msg.data
            global current_timesteps_left

            current_timesteps_left = int(new_text)
            print("current_timesteps_left = ", current_timesteps_left)
            await ws.send_str(msg.data + '/answer')

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

async def episode_index_update_websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            # if msg.data == 'close':
            #     await ws.close()
            # else:
            new_text = msg.data
            global changing_episode_index
            global changing_num_timesteps_available
            new_text = new_text.split(',')
            changing_episode_index = int(new_text[0])
            changing_num_timesteps_available = int(new_text[1])
            print("changing_episode_index = ", changing_episode_index)
            print("changing_num_timesteps_available = ", changing_num_timesteps_available)
            await ws.send_str(msg.data + '/answer')

        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

async def game_update_websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                new_text = msg.data
                global changing_text
                changing_text = new_text
                print("changing_text = ", changing_text)
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

async def human_reward_update_websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                new_text = msg.data
                global human_rew
                new_text = new_text.split(',')
                # human_rew[(BLUE, LIGHT)] = int(new_text[0])
                human_rew[(RED, LIGHT)] = int(new_text[0])
                human_rew[(BLUE, HEAVY)] = int(new_text[1])
                human_rew[(RED, HEAVY)] = int(new_text[2])

                print("human_rew = ", human_rew)
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws

async def robot_reward_update_websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                new_text = msg.data
                global robot_rew
                new_text = new_text.split(',')
                # robot_rew[(BLUE, LIGHT)] = int(new_text[0])
                robot_rew[(RED, LIGHT)] = int(new_text[0])
                robot_rew[(BLUE, HEAVY)] = int(new_text[1])
                robot_rew[(RED, HEAVY)] = int(new_text[2])

                print("robot_rew = ", robot_rew)
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws






app = web.Application()

app.add_routes([
    web.get('/', setup_window),
        # web.get('/ask_first', handle_first_time),
        web.get('/ask', handle),
        # web.get('/ask_with_close', handle_with_close),
        web.get('/create', setup_window),
        web.get('/create_last_episode', setup_window_last_episode),
        web.get('/create_practice', setup_practice_window),
        web.get('/close', close_window),
        # web.get('/ws', game_update_websocket_handler),
        web.get('/ep_idx_update', episode_index_update_websocket_handler),
        web.get('/timestep_update', timestep_update_websocket_handler),
        web.get('/human_reward_update', human_reward_update_websocket_handler),
        web.get('/robot_reward_update', robot_reward_update_websocket_handler),
                ])



if __name__ == '__main__':
    web.run_app(app)



from multiprocessing import Process,Pipe

# def f(child_conn):
#     msg = "Hello"
#     child_conn.send(msg)
#     child_conn.close()
#
# if __name__ == '__main__':
#     while True:
#         send = input("send? ")
#         if send == '0':
#             f()
#

