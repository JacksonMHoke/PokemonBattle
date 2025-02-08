# kwargs is a placeholder until I know what context moves will need for sure

# battlefield
# has 2 trainers
# ally array of active pokemon
# enemy array of active pokemon
# action queue maybe?
# fieldEffect(enum)?
## battlefield handles the moves and passes in relevant pokemon to moves

# trainer
# has array of pokemon
# has bag
# selectMove(pokemonIdx)

# pokemon
# name
# has array of types
# has array of moves
# hp, def, spD, att, spA, spe
# selectMove() returns move selected to trainer

# action(abstract)
# do(**kwargs)

# singleTargetAttackAction inherits from action
# do(**kwargs) attacks single target

# multiEnemyAttackAction inherits from action
# do(**kwargs) attacks all enemies

# allAttackAction inherits from action
# do(**kwargs) attacks all units except self

# buffStatAction(**kwargs) buffs stat

# move
# has array of types(for potential multi-type moves in future)
# power
# enact(**kwargs)
## moves will mainly use action classes as a way to enact and access data through kwargs context passed in through battlefield

# type(enum)
# global const effectivenessTable 2d array of type enum
#            - eTable[type1][type] = mult of type 1 attacking type 2