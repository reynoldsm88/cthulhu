data_dir = 'data'
raw_data_dir = f'{data_dir}/raw'
preprocess_data_dir = f'{data_dir}/preprocess'


def inputln( display: str ):
    return input( f'{display}\n' )


def confirm_loop( text, op ):
    i = inputln( text )

    if i not in [ 'y', 'n' ]:
        confirm_loop( text, op )
    elif i is 'y':
        op()
    elif i is 'n':
        exit()
    else:
        print( 'you dont seem to understand yes or no... quitting' )
        exit( 1 )