''' Builder definitions for Go Build '''

# TODO: I'm not sure if we want go build or go install... This also seems like a dumb thing,
# having a signature that will match *every* directory. Maybe there's a better option?
go_build = {
    'sig': r'',
    'cmd': 'go build',
    'func': None,
    'ft': ['go'],
    'subdir': None,
    'shell': False
}
