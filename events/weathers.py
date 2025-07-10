# from events.event import Weather
# from globals import *
# from random import random
# from events.statuses import Burned
# from behaviors.executionBehaviors import StatusSingleTarget

# class Rain(Weather):
#     """Weather effect that buffs water moves by 25%."""
#     def __init__(self):
#         triggers=[Trigger.BEFORE_MOVE, Trigger.AFTER_MOVE, Trigger.END_TURN_STATUS]
#         super().__init__(self.__class__.__name__, triggers)
#         self.remainingTurns=4
#         self.powerBuff=0.25
#         self.buffedThisMove=False
#         self.color='blue'
    
#     def trigger(self, battleContext, eventContext, trigger):
#         if trigger==Trigger.BEFORE_MOVE and battleContext.move.type==Type.WATER:
#             eventContext.attackMult+=self.powerBuff
#             battleContext.window['combatLog'].update(f'Rain buffs the moves power by {self.powerBuff} multiplier!\n', append=True)
#             self.buffedThisMove=True
#         if trigger==Trigger.AFTER_MOVE and self.buffedThisMove:
#             eventContext.attackMult-=self.powerBuff
#             self.buffedThisMove=False
#         if trigger==Trigger.END_TURN_STATUS:
#             self.remainingTurns-=1
#             if self.remainingTurns<=0:
#                 battleContext.window['combatLog'].update(f'Rain ended!\n', append=True)
#                 battleContext.weather=None

# class MagmaStorm(Weather):              # TODO: Event handler to order events and multi status behavior
#     """Weather effect that causes burn on everyone every turn and deals 15 damage. Ends after 4 turns."""
#     def __init__(self):
#         triggers=[Trigger.END_TURN_STATUS]
#         super().__init__(self.__class__.__name__, triggers)
#         self.remainingTurns=4
#         self.dmgPerTurn=15
#         self.color='red'
    
#     def trigger(self, battleContext, eventContext, trigger):
#         if trigger==Trigger.END_TURN_STATUS:
#             for team in battleContext.teams:
#                 for slot in team.slots:
#                     if slot.pokemon is None:
#                         continue
#                     battleContext.setDefenders([slot])
#                     StatusSingleTarget.do(battleContext, inflictedStatus=Burned())
#                     slot.pokemon.takeDamage(self.dmgPerTurn, battleContext)

#             self.remainingTurns-=1
#             if self.remainingTurns<=0:
#                 battleContext.window['combatLog'].update(f'Magma storm has ended!\n', append=True)
#                 battleContext.weather=None