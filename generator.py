#   Domato - main generator script
#   -------------------------------
#
#   Written and maintained by Ivan Fratric <ifratric@google.com>
#
#   Copyright 2017 Google Inc. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


from __future__ import print_function
import os
import re
import random
import sys

from grammar import Grammar

_N_MAIN_LINES = 1000
_N_EVENTHANDLER_LINES = 500

_N_ADDITIONAL_HTMLVARS = 5

# A map from tag name to corresponding type for HTML tags
_HTML_TYPES = {
    'a': 'HTMLAnchorElement',
    'abbr': 'HTMLUnknownElement',
    'acronym': 'HTMLUnknownElement',
    'address': 'HTMLUnknownElement',
    'applet': 'HTMLUnknownElement',
    'area': 'HTMLAreaElement',
    'article': 'HTMLUnknownElement',
    'aside': 'HTMLUnknownElement',
    'audio': 'HTMLAudioElement',
    'b': 'HTMLUnknownElement',
    'base': 'HTMLBaseElement',
    'basefont': 'HTMLUnknownElement',
    'bdi': 'HTMLUnknownElement',
    'bdo': 'HTMLUnknownElement',
    'bgsound': 'HTMLUnknownElement',
    'big': 'HTMLUnknownElement',
    'blockquote': 'HTMLUnknownElement',
    'br': 'HTMLBRElement',
    'button': 'HTMLButtonElement',
    'canvas': 'HTMLCanvasElement',
    'caption': 'HTMLTableCaptionElement',
    'center': 'HTMLUnknownElement',
    'cite': 'HTMLUnknownElement',
    'code': 'HTMLUnknownElement',
    'col': 'HTMLTableColElement',
    'colgroup': 'HTMLUnknownElement',
    'command': 'HTMLUnknownElement',
    'content': 'HTMLContentElement',
    'data': 'HTMLDataElement',
    'datalist': 'HTMLDataListElement',
    'dd': 'HTMLUnknownElement',
    'del': 'HTMLModElement',
    'details': 'HTMLDetailsElement',
    'dfn': 'HTMLUnknownElement',
    'dialog': 'HTMLDialogElement',
    'dir': 'HTMLDirectoryElement',
    'div': 'HTMLDivElement',
    'dl': 'HTMLDListElement',
    'dt': 'HTMLUnknownElement',
    'em': 'HTMLUnknownElement',
    'embed': 'HTMLEmbedElement',
    'fieldset': 'HTMLFieldSetElement',
    'figcaption': 'HTMLUnknownElement',
    'figure': 'HTMLUnknownElement',
    'font': 'HTMLFontElement',
    'footer': 'HTMLUnknownElement',
    'form': 'HTMLFormElement',
    'frame': 'HTMLFrameElement',
    'frameset': 'HTMLFrameSetElement',
    'h1': 'HTMLHeadingElement',
    'h2': 'HTMLHeadingElement',
    'h3': 'HTMLHeadingElement',
    'h4': 'HTMLHeadingElement',
    'h5': 'HTMLHeadingElement',
    'h6': 'HTMLHeadingElement',
    'header': 'HTMLUnknownElement',
    'hgroup': 'HTMLUnknownElement',
    'hr': 'HTMLHRElement',
    'i': 'HTMLUnknownElement',
    'iframe': 'HTMLIFrameElement',
    'image': 'HTMLImageElement',
    'img': 'HTMLImageElement',
    'input': 'HTMLInputElement',
    'ins': 'HTMLModElement',
    'isindex': 'HTMLUnknownElement',
    'kbd': 'HTMLUnknownElement',
    'keygen': 'HTMLKeygenElement',
    'label': 'HTMLLabelElement',
    'layer': 'HTMLUnknownElement',
    'legend': 'HTMLLegendElement',
    'li': 'HTMLLIElement',
    'link': 'HTMLLinkElement',
    'listing': 'HTMLUnknownElement',
    'main': 'HTMLUnknownElement',
    'map': 'HTMLMapElement',
    'mark': 'HTMLUnknownElement',
    'marquee': 'HTMLMarqueeElement',
    'menu': 'HTMLMenuElement',
    'menuitem': 'HTMLMenuItemElement',
    'meta': 'HTMLMetaElement',
    'meter': 'HTMLMeterElement',
    'nav': 'HTMLUnknownElement',
    'nobr': 'HTMLUnknownElement',
    'noembed': 'HTMLUnknownElement',
    'noframes': 'HTMLUnknownElement',
    'nolayer': 'HTMLUnknownElement',
    'noscript': 'HTMLUnknownElement',
    'object': 'HTMLObjectElement',
    'ol': 'HTMLOListElement',
    'optgroup': 'HTMLOptGroupElement',
    'option': 'HTMLOptionElement',
    'output': 'HTMLOutputElement',
    'p': 'HTMLParagraphElement',
    'param': 'HTMLParamElement',
    'picture': 'HTMLPictureElement',
    'plaintext': 'HTMLUnknownElement',
    'pre': 'HTMLPreElement',
    'progress': 'HTMLProgressElement',
    'q': 'HTMLQuoteElement',
    'rp': 'HTMLUnknownElement',
    'rt': 'HTMLUnknownElement',
    'ruby': 'HTMLUnknownElement',
    's': 'HTMLUnknownElement',
    'samp': 'HTMLUnknownElement',
    'section': 'HTMLUnknownElement',
    'select': 'HTMLSelectElement',
    'shadow': 'HTMLShadowElement',
    'small': 'HTMLUnknownElement',
    'source': 'HTMLSourceElement',
    'span': 'HTMLSpanElement',
    'strike': 'HTMLUnknownElement',
    'strong': 'HTMLUnknownElement',
    'style': 'HTMLStyleElement',
    'sub': 'HTMLUnknownElement',
    'summary': 'HTMLUnknownElement',
    'sup': 'HTMLUnknownElement',
    'table': 'HTMLTableElement',
    'tbody': 'HTMLTableSectionElement',
    'td': 'HTMLUnknownElement',
    'template': 'HTMLTemplateElement',
    'textarea': 'HTMLTextAreaElement',
    'tfoot': 'HTMLTableSectionElement',
    'th': 'HTMLTableCellElement',
    'thead': 'HTMLTableSectionElement',
    'time': 'HTMLTimeElement',
    'title': 'HTMLTitleElement',
    'tr': 'HTMLTableRowElement',
    'track': 'HTMLTrackElement',
    'tt': 'HTMLUnknownElement',
    'u': 'HTMLUnknownElement',
    'ul': 'HTMLUListElement',
    'var': 'HTMLUnknownElement',
    'video': 'HTMLVideoElement',
    'wbr': 'HTMLUnknownElement',
    'xmp': 'HTMLUnknownElement'
}

# A map from tag name to corresponding type for SVG tags
_SVG_TYPES = {
    'a': 'SVGAElement',
    'altGlyph': 'SVGElement',
    'altGlyphDef': 'SVGElement',
    'altGlyphItem': 'SVGElement',
    'animate': 'SVGAnimateElement',
    'animateColor': 'SVGElement',
    'animateMotion': 'SVGAnimateMotionElement',
    'animateTransform': 'SVGAnimateTransformElement',
    'circle': 'SVGCircleElement',
    'clipPath': 'SVGClipPathElement',
    'color-profile': 'SVGElement',
    'cursor': 'SVGCursorElement',
    'defs': 'SVGDefsElement',
    'desc': 'SVGDescElement',
    'discard': 'SVGDiscardElement',
    'ellipse': 'SVGEllipseElement',
    'feBlend': 'SVGFEBlendElement',
    'feColorMatrix': 'SVGFEColorMatrixElement',
    'feComponentTransfer': 'SVGFEComponentTransferElement',
    'feComposite': 'SVGFECompositeElement',
    'feConvolveMatrix': 'SVGFEConvolveMatrixElement',
    'feDiffuseLighting': 'SVGFEDiffuseLightingElement',
    'feDisplacementMap': 'SVGFEDisplacementMapElement',
    'feDistantLight': 'SVGFEDistantLightElement',
    'feDropShadow': 'SVGFEDropShadowElement',
    'feFlood': 'SVGFEFloodElement',
    'feFuncA': 'SVGFEFuncAElement',
    'feFuncB': 'SVGFEFuncBElement',
    'feFuncG': 'SVGFEFuncGElement',
    'feFuncR': 'SVGFEFuncRElement',
    'feGaussianBlur': 'SVGFEGaussianBlurElement',
    'feImage': 'SVGFEImageElement',
    'feMerge': 'SVGFEMergeElement',
    'feMergeNode': 'SVGFEMergeNodeElement',
    'feMorphology': 'SVGFEMorphologyElement',
    'feOffset': 'SVGFEOffsetElement',
    'fePointLight': 'SVGFEPointLightElement',
    'feSpecularLighting': 'SVGFESpecularLightingElement',
    'feSpotLight': 'SVGFESpotLightElement',
    'feTile': 'SVGFETileElement',
    'feTurbulence': 'SVGFETurbulenceElement',
    'filter': 'SVGFilterElement',
    'font': 'SVGElement',
    'font-face': 'SVGElement',
    'font-face-format': 'SVGElement',
    'font-face-name': 'SVGElement',
    'font-face-src': 'SVGElement',
    'font-face-uri': 'SVGElement',
    'foreignObject': 'SVGForeignObjectElement',
    'g': 'SVGGElement',
    'glyph': 'SVGElement',
    'glyphRef': 'SVGElement',
    'hatch': 'SVGElement',
    'hatchpath': 'SVGElement',
    'hkern': 'SVGElement',
    'image': 'SVGImageElement',
    'line': 'SVGLineElement',
    'linearGradient': 'SVGLinearGradientElement',
    'marker': 'SVGMarkerElement',
    'mask': 'SVGMaskElement',
    'mesh': 'SVGElement',
    'meshgradient': 'SVGElement',
    'meshpatch': 'SVGElement',
    'meshrow': 'SVGElement',
    'metadata': 'SVGMetadataElement',
    'missing-glyph': 'SVGElement',
    'mpath': 'SVGMPathElement',
    'path': 'SVGPathElement',
    'pattern': 'SVGPatternElement',
    'polygon': 'SVGPolygonElement',
    'polyline': 'SVGPolylineElement',
    'radialGradient': 'SVGRadialGradientElement',
    'rect': 'SVGRectElement',
    'set': 'SVGSetElement',
    'svg': 'SVGSVGElement',
    'solidcolor': 'SVGElement',
    'stop': 'SVGStopElement',
    'switch': 'SVGSwitchElement',
    'symbol': 'SVGSymbolElement',
    'text': 'SVGTextElement',
    'textPath': 'SVGTextPathElement',
    'title': 'SVGTitleElement',
    'tref': 'SVGElement',
    'tspan': 'SVGTSpanElement',
    'unknown': 'SVGElement',
    'use': 'SVGUseElement',
    'view': 'SVGViewElement',
    'vkern': 'SVGElement'
}


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
    generate_html_elements(htmlctx, _N_ADDITIONAL_HTMLVARS)

    result = result.replace('<cssfuzzer>', css)
    result = result.replace('<htmlfuzzer>', html)

    handlers = False
    while '<jsfuzzer>' in result:
        numlines = _N_MAIN_LINES
        if handlers:
            numlines = _N_EVENTHANDLER_LINES
        else:
            handlers = True
        result = result.replace(
            '<jsfuzzer>',
            generate_function_body(jsgrammar, htmlctx, numlines),
            1
        )

    return result


def generate_samples(grammar_dir, outfiles):
    """Generates a set of samples and writes them to the output files.

    Args:
      grammar_dir: directory to load grammar files from.
      outfiles: A list of output filenames.
    """

    f = open(os.path.join(grammar_dir, 'template.html'))
    template = f.read()
    f.close()

    htmlgrammar = Grammar()
    err = htmlgrammar.parse_from_file(os.path.join(grammar_dir, 'html.txt'))
    # CheckGrammar(htmlgrammar)
    if err > 0:
        print('There were errors parsing grammar')
        return

    cssgrammar = Grammar()
    err = cssgrammar.parse_from_file(os.path.join(grammar_dir, 'css.txt'))
    # CheckGrammar(cssgrammar)
    if err > 0:
        print('There were errors parsing grammar')
        return

    jsgrammar = Grammar()
    err = jsgrammar.parse_from_file(os.path.join(grammar_dir, 'js.txt'))
    # CheckGrammar(jsgrammar)
    if err > 0:
        print('There were errors parsing grammar')
        return

    # JS and HTML grammar need access to CSS grammar.
    # Add it as import
    htmlgrammar.add_import('cssgrammar', cssgrammar)
    jsgrammar.add_import('cssgrammar', cssgrammar)

    for outfile in outfiles:
        result = generate_new_sample(template, htmlgrammar, cssgrammar,
                                     jsgrammar)

        if result is not None:
            print('Writing a sample to ' + outfile)
            try:
                f = open(outfile, 'w')
                f.write(result)
                f.close()
            except IOError:
                print('Error writing to output')


def get_option(option_name):
    for i in range(len(sys.argv)):
        if (sys.argv[i] == option_name) and ((i + 1) < len(sys.argv)):
            return sys.argv[i + 1]
        elif sys.argv[i].startswith(option_name + '='):
            return sys.argv[i][len(option_name) + 1:]
    return None


def main():
    fuzzer_dir = os.path.dirname(__file__)

    multiple_samples = False

    for a in sys.argv:
        if a.startswith('--output_dir='):
            multiple_samples = True

    if '--output_dir' in sys.argv:
        multiple_samples = True

    if multiple_samples:
        print('Running on ClusterFuzz')
        out_dir = get_option('--output_dir')
        nsamples = int(get_option('--no_of_files'))
        print('Output directory: ' + out_dir)
        print('Number of samples: ' + str(nsamples))

        if not os.path.exists(out_dir):
            os.mkdir(out_dir)

        outfiles = []
        for i in range(nsamples):
            outfiles.append(os.path.join(out_dir, 'fuzz-' + str(i).zfill(5) + '.html'))

        generate_samples(fuzzer_dir, outfiles)

    elif len(sys.argv) > 1:
        outfile = sys.argv[1]
        generate_samples(fuzzer_dir, [outfile])

    else:
        print('Arguments missing')
        print("Usage:")
        print("\tpython generator.py <output file>")
        print("\tpython generator.py --output_dir <output directory> --no_of_files <number of output files>")


if __name__ == '__main__':
    main()
