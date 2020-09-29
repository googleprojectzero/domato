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

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from grammar import Grammar

_N_MAIN_LINES = 1000
_N_EVENTHANDLER_LINES = 500


def generate_new_sample(template, phpgrammar):
    """Parses grammar rules from string.

    Args:
      template: A template string.
      phpgrammar: Grammar for generating PHPcode.

    Returns:
      A string containing sample data.
    """

    result = template
    handlers = False
    while '<phpfuzzer>' in result:
        numlines = _N_MAIN_LINES
        if handlers:
            numlines = _N_EVENTHANDLER_LINES
        else:
            handlers = True
        result = result.replace(
            '<phpfuzzer>',
            phpgrammar._generate_code(numlines),
            1
        )

    return result


def generate_samples(grammar_dir, outfiles):
    """Generates a set of samples and writes them to the output files.

    Args:
      grammar_dir: directory to load grammar files from.
      outfiles: A list of output filenames.
    """

    f = open(os.path.join(grammar_dir, 'template.php'))
    template = f.read()
    f.close()

    phpgrammar = Grammar()
    err = phpgrammar.parse_from_file(os.path.join(grammar_dir, 'php.txt'))
    if err > 0:
        print('There were errors parsing grammar')
        return

    for outfile in outfiles:
        result = generate_new_sample(template, phpgrammar)

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
            outfiles.append(os.path.join(out_dir, 'fuzz-' + str(i).zfill(5) + '.php'))

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
