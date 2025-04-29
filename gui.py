import FreeSimpleGUI as sg
from globals import *

def waitForSubmit(battleContext, team):
    """Waits until submit button is clicked"""
    while True:
        e, v=battleContext.window.read()
        if e==sg.WINDOW_CLOSED or e=="Exit":
            break
        if (v[f'team{team+1}DDChoice']!='' or v[f'team{team+1}DDSwapChoice']!='') and ('submit' in e or '\r' in e):
            break
    return v

def refreshWindow(battleContext):
    '''Refreshes GUI with values from battleContext'''
    if battleContext.weather is not None:
        battleContext.window['weather'].update(background_color=battleContext.weather.color)
    else:
        battleContext.window['weather'].update(background_color='gray')
    for i, team in enumerate(battleContext.teams):
        for j, slot in enumerate(team.slots):
            if slot.pokemon is None or slot.pokemon.state==State.FAINTED:
                battleContext.window[f'team{i+1}:{j}PokemonName'].update(value='Name: N/A')
                battleContext.window[f'team{i+1}:{j}HP'].update(value='HP: N/A')
                battleContext.window[f'team{i+1}:{j}Status'].update(value='   ', background_color='gray')
                battleContext.window[f'team{i+1}:{j}Sprite'].update(filename=f'./sprites/default.png')
                continue
            battleContext.window[f'team{i+1}:{j}PokemonName'].update(value=f'Name: {slot.pokemon.name}')
            battleContext.window[f'team{i+1}:{j}HP'].update(value=f'HP: {slot.pokemon.stats.currentHP}')
            battleContext.window[f'team{i+1}:{j}Status'].update(value='   ', background_color='gray' if slot.pokemon.status is None else slot.pokemon.status.color)
            battleContext.window[f'team{i+1}:{j}Sprite'].update(filename=f'./sprites/{type(slot.pokemon).__name__.lower()}.png')
    battleContext.window.refresh()

def showDropdown(battleContext, team, text, values):
    battleContext.window[f'team{team+1}DDTitle'].update(value=text)
    battleContext.window[f'team{team+1}DDChoice'].update(values=values)
    battleContext.window[f'team{team+1}DD'].update(visible=True)
    battleContext.window[f'team{team+1}DDChoice'].SetFocus()
    battleContext.window.refresh()

def hideDropdown(battleContext, team):
    battleContext.window[f'team{team+1}DD'].update(visible=False)

def showSwapDropdown(battleContext, team, text, values):
    battleContext.window[f'team{team+1}DDSwapChoice'].update(values=values, visible=True)

def hideSwapDropdown(battleContext, team):
    battleContext.window[f'team{team+1}DDSwapChoice'].update(visible=False)


def getLayout(battleContext):
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

    teamSlots=[]
    teamDDs=[]
    for i, team in enumerate(battleContext.teams):
        teamDDs.append(sg.Column([
            [sg.Text('Select a _', key=f'team{i+1}DDTitle')],
            [sg.Combo(['choice 1', 'choice 2'], readonly=True, size=(25, 1), auto_size_text=False, key=f'team{i+1}DDChoice'), sg.Combo(['swapChoice1', 'swapChoice2'], readonly=True, size=(25, 1), auto_size_text=False, key=f'team{i+1}DDSwapChoice', visible=False)],
            [sg.Button('Submit', key=f'submit{i+1}')]
        ], visible=False, key=f'team{i+1}DD'))
        teamSlots.append([])
        for j, slot in enumerate(team.slots):
            teamSlots[i].append(sg.Column([
                [sg.Text('Name: N/A', key=f'team{i+1}:{j}PokemonName')],
                [sg.Text('HP: N/A', key=f'team{i+1}:{j}HP'), sg.Text('   ', background_color='gray', key=f'team{i+1}:{j}Status')],
                [sg.Image(filename="./sprites/default.png", key=f'team{i+1}:{j}Sprite')]
            ]))
            teamSlots[i].append(sg.VerticalSeparator())
        teamSlots[i].pop()
    
    teamLayouts=[sg.Column([[sg.Text('Weather: '), sg.Text('    ', background_color='gray', key='weather')]])]
    for i, (slots, dd) in enumerate(zip(teamSlots, teamDDs)):
        teamLayouts.append(sg.Column([
            [sg.Text(f'Team {i+1}')],
            [sg.Column([slots])],
            [dd],
        ]))
        teamLayouts.append(sg.HorizontalSeparator())
    teamLayouts.pop()
    rightLayout=sg.Column([[sg.Text('Combat Log')], [sg.Multiline('', key='combatLog', size=(250, 600), disabled=True, autoscroll=True)]], vertical_alignment='top', element_justification='right')
    return [[sg.Column([[l] for l in teamLayouts]), sg.VerticalSeparator(), rightLayout]]

class DropdownItem:
    """
    Dropdown item class that stores display text and index of the option selected.

    Attributes:
        displayText (str): text to be displayed
        id (int): index of option on dropdown menu
    """
    def __init__(self, displayText, id):
        self.displayText=displayText
        self.id=id

    def __str__(self):
        return self.displayText