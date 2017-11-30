''' Builder definitions for Rust Cargo '''

cargo = {
    'sig': r'Cargo\.toml|Cargo\.lock',
    'cmd': 'cargo build',
    'func': None,
    'ft': ['rust'],
    'subdir': None,
    'shell': False
}
