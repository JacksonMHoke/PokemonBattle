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
        for j, slot in enumerate(team.slots):
            if slot.pokemon is None or slot.pokemon.state==State.FAINTED:
                context.window[f'team{i+1}:{j}PokemonName'].update(value='Name: N/A')
                context.window[f'team{i+1}:{j}HP'].update(value='HP: N/A')
                context.window[f'team{i+1}:{j}Sprite'].update(filename=f'./sprites/default.png')
                continue
            context.window[f'team{i+1}:{j}PokemonName'].update(value=f'Name: {slot.pokemon.name}')
            context.window[f'team{i+1}:{j}HP'].update(value=f'HP: {slot.pokemon.stats[Stat.HP]}')
            context.window[f'team{i+1}:{j}Sprite'].update(filename=f'./sprites/{type(slot.pokemon).__name__.lower()}.png')
    context.window.refresh()

    # TODO: implement this function once UI is decided on

def getLayout(context):
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
    
    # team1DD=sg.Column([[sg.Text('Select a _', key='team1DDTitle')], [sg.Combo(['choice 1', 'choice 2'], readonly=True, size=(50, 1), auto_size_text=False, key='team1DDChoice')], [sg.Button('Submit', key='submit1')]], visible=False, key='team1DD')
    # team2DD=sg.Column([[sg.Text('Select a _', key='team2DDTitle')], [sg.Combo(['choice 1', 'choice 2'], readonly=True, size=(50, 1), auto_size_text=False, key='team2DDChoice')], [sg.Button('Submit', key='submit2')]], visible=False, key='team2DD')

    teamSlots=[]
    teamDDs=[]
    for i, team in enumerate(context.teams):
        teamDDs.append(sg.Column([
            [sg.Text('Select a _', key=f'team{i+1}DDTitle')],
            [sg.Combo(['choice 1', 'choice 2'], readonly=True, size=(50, 1), auto_size_text=False, key=f'team{i+1}DDChoice')],
            [sg.Button('Submit', key=f'submit{i+1}')]
        ], visible=False, key=f'team{i+1}DD'))
        teamSlots.append([])
        for j, slot in enumerate(team.slots):
            teamSlots[i].append(sg.Column([
                [sg.Text('Name: N/A', key=f'team{i+1}:{j}PokemonName')],
                [sg.Text('HP: N/A', key=f'team{i+1}:{j}HP')],
                [sg.Image(filename="./sprites/default.png", key=f'team{i+1}:{j}Sprite')]
            ]))
            teamSlots[i].append(sg.VerticalSeparator())
        teamSlots[i].pop()

    print('TeamSlots', teamSlots, flush=True)
    
    teamLayouts=[]
    for i, (slots, dd) in enumerate(zip(teamSlots, teamDDs)):
        print('Individual slots', slots, flush=True)
        print(dd)
        teamLayouts.append(sg.Column([
            [sg.Text(f'Team {i+1}')],
            [sg.Column([slots])],
            [dd],
        ]))
        teamLayouts.append(sg.HorizontalSeparator())
    teamLayouts.pop()

    print('Team Layouts', teamLayouts, flush=True)
    print(teamSlots[0][0].Layout)
    rightLayout=sg.Column([[sg.Text('Combat Log')], [sg.Multiline('', key='combatLog', size=(250, 600), disabled=True, autoscroll=True)]], vertical_alignment='top', element_justification='right')
    return [[sg.Column([[l] for l in teamLayouts]), sg.VerticalSeparator(), rightLayout]]


    # Layout for the top section (Team 1)
    # team1_layout=[
    #     [sg.Text('Team 1', font=('Helvetica', 16))],
    #     [sg.Text('Name: N/A', key='team1PokemonName')],
    #     [sg.Text('HP: N/A', key='team1HP')],
    #     [sg.Image(filename="./sprites/default.png", key='team1Sprite')],
    #     [team1DD]
    # ]

    # Layout for the bottom section (Team 2)
    # team2_layout=[
    #     [sg.Text('Team 2', font=('Helvetica', 16))],
    #     [sg.Text('Name: N/A', key='team2PokemonName')],
    #     [sg.Text('HP: N/A', key='team2HP')],
    #     [sg.Image(filename="./sprites/default.png", key='team2Sprite')],
    #     [team2DD]
    # ]

    # Full window layout: Two rows with columns for team layouts
    # leftLayout=sg.Column([[sg.Column(team1_layout, element_justification='center')], [sg.HorizontalSeparator()], [sg.Column(team2_layout, element_justification='center')]])
    # 
    # return [[teamLayouts, sg.VerticalSeparator(), rightLayout]]

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