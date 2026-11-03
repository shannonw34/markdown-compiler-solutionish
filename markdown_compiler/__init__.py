"""
Functions that work on whole documents at a time.
All per-line work happens in compile_lines below.
"""
from markdown_compiler.util.line_functions import *


def compile_lines(text):
    '''
    Apply every markdown transformation to the input text.

    >>> compile_lines('This is a **bold** _italic_ `code` test.\\n')
    '<p>\\nThis is a <b>bold</b> <i>italic</i> <code>code</code> test.\\n</p>'

    >>> print(compile_lines("""
    ... # A header
    ...
    ... A paragraph with a [link](https://x).
    ... """))
    <BLANKLINE>
    <h1> A header</h1>
    <p>
    A paragraph with a <a href="https://x">link</a>.
    </p>
    '''
    lines = text.split('\n')
    new_lines = []
    in_paragraph = False
    for line in lines:
        line = line.strip()
        if line == '':
            if in_paragraph:
                line = '</p>'
                in_paragraph = False
        else:
            if line[0] != '#' and not in_paragraph:
                in_paragraph = True
                line = '<p>\n' + line
            line = compile_headers(line)
            line = compile_strikethrough(line)
            line = compile_bold_stars(line)
            line = compile_bold_underscore(line)
            line = compile_italic_star(line)
            line = compile_italic_underscore(line)
            line = compile_code_inline(line)
            line = compile_images(line)
            line = compile_links(line)
        new_lines.append(line)
    return '\n'.join(new_lines)


def markdown_to_html(markdown, add_css):
    '''
    Wrap compile_lines' output in the HTML boilerplate.

    >>> assert(markdown_to_html('this *is* a _test_', False))
    >>> assert(markdown_to_html('this *is* a _test_', True))
    '''
    html = '''
<html>
<head>
    <style>
    ins { text-decoration: line-through; }
    </style>
    '''
    if add_css:
        html += '''
<link rel="stylesheet" href="https://izbicki.me/css/code.css" />
<link rel="stylesheet" href="https://izbicki.me/css/default.css" />
        '''
    html += '''
</head>
<body>
    ''' + compile_lines(markdown) + '''
</body>
</html>
    '''
    return html


def minify(html):
    r'''
    Collapse runs of whitespace into a single space and strip.

    >>> minify('       ')
    ''
    >>> minify('   a    ')
    'a'
    >>> minify('   a    b        c    ')
    'a b c'
    >>> minify('a\\nb\\nc')
    'a b c'
    >>> minify('a \\nb\\n c')
    'a b c'
    '''
    return ' '.join(html.split())


def convert_file(input_file, add_css):
    '''
    Convert the markdown in input_file to HTML in the sibling .html file.
    '''
    if input_file[-3:] != '.md':
        raise ValueError('input_file does not end in .md')
    with open(input_file, 'r') as f:
        markdown = f.read()
    html = minify(markdown_to_html(markdown, add_css))
    with open(input_file[:-2] + 'html', 'w') as f:
        f.write(html)
