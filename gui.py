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
                continue
            context.window[f'team{i+1}PokemonName'].update(value=f'Name: {slot.pokemon.name}')
            context.window[f'team{i+1}HP'].update(value=f'HP: {slot.pokemon.stats[Stat.HP]}')
    context.window.refresh()

    # TODO: implement this function once UI is decided on

def getLayout():
    """Gets layout for battle"""
    # Layout for the top section (Team 1)
    movesTeam1=sg.Column([[sg.Text('Select a Move:')], [sg.Combo(['Move1', 'Move2'], readonly=True, key='team1MoveChoice')]], visible=False, key='team1MoveOptions')
    movesTeam2=sg.Column([[sg.Text('Select a Move:')], [sg.Combo(['Move1', 'Move2'], readonly=True, key='team2MoveChoice')]], visible=False, key='team2MoveOptions')
    trainerSelectionTeam1=sg.Column([[sg.Text('Select a Trainer:')], [sg.Combo(['T1', 'T2'], readonly=True, key='team1TrainerChoice')]], visible=False, key='team1TrainerOptions')
    trainerSelectionTeam2=sg.Column([[sg.Text('Select a Trainer:')], [sg.Combo(['T1', 'T2'], readonly=True, key='team2TrainerChoice')]], visible=False, key='team2TrainerOptions')
    selectionTeam1=sg.Column([[sg.Text('Select a Pokémon:')], [sg.Combo(['Pikachu', 'Charmander', 'Bulbasaur', 'Squirtle'], key='team1PokemonChoice', readonly=True)]], visible=False, key='team1PokemonOptions')
    selectionTeam2=sg.Column([[sg.Text('Select a Pokémon:')], [sg.Combo(['Pikachu', 'Charmander', 'Bulbasaur', 'Squirtle'], key='team2PokemonChoice', readonly=True)]], visible=False, key='team2PokemonOptions')
    targetTeam1=sg.Column([[sg.Text('Select a Target:')], [sg.Combo(['Target1', 'Target2'], readonly=True, key='team1TargetChoice')]], visible=False, key='team1TargetOptions')
    targetTeam2=sg.Column([[sg.Text('Select a Target:')], [sg.Combo(['Target1', 'Target2'], readonly=True, key='team2TargetChoice')]], visible=False, key='team2TargetOptions')


    team1_layout = [
        [sg.Text('Team 1', font=('Helvetica', 16))],
        [sg.Text('Name: N/A', key='team1PokemonName')],
        [sg.Text('HP: N/A', key='team1HP')],
        [movesTeam1],
        [selectionTeam1],
        [trainerSelectionTeam1],
        [targetTeam1],
        [sg.Button('Submit', key='submit1')]
    ]

    # Layout for the bottom section (Team 2)
    team2_layout = [
        [sg.Text('Team 2', font=('Helvetica', 16))],
        [sg.Text('Name: N/A', key='team2PokemonName')],
        [sg.Text('HP: N/A', key='team2HP')],
        [movesTeam2],
        [selectionTeam2],
        [trainerSelectionTeam2],
        [targetTeam2],
        [sg.Button('Submit', key='submit2')]
    ]

    # Full window layout: Two rows with columns for team layouts
    layout = [
        [sg.Column(team1_layout, element_justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Column(team2_layout, element_justification='center')]
    ]
    return layout