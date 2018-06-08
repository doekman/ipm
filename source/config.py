import configparser, os, sys
from pathlib import Path

class IpmConfig:
	def __init__(self):
		self.config_file_name = '~/ipmconfig'
		self.config_file = os.path.expanduser(self.config_file_name)
		self.packmans = []

	def add(self, packman):
		self.packmans.append(packman)

def create_config(file_name):
	config_content = '''[ipm]
#Provide a path for the sync directory
data_dir =  ~/Dropbox (Persoonlijk)/ipm
#uncomment the package managers you want to use
#[brew]
#[cask]
#[pip]
#[pip3]
#[gem]
#[git]
#you can specify multiple locations, only the direct folders are checked if they contain git repositories
#location=~/Documents/GitHub
#[applications]
#you can specify multiple locations, only the direct folders are checked if they contain applications
#location=/Applications
#location=/Applications/Utilities
#location=~/Applications
'''
	with open(file_name, 'w') as configfile:
		print(config_content, file=configfile)


def read_config():
	cfg = IpmConfig()
	if not Path(cfg.config_file).exists():
		create_config(cfg.config_file)
		print('Please edit the configuration file {} and run the tool again'.format(cfg.config_file_name))
		exit(1)

	config = configparser.ConfigParser()
	config.read_file(open(cfg.config_file))

	if not 'ipm' in config:
		print('The [ipm] section is not defined in {}'.format(cfg.config_file_name), file=sys.stderr)
		exit(1)

	if not 'data_dir' in config['ipm']:
		print('The [ipm] section in {} does not contain the key "data_dir"'.format(cfg.config_file_name), file=sys.stderr)
		exit(1)

	data_dir_name = config['ipm']['data_dir']
	cfg.data_dir = os.path.expanduser(data_dir_name)
	if not Path(cfg.data_dir).is_dir():
		print('Data directory {} not found'.format(self.data_dir), file=sys.stderr)
		exit(1)

	pack_mans = ['brew', 'cask', 'pip', 'pip3', 'gem', 'git', 'applications']
	for pack_man in pack_mans:
		if pack_man in config:
			print('Doing {}'.format(pack_man))
			cfg.add(pack_man)
			#if pack_man in ['git', 'applications']:
	return cfg