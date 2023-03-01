# fly-cli

Invoke object methods from the command-line. WIP.

## install

Add this package to your dependencies in requirements.txt or use pip install:

```
pip install fly-cli
```

## usage

Let's say you have a class `Greeter` in module `app` (`app.py`) that you want to create a CLI for:

```
class Greeter:
    def greet(name, greeting='hi there'):
        """
        Greet someone by name.

        :param name: The name of the person to be greeted.
        :param greeting: The greeting message to use.
        """
        print(f'{greeting}, {name}')
```

Run this command to generate a stub:

```
fly stub app:Greeter greeter
```

This will create a binary called `greeter` with the following contents:

```
#!/usr/bin/env python
from fly_cli import FlyCLI
from app import Greeter


def main():
    fly = FlyCLI()
    fly(Greeter())

if __name__ == '__main__':
    main()
```

The `FlyCLI` class inspects the object and generates a sub-command for each method, analysing the method parameters to add arguments to the parser.

Now you can run the script to call an instance of the class:

```
> ./greeter greet --greeting="hola" bob
hola, bob
```

Edit the script to add constructor arguments or configuration if required.

Help text is generated from method documentation, parsing Sphinx parameter declarations, type declarations and default values to generate argument help.

Listing subcommands:
```
./greeter --help
usage: greeter [-h] command ...

positional arguments:
  command
    greet     Greet someone by name.

optional arguments:
  -h, --help  show this help message and exit
```

Subcommand help:
```
> ./greeter greet --help
usage: greeter greet [-h] [--greeting GREETING] name

positional arguments:
  name                 The name of the person to be greeted.

optional arguments:
  -h, --help           show this help message and exit
  --greeting GREETING  The greeting message to use. Default is "hi there".
```

To add more subcommands, add more methods on the class.

If you add type annotations to your parameters, it will coerce the values into the specified type when parsing arguments.

Boolean parameters become string arguments accepting various forms of truthiness: on, off, yes, no, 1, 0, true, false. This is converted to a boolean before the method is called.

`fly-cli` eats its own dogfood, the console script `fly` wraps the `FlyCLI` class.
