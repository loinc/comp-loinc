import sys

import typer


class CliClass:
    def __init__(self):
        self.typer = typer.Typer()

        self.typer.callback()(self.callback)
        self.typer.command()(self.main)

        self.custom = typer.Typer(chain=True)
        self.typer.add_typer(self.custom, name='custom')
        # self.typer.command(name='custom')(self.custom)

        self.custom.command()(self.custom_a)
        self.custom.command()(self.custom_b)

    def callback(self):
        print('Callback called')

    def main(self):
        print('Command main')

    def custom(self):
        print('Command custom')

    def custom_a(self, message: str = 'default custom a message'):
        print(message)

    def custom_b(self):
        print('Command custom b')


cli = CliClass()

if len(sys.argv) == 1:
    sys.argv.extend(['custom', 'custom-a', '--message', 'A', 'custom-b'])
cli.typer()
