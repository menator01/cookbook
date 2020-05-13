#! /usr/bin/env python3.8

def time_converter(arg):
    '''Convert minutes to hours if above 60'''
    hours, minutes = divmod(arg, 60)
    if arg > 60:
        if hours > 1:
            var = f'{hours} hrs. {minutes} min.'
        else:
            var = f'{hours} hr. {minutes} min.'
    elif arg == 60:
        var = f'{hours} hr.'
    else:
        var = f'{minutes} min.'
    return var
