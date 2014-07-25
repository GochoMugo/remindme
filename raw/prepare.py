'''
Prepares everything for jade to process
'''

import json

defaults_file = 'raw/defaults.json'
specifics_file = 'specifics.json'
output_file = 'out.json'

with open(defaults_file, 'r') as defaults_file:
    defaults = json.loads(defaults_file.read())
    with open(specifics_file, 'r+') as specifics_file:
        specifics = json.loads(specifics_file.read())
        defaults.update(specifics)
        with open(output_file, 'w') as output_file:
            output_file.write(json.dumps(defaults, indent=4))
