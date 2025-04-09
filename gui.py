import FreeSimpleGUI as sg
from globals import *

def resizeWindow(window):
    window.TKroot.update_idletasks()  # Force TKinter to process all pending events
    new_width = window.TKroot.winfo_reqwidth()
    new_height = window.TKroot.winfo_reqheight()
    window.TKroot.geometry(f"{new_width}x{new_height}")

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
    # movesTeam1=sg.Column([[sg.Text('Select a Move:')], [sg.Combo(['Move1', 'Move2'], readonly=True, key='team1MoveChoice')]], visible=False, key='team1MoveOptions')
    # movesTeam2=sg.Column([[sg.Text('Select a Move:')], [sg.Combo(['Move1', 'Move2'], readonly=True, key='team2MoveChoice')]], visible=False, key='team2MoveOptions')
    # trainerSelectionTeam1=sg.Column([[sg.Text('Select a Trainer:')], [sg.Combo(['T1', 'T2'], readonly=True, key='team1TrainerChoice')]], visible=False, key='team1TrainerOptions')
    # trainerSelectionTeam2=sg.Column([[sg.Text('Select a Trainer:')], [sg.Combo(['T1', 'T2'], readonly=True, key='team2TrainerChoice')]], visible=False, key='team2TrainerOptions')
    # selectionTeam1=sg.Column([[sg.Text('Select a Pokémon:')], [sg.Combo(['Pikachu', 'Charmander', 'Bulbasaur', 'Squirtle'], key='team1PokemonChoice', readonly=True)]], visible=False, key='team1PokemonOptions')
    # selectionTeam2=sg.Column([[sg.Text('Select a Pokémon:')], [sg.Combo(['Pikachu', 'Charmander', 'Bulbasaur', 'Squirtle'], key='team2PokemonChoice', readonly=True)]], visible=False, key='team2PokemonOptions')
    # targetTeam1=sg.Column([[sg.Text('Select a Target:')], [sg.Combo(['Target1', 'Target2'], readonly=True, key='team1TargetChoice')]], visible=False, key='team1TargetOptions')
    # targetTeam2=sg.Column([[sg.Text('Select a Target:')], [sg.Combo(['Target1', 'Target2'], readonly=True, key='team2TargetChoice')]], visible=False, key='team2TargetOptions')

    team1DD=sg.Column([[sg.Text('Select a _', key='team1DDTitle')], [sg.Combo(['choice 1', 'choice 2'], readonly=True, key='team1DDChoice')], [sg.Button('Submit', key='submit1')]], visible=False, key='team1DD')
    team2DD=sg.Column([[sg.Text('Select a _', key='team2DDTitle')], [sg.Combo(['choice 1', 'choice 2'], readonly=True, key='team2DDChoice')], [sg.Button('Submit', key='submit2')]], visible=False, key='team2DD')


    team1_layout = [
        [sg.Text('Team 1', font=('Helvetica', 16))],
        [sg.Text('Name: N/A', key='team1PokemonName')],
        [sg.Text('HP: N/A', key='team1HP')],
        [team1DD]
    ]

    # Layout for the bottom section (Team 2)
    team2_layout = [
        [sg.Text('Team 2', font=('Helvetica', 16))],
        [sg.Text('Name: N/A', key='team2PokemonName')],
        [sg.Text('HP: N/A', key='team2HP')],
        [team2DD]
    ]

    # Full window layout: Two rows with columns for team layouts
    layout = [
        [sg.Column(team1_layout, element_justification='center')],
        [sg.HorizontalSeparator()],
        [sg.Column(team2_layout, element_justification='center')]
    ]
    return layout