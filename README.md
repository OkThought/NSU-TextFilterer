# TextFilterer
A command line tool to filter text (formulas, special symbols, etc)

## Why?
Sometimes you need to extract some useful stuff from text and you start by simply removing something definately unwanted from the text. This tool is intended to help you with that by providing a simple cmd util with some predefined patterns to filter out of text. 

Originally, its idea is to remove mathematical formulas from text. And as programmers usually do, I prepared solution to this problem so that it can be extended.

## How to use?

First, to be able to run it you need python 3.x installed. You may find how to do this here: https://wiki.python.org/moin/BeginnersGuide/Download

1. To filter setnences with formulas like `a+b=c` from file 'example.txt' and save the filtered text in file 'result.txt' all you need to do is:

`$ filter_text.py example.txt result.txt`

2. To see help pass -h or --help flag as usually:

```
$ pdf2txt.py -h
usage: filter_text.py [-h] [--sentence-delimiters [char [char ...]]]
                      [--operation-chars [char [char ...]]]
                      [--keep-sentences-with-formulas]
                      [--skip-chars [char [char ...]]]
                      [src] [dst]

positional arguments:
  src                   file to filter. By default stdin.
  dst                   filtered file. By default stdout or
                        "<src_file_path>-filtered.<src_file_extension>" if src
                        is specified.

optional arguments:
  -h, --help            show this help message and exit
  --sentence-delimiters [char [char ...]]
                        characters indicating sentence endings and beginnings.
                        By default: ".!?"
  --operation-chars [char [char ...]]
                        characters of which math operations consist. By
                        default: +=*<>≤≥|^
  --keep-sentences-with-formulas
                        when specified does not filter sentences with
                        formulas.
  --skip-chars [char [char ...]]
                        characters not written to dst. By default: "#@$\\`"

```

3. The tool uses stdin and stdout by default so you can use it by piping output from another command, for example:

`$ pdf2txt.py file.pdf | filter_text`

## Contact
The project was originally made for my teacher, Aigerim Bakieva, and I don't maintain it. But if you find it useful and want to have something added/fixed/changed, do not hezitate to write me a letter to my educational email: bogush@g.nsu.ru (Ivan Bogush).
