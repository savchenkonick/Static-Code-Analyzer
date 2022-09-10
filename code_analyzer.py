r"""Static Code Analyzer
A simple static analyzer tool that finds common stylistic issues in Python code.
    Code is analyzed with the help of Abstract Syntactic Tree (AST)
and Regular expressions.

All the names of function arguments as well as local variables are checked
to meet the requirements of PEP8:
[S010] Argument name arg_name should be written in snake_case;
[S011] Variable var_name should be written in snake_case;
[S012] The default argument value is mutable.
The program does not force the names of
variables outside of functions (for example, in modules or classes).
This realized with the AST from the ast module.

Scrypt takes path to file as argument.
Example:
python code_analyzer.py my_module.py

use -h for help

Issues that can be found:
'S001': 'Too long',
'S002': 'Indentation is not a multiple of four',
'S003': 'Unnecessary semicolon after a statement',
'S004': 'Less than two spaces before inline comments',
'S005': 'TODO found',
'S006': 'More than two blank lines preceding a code line',
'S007': 'Too many spaces after construction_name (def or class)',
'S008': 'Class name class_name should be written in CamelCase',
'S009': 'Function name function_name should be written in snake_case',
'S010': 'Argument name arg_name should be written in snake_case',
'S011': 'Variable var_name should be written in snake_case',
'S012': 'The default argument value is mutable'

"""

import argparse
import os
import re
import ast
from pathlib import Path


class CodeAnalyzer:
    def __init__(self, input_path):
        self.input_path = input_path
        self.preceding_blank_lines = 0
        self.current_path = ''
        self.issues = {'S001': 'Too long',
                       'S002': 'Indentation is not a multiple of four',
                       'S003': 'Unnecessary semicolon after a statement',
                       'S004': 'Less than two spaces before inline comments',
                       'S005': 'TODO found',
                       'S006': 'More than two blank lines preceding a code line',
                       'S007': 'Too many spaces after construction_name (def or class)',
                       'S008': 'Class name class_name should be written in CamelCase',
                       'S009': 'Function name function_name should be written in snake_case',
                       'S010': 'Argument name arg_name should be written in snake_case',
                       'S011': 'Variable var_name should be written in snake_case',
                       'S012': 'The default argument value is mutable'
                       }
        self.result = {}

    def output(self, line_number, code):
        try:
            self.result[str(self.current_path)].append((line_number, code))
        except KeyError:
            self.result[str(self.current_path)] = [(line_number, code)]

    def len_check(self, line, line_number):
        code = 'S001'
        if len(line.rstrip('\n')) > 79:
            self.output(line_number, code)

    def ident_check(self, line, line_number):
        code = 'S002'
        ident_counter = 0
        for letter in line:
            if letter != ' ':
                break
            ident_counter += 1
        if ident_counter > 0 and (ident_counter % 4) != 0:
            self.output(line_number, code)

    def semicolon_check(self, line, line_number):
        code = 'S003'
        line = line.split('#')
        line = line[0].rstrip()
        if len(line) > 0:
            if line[-1] == ';':
                self.output(line_number, code)

    def two_spaces_check(self, line, line_number):
        code = 'S004'
        if line[0] == '#':
            return None
        line = line.split('#')
        if len(line) > 1 and line[0][-2:] != '  ':
            self.output(line_number, code)

    def todo_check(self, line, line_number):
        code = 'S005'
        line = line.split('#')
        if len(line) > 1:
            del line[0]
            for part in line:
                if 'todo' in part.lower():
                    self.output(line_number, code)
                    break

    def blank_lines_check(self, line, line_number):
        code = 'S006'
        if line.rstrip('\n') == '':
            self.preceding_blank_lines += 1
            return None
        if self.preceding_blank_lines > 2:
            self.preceding_blank_lines = 0
            self.output(line_number, code)
        elif 0 < self.preceding_blank_lines <= 2:
            self.preceding_blank_lines = 0

    def def_spaces_check(self, line, line_number):
        code = 'S007'
        def_template = r'[^#]? *_?_?def {2,}'
        class_template = r'[^#]? *class {2,}'
        if re.match(def_template, line) or re.match(class_template, line):
            self.output(line_number, code)

    def class_naming_check(self, line, line_number):
        code = 'S008'
        lwrcase_template = r' *class +[a-z]'
        undscr_template = r' *class +[a-zA-z]+_'
        if re.match(lwrcase_template, line) or re.match(undscr_template, line):
            self.output(line_number, code)

    def function_naming_check(self, line, line_number):
        code = 'S009'
        template = r' *def +[a-z0-9_]*[A-Z]'
        if re.match(template, line):
            self.output(line_number, code)

    def arguments_check(self, file_path):
        template = r'.*[A-Z]'
        file = open(file_path).read()
        tree = ast.parse(file)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                mutable_found = False
                args = [a.arg for a in node.args.args]
                args_default = [a for a in node.args.defaults]
                # check if arg in snake_case
                for arg in args:
                    if re.match(template, arg):
                        self.output(node.lineno, 'S010')
                # check if def arg is mutable:
                for def_arg in args_default:
                    if not mutable_found:
                        mutable_found = True
                        if type(def_arg).__name__ != 'Constant':
                            self.output(node.lineno, 'S012')
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    try:
                        target.__dict__['id']
                    except KeyError:
                        pass
                    else:
                        if re.match(template, target.__dict__['id']):
                            self.output(node.lineno, 'S011')

    def check_file(self, file_path):
        with open(file_path) as file:
            line_number = 1
            for line in file:
                # line_stripped = line.rstrip('\n')
                self.len_check(line, line_number)
                self.ident_check(line, line_number)
                self.semicolon_check(line, line_number)
                self.two_spaces_check(line, line_number)
                self.todo_check(line, line_number)
                self.blank_lines_check(line, line_number)
                self.def_spaces_check(line, line_number)
                self.class_naming_check(line, line_number)
                self.function_naming_check(line, line_number)
                line_number += 1
        self.arguments_check(file_path)

    def check_path(self):
        if os.path.isfile(self.input_path):
            self.current_path = Path(self.input_path)
            self.check_file(self.current_path)
        else:
            basepath = Path(self.input_path)
            files = (entry for entry in basepath.iterdir() if entry.is_file())
            for file in files:
                if file.name.endswith('.py'):
                    self.current_path = file
                    self.check_file(file)

    def print_result(self):
        sorted_files = sorted(self.result)
        for file_name in sorted_files:
            for line in self.result[file_name]:
                print(f'{file_name}: Line {line[0]}: {line[1]} {self.issues[line[1]]}')


def analyzer():
    parser = argparse.ArgumentParser(description='Script takes path to file or '
                                                 'folder and tests it py files')
    parser.add_argument('path', type=str, help='path to folder of file name')
    args = parser.parse_args()
    return args.path


if __name__ == '__main__':
    path = analyzer()
    # path = 'my_module.py'
    python_file = CodeAnalyzer(path)
    python_file.check_path()
    python_file.print_result()
