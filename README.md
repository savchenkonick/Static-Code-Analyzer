# Static Code Analyzer
> A simple static analyzer tool that finds common stylistic issues in Python code.
Code is analyzed with the help of Abstract Syntactic Tree (AST)
and Regular expressions.

## Table of Contents
* [About](#About)
* [Examples](#Examples)
* [Technologies Used](#technologies-)
* [Github Link](#Github-link)


## About
All the names of function arguments as well as local variables are checked to meet the requirements of PEP8:

[S010] Argument name arg_name should be written in snake_case;

[S011] Variable var_name should be written in snake_case;

[S012] The default argument value is mutable.

The program does not force the names of variables outside of functions (for example, in modules or classes). This realized with the AST from the ast module.

Scrypt takes path to file as argument.

## Examples:
python code_analyzer.py my_module.py

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

## Technologies Used
- Python v3.6 or more
- Abstract Syntactic Tree (AST)
- Regular expressions (RE)

## Github link
https://github.com/savchenkonick/Static-Code-Analyzer
