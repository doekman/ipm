import subprocess, sys, re, shlex

class BasePackMan:
	def __init__(self, name):
		self.name = name

	def do_shell_script(self, cmd):
		try:
			result = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			value = result.stdout.strip().decode("UTF-8")
		except:
			print("Error executing: "+cmd, file=sys.stderr)
			value = None
		return value

	def parse_lines(self, lines, regex):
		result = []
		for line in lines.splitlines():
			match = regex.match(line)
			if match!=None:
				result.append( match.groupdict() )
		return result

	def run_and_parse(self, cmd, regex):
		return self.parse_lines(self.do_shell_script(cmd), regex)

#gem:	regex = re.compile(r'^(?P<name>\w+) \((?P<version>[^)]+\))$')

brew_regex = re.compile(r'^(?P<name>\w+) (?P<version>.+)$')
app_regex = re.complile(r'^(?P<name>.+)$')

class BrewPackMan(BasePackMan):
	def list_all(self):
		return self.run_and_parse('brew list --versions', brew_regex)

class CaskPackMan(BasePackMan):
	def list_all(self):
		return self.run_and_parse('brew cask list --versions', brew_regex)

class ApplicationsPackMan(BasePackMan):
	def __init__(self, name, locations):
		super().__init__(name)
		self.locations = locations

	def list_all(self):
		return [(location,self.list_group(location)) for location in self.locations]

	def list_group(self, location):
		return self.run_and_parse('cd {}; ls -d *.app'.format(shlex.quote(location)), app_regex)


#gem list --local

class GroupedTablularData:
	def save(self, filename, data):
		