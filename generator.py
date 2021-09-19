from __future__ import print_function
import re
import random

from grammar import Grammar
from svg_tags import _SVG_TYPES
from html_tags import _HTML_TYPES

def generate_html_elements(ctx, n):
    for i in range(n):
        tag = random.choice(list(_HTML_TYPES))
        tagtype = _HTML_TYPES[tag]
        ctx['htmlvarctr'] += 1
        varname = 'htmlvar%05d' % ctx['htmlvarctr']
        ctx['htmlvars'].append({'name': varname, 'type': tagtype})
        ctx['htmlvargen'] += '/* newvar{' + varname + ':' + tagtype + '} */ var ' + varname + ' = document.createElement(\"' + tag + '\"); //' + tagtype + '\n'


def add_html_ids(matchobj, ctx):
    tagname = matchobj.group(0)[1:-1]
    if tagname in _HTML_TYPES:
        ctx['htmlvarctr'] += 1
        varname = 'htmlvar%05d' % ctx['htmlvarctr']
        ctx['htmlvars'].append({'name': varname, 'type': _HTML_TYPES[tagname]})
        ctx['htmlvargen'] += '/* newvar{' + varname + ':' + _HTML_TYPES[tagname] + '} */ var ' + varname + ' = document.getElementById(\"' + varname + '\"); //' + _HTML_TYPES[tagname] + '\n'
        return matchobj.group(0) + 'id=\"' + varname + '\" '
    elif tagname in _SVG_TYPES:
        ctx['svgvarctr'] += 1
        varname = 'svgvar%05d' % ctx['svgvarctr']
        ctx['htmlvars'].append({'name': varname, 'type': _SVG_TYPES[tagname]})
        ctx['htmlvargen'] += '/* newvar{' + varname + ':' + _SVG_TYPES[tagname] + '} */ var ' + varname + ' = document.getElementById(\"' + varname + '\"); //' + _SVG_TYPES[tagname] + '\n'
        return matchobj.group(0) + 'id=\"' + varname + '\" '
    else:
        return matchobj.group(0)


def generate_function_body(jsgrammar, htmlctx, num_lines):
    js = ''
    js += 'var fuzzervars = {};\n\n'
    js += "SetVariable(fuzzervars, window, 'Window');\nSetVariable(fuzzervars, document, 'Document');\nSetVariable(fuzzervars, document.body.firstChild, 'Element');\n\n"
    js += '//beginjs\n'
    js += htmlctx['htmlvargen']
    js += jsgrammar._generate_code(num_lines, htmlctx['htmlvars'])
    js += '\n//endjs\n'
    js += 'var fuzzervars = {};\nfreememory()\n'
    return js


def check_grammar(grammar):
    """Checks if grammar has errors and if so outputs them.
    Args:
      grammar: The grammar to check.
    """

    for rule in grammar._all_rules:
        for part in rule['parts']:
            if part['type'] == 'text':
                continue
            tagname = part['tagname']
            # print tagname
            if tagname not in grammar._creators:
                print('No creators for type ' + tagname)


def generate_new_sample(template, htmlgrammar, cssgrammar, jsgrammar):
    """Parses grammar rules from string.
    Args:
      template: A template string.
      htmlgrammar: Grammar for generating HTML code.
      cssgrammar: Grammar for generating CSS code.
      jsgrammar: Grammar for generating JS code.
    Returns:
      A string containing sample data.
    """

    result = template

    css = cssgrammar.generate_symbol('rules')
    html = htmlgrammar.generate_symbol('bodyelements')

    htmlctx = {
        'htmlvars': [],
        'htmlvarctr': 0,
        'svgvarctr': 0,
        'htmlvargen': ''
    }
    html = re.sub(
        r'<[a-zA-Z0-9_-]+ ',
        lambda match: add_html_ids(match, htmlctx),
        html
    )
    generate_html_elements(htmlctx, 5)

    result = result.replace('<cssfuzzer>', css)
    result = result.replace('<htmlfuzzer>', html)

    handlers = False
    while '<jsfuzzer>' in result:
        numlines = 1000
        if handlers:
            numlines = 500
        else:
            handlers = True
        result = result.replace(
            '<jsfuzzer>',
            generate_function_body(jsgrammar, htmlctx, numlines),
            1
        )

    return result

def import_grammar():
    
    htmlgrammar = Grammar()
    err = htmlgrammar.parse_from_file('rules/html.txt')
    # CheckGrammar(htmlgrammar)
    if err > 0:
        print('There were errors parsing html grammar')
        return

    cssgrammar = Grammar()
    err = cssgrammar.parse_from_file('rules/css.txt')
    # CheckGrammar(cssgrammar)
    if err > 0:
        print('There were errors parsing css grammar')
        return

    jsgrammar = Grammar()
    err = jsgrammar.parse_from_file('rules/js.txt')
    # CheckGrammar(jsgrammar)
    if err > 0:
        print('There were errors parsing js grammar')
        return

    # JS and HTML grammar need access to CSS grammar.
    # Add it as import
    htmlgrammar.add_import('cssgrammar', cssgrammar)
    jsgrammar.add_import('cssgrammar', cssgrammar)

    return htmlgrammar, cssgrammar, jsgrammar

def generate_samples(template):
    """Generates a set of samples and writes them to the output files.
    Args:
      grammar_dir: directory to load grammar files from.
      outfiles: A list of output filenames.
    """
    return generate_new_sample(template, *import_grammar())