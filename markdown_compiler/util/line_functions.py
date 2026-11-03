'''
Each function takes a single line and transforms it in some way.

Four functions are stubs -- they return their input unchanged and must
be implemented.  Five are already implemented and must not be touched.
'''


def _pair(line, delim, open_tag, close_tag):
    '''
    Replace each alternating pair of delim with open_tag/close_tag.

    >>> _pair('a*b*c', '*', '<i>', '</i>')
    'a<i>b</i>c'
    >>> _pair('a*b', '*', '<i>', '</i>')
    'a<i>b'
    '''
    out, i, opened = '', 0, False
    while i < len(line):
        if line[i:i + len(delim)] == delim:
            out += close_tag if opened else open_tag
            opened = not opened
            i += len(delim)
        else:
            out += line[i]
            i += 1
    return out


def compile_headers(line):
    if not line.startswith('#'):
        return line

    level = len(line) - len(line.lstrip('#'))

    if level > 6 or line[level:level + 1] != ' ':
        return line

    return f'<h{level}>{line[level:]}</h{level}>'


def compile_italic_star(line):
    if line.count('*') % 2 != 0:
        return line
    return _pair(line, '*', '<i>', '</i>')


def compile_italic_underscore(line):
    return _pair(line, '_', '<i>', '</i>')


def compile_strikethrough(line):
    return _pair(line, '~~', '<ins>', '</ins>')


def compile_bold_stars(line):
    if line.count('**') % 2 != 0:
        return line
    return _pair(line, '**', '<b>', '</b>')


def compile_bold_underscore(line):
    return _pair(line, '__', '<b>', '</b>')


def compile_code_inline(line):
    out, inside, i = '', False, 0
    while i < len(line):
        if line[i:i + 3] == '```':
            out += '```'
            i += 3
            continue
        c = line[i]
        if c == '`':
            out += '</code>' if inside else '<code>'
            inside = not inside
        elif inside and c == '<':
            out += '&lt;'
        elif inside and c == '>':
            out += '&gt;'
        else:
            out += c
        i += 1
    return out


def compile_links(line):
    out = line
    while '[' in out and '](' in out:
        i = out.find('[')
        j = out.find('](', i)
        k = out.find(')', j)
        if j < 0 or k < 0:
            break
        out = out[:i] + f'<a href="{out[j+2:k]}">{out[i+1:j]}</a>' + out[k+1:]
    return out


def compile_images(line):
    out = ''
    i = 0

    while i < len(line):
        start = line.find('![', i)

        if start == -1:
            out += line[i:]
            break

        out += line[i:start]
        end_alt = line.find('](', start + 2)
        end_url = line.find(')', end_alt + 2) if end_alt != -1 else -1

        if end_alt == -1 or end_url == -1:
            out += line[start:]
            break

        alt = line[start + 2:end_alt]
        url = line[end_alt + 2:end_url]
        out += f'<img src="{url}" alt="{alt}" />'
        i = end_url + 1

    return out
