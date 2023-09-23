import ctypes
import subprocess
import webbrowser

code_page = str(ctypes.windll.kernel32.GetConsoleOutputCP())
response = subprocess.check_output('py -0').decode(code_page)
versions = [line.split()[0].split(':')[1] for line in response.splitlines() if 'Python' in line]
print(f'Python versions: {versions}')

for version in versions:
    command = f'py -{version} -m pip freeze > packages-{version}.txt'
    print(f'Executing: {command}')
    subprocess.check_call(command, shell=True)

command = 'matcher --format html --output out.html packages-*.txt'
print(f'Executing: {command}')
subprocess.check_call(command, shell=True)
webbrowser.open('out.html')
