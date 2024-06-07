from params import *


# workout_standing = workout_transition + workout_standing
def change_actions(x):
    if x in idle_standing:
        return 'idle_standing'
    elif x in idle_sitting:
        return 'idle_sitting'
    elif x in idle_lyingdown:
        return 'idle_lyingdown'
    elif x in workout_standing:
        return 'workout_standing'
    elif x in workout_transition:
        return 'workout_transition'
    elif x in workout_lyingdown:
        return 'workout_lyingdown'
    elif x in workout_yoga_strectching:
        return 'yoga/strectching'
    elif x in remove_spe:
        return 'remove'
    elif x in doubt:
        return "doubt"
    else:
        return x

