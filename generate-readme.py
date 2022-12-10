import os
import inspect
import importlib

def generate_readme(project_dir):
	project_name = os.path.basename(project_dir)
	files = os.listdir(project_dir)
	entry_point = None
	for file in files:
		if file.endswith('.py'):
			with open(os.path.join(project_dir, file), 'r') as f:
				if 'def main(' in f.read():
					entry_point = file
					break

	# Generate a requirements.txt file containing the dependencies of the project.
	dependencies = set()
	for file in files:
		if file.endswith('.py'):
			with open(os.path.join(project_dir, file), 'r') as f:
				for line in f:
					words = line.split()
					for word in words:
						if word == 'import':
							dependencies.add(words[words.index(word)+1])
						elif 'from' in words and words[words.index('from')+1] not in dependencies:
							dependencies.add(words[words.index('from')+1])

	# Write the dependencies to the requirements.txt file.
	with open(os.path.join(project_dir, 'requirements.txt'), 'w') as f:
		for dependency in dependencies:
			f.write('{}\n'.format(dependency))

	# Write the README.md file.
	with open(os.path.join(project_dir, 'README.md'), 'w') as f:
		f.write('# {}\n\n'.format(project_name))
		f.write('This is a Python project containing the following files:\n\n')
		for file in files:
			f.write('- {}\n'.format(file))
		f.write('\n## Dependencies\n\n')
		f.write('This project requires the following libraries to be installed:\n\n')

		# Write the instructions to install the required libraries.
		f.write('To install the required libraries, run the following command:\n\n')
		f.write('```\n')
		f.write('pip install -r requirements.txt\n')
		f.write('```\n\n')
		f.write('## Running the code\n\n')
		f.write('To run the project, use the following command:\n\n')
		f.write('```\n')
		f.write('python {}\n'.format(entry_point))
		f.write('```\n\n')
		f.write('## Features\n\n')
		f.write('This project includes the following features:\n\n')
		for name, obj in inspect.getmembers(project_dir):
			if inspect.isfunction(obj) and obj.__doc__:
				f.write('- {}: {}\n'.format(name, obj.__doc__))

project_dir = input('Enter the path to your Python project directory: ')
generate_readme(project_dir)
