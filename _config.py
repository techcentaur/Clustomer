"""YAML read configuration"""

from yaml import (safe_load, YAMLError)

with open("_config.yml", 'r') as ymlfile:
	try:
		yml_data = safe_load(ymlfile)
	except YAMLError as err:
		print(err)