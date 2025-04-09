import FreeSimpleGUI as sg
from globals import *

def waitForSubmit(context):
    """Waits until submit button is clicked"""
    while True:
        e, v=context.window.read()
        if e==sg.WINDOW_CLOSED or e=="Exit":
            break
        if 'submit' in e:
            break
    return v

def refreshWindow(context):
    '''Refreshes GUI with values from context'''
    for i, team in enumerate(context.teams):
        for slot in team.slots:
            if slot.pokemon is None or slot.pokemon.state==State.FAINTED:
                context.window[f'team{i+1}PokemonName'].update(value='Name: N/A')
                context.window[f'team{i+1}HP'].update(value='HP: N/A')
                context.window[f'team{i+1}Sprite'].update(filename=f'./sprites/default.png')
                continue
            context.window[f'team{i+1}PokemonName'].update(value=f'Name: {slot.pokemon.name}')
            context.window[f'team{i+1}HP'].update(value=f'HP: {slot.pokemon.stats[Stat.HP]}')
            context.window[f'team{i+1}Sprite'].update(filename=f'./sprites/{type(slot.pokemon).__name__.lower()}.png')
    context.window.refresh()

    # TODO: implement this function once UI is decided on

def getLayout():
    """Gets layout for battle"""
    sg.LOOK_AND_FEEL_TABLE['FlatTheme']={
        'BACKGROUND': '#313338',
        'TEXT': '#FFFFFF',
        'INPUT': '#FFFFFF',
        'TEXT_INPUT': '#000000',
        'SCROLL': '#c7e78b',
        'BUTTON': ('#000000', '#FFFFFF'),
        'PROGRESS': ('#FFFFFF', '#000000'),
        'BORDER': 0,
        'SLIDER_DEPTH': 0,
        'PROGRESS_DEPTH': 0,
    }
    sg.theme('FlatTheme')
    
    team1DD=sg.Column([[sg.Text('Select a _', key='team1DDTitle')], [sg.Combo(['choice 1', 'choice 2'], readonly=True, size=(50, 1), auto_size_text=False, key='team1DDChoice')], [sg.Button('Submit', key='submit1')]], visible=False, key='team1DD')
    team2DD=sg.Column([[sg.Text('Select a _', key='team2DDTitle')], [sg.Combo(['choice 1', 'choice 2'], readonly=True, size=(50, 1), auto_size_text=False, key='team2DDChoice')], [sg.Button('Submit', key='submit2')]], visible=False, key='team2DD')

    # Layout for the top section (Team 1)
    team1_layout=[
        [sg.Text('Team 1', font=('Helvetica', 16))],
        [sg.Text('Name: N/A', key='team1PokemonName')],
        [sg.Text('HP: N/A', key='team1HP')],
        [sg.Image(filename="./sprites/default.png", key='team1Sprite')],
        [team1DD]
    ]

    # Layout for the bottom section (Team 2)
    team2_layout=[
        [sg.Text('Team 2', font=('Helvetica', 16))],
        [sg.Text('Name: N/A', key='team2PokemonName')],
        [sg.Text('HP: N/A', key='team2HP')],
        [sg.Image(filename="./sprites/default.png", key='team2Sprite')],
        [team2DD]
    ]

    # Full window layout: Two rows with columns for team layouts
    leftLayout=sg.Column([[sg.Column(team1_layout, element_justification='center')], [sg.HorizontalSeparator()], [sg.Column(team2_layout, element_justification='center')]])
    rightLayout=sg.Column([[sg.Text('Combat Log')], [sg.Multiline('', key='combatLog', size=(250, 600), disabled=True, autoscroll=True)]], vertical_alignment='top', element_justification='right')
    return [[leftLayout, sg.VerticalSeparator(), rightLayout]]