import argparse
import functools
import inspect
import os
import re
import stat
import sys
import textwrap
import types

from inspect import Parameter, Signature


def asbool(value):
    if value in [True, 'true', 'TRUE', 'on', 'yes', '1']:
        return True
    if value in [False, 'false', 'FALSE', 'off', 'no', '0']:
        return False
    raise Exception(f'Unhandled boolean value: {value}')


class FlyCLI():
    def __call__(self, obj):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='_command', metavar='command', required=True)
        methods = inspect.getmembers(obj, inspect.ismethod)

        if not methods:
            raise Exception('No methods found on the class')

        boolean_arguments = []

        for (name, method) in methods:
            if name[0] == '_':
                continue

            method_help = f'{name} command.'
            parameter_docs = {}

            if method.__doc__:
                doc = method.__doc__.strip()

                [method_doc, *param_parts] = re.split(' *:param', doc)
                method_help = textwrap.dedent(method_doc)

                if param_parts:
                    param_parts[0] = ':param %s' % param_parts[0]

                parameter_parts = ':param'.join(param_parts).split("\n")
                for part in parameter_parts:
                    match = re.match(r':param\s+([^:]*)\s*:\s*(.*)', part)
                    if match:
                        [parameter_name, parameter_doc] = match.group(1, 2)
                        parameter_docs[parameter_name] = parameter_doc

            subparser = subparsers.add_parser(name, help=method_help)
            for parameter in inspect.signature(method).parameters.values():
                help = []
                kwargs = {}
                if parameter.annotation and parameter.annotation is not Signature.empty:
                    kwargs['type'] = parameter.annotation
                    if kwargs['type'] is bool:
                        boolean_arguments.append(parameter.name)
                if parameter.name in parameter_docs:
                    help.append(parameter_docs[parameter.name])
                if parameter.default is not Signature.empty:
                    default = parameter.default
                    if kwargs['type'] is bool:
                        kwargs['type'] = str
                        default = 'yes' if default else 'no'
                    kwargs['default'] = default
                    help.append(f'Default is "{default}".')
                if help:
                    kwargs['help'] = ' '.join(help)

                if parameter.kind == Parameter.POSITIONAL_ONLY or parameter.default is Signature.empty:
                    subparser.add_argument(parameter.name, **kwargs)
                else:
                    subparser.add_argument(f'--{parameter.name}', **kwargs)

        args = vars(parser.parse_args(sys.argv[1:]))

        for key, value in args.items():
            if key in boolean_arguments:
                args[key] = asbool(value)

        command = args.pop('_command')
        return getattr(obj, command)(**args)

    def stub(self, signature: str, filename: str, overwrite: bool = False):
        """
        Generate a stub script for calling methods on a class instance.

        :param signature: Signature of the class, like module:class or module.module:class.
        :param filename: The stub is generated into this file.
        """
        (module, cls) = signature.split(':')

        imports = ''
        if module != 'fly':
            imports = f'from {module} import {cls}'

        contents = textwrap.dedent(f"""\
        #!/usr/bin/env python
        from fly_cli import FlyCLI
        {imports}


        def main():
            fly = FlyCLI()
            fly({cls}())

        if __name__ == '__main__':
            main()""")

        with open(filename, 'w') as f:
            f.write(contents)

        os.chmod(filename, os.stat(filename).st_mode | stat.S_IXUSR | stat.S_IXGRP)


def main():
    fly = FlyCLI()
    fly(fly)


if __name__ == '__main__':
    main()
