#   Domato - generator script for WebGPU
#   -------------------------------
#
#   Written and maintained by Ivan Fratric <ifratric@google.com>
#   Modified by Brendon Tiszka to target webgpu <tiszka@google.com>
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
import glob
import os
import random
import re
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(parent_dir)
from grammar import Grammar

_N_MAIN_LINES = 1000
_N_SHADERS = 10

def extract_shader_stages_and_functions(code):
    # Pattern to match both single-line and multiline stage attributes
    pattern = r'@(?:compute|vertex|fragment)(?:\s+@[^(\n]+(?:\([^)]*\))?)*\s*(?:\n\s*)?fn\s+(\w+)'
    matches = re.finditer(pattern, code)
    
    # Extract stage-function pairs
    result = []
    for match in matches:
        # Find the stage attribute within the matched attributes
        stage_attr = re.search(r'@(compute|vertex|fragment)', match.group(0)).group(0)
        function_name = match.group(1)
        result.append((stage_attr, function_name))
    
    return result

def parse_entrypoints(shaders):
    entrypoints = []
    for shader in shaders:
        attr_fn_pairs = extract_shader_stages_and_functions(shader)
        for attr, fn in attr_fn_pairs:
            entrypoints.append(fn)

    result = ""
    for entrypoint in entrypoints:
        result += "<entrypoint> = \"{}\"\n".format(entrypoint)    

    return result

def parse_bindings(shaders):
    binding_pattern = r'@binding\((\d+)\)'
    
    binding_numbers = []
    for shader in shaders:
        matches = re.finditer(binding_pattern, shader)
        binding_numbers.extend(match.group(1) for match in matches)
    
    return "\n".join(f"<BindInt> = {binding}" for binding in binding_numbers)

def generate_function_body(webgpugrammar, num_lines):
    js = ''
    js += webgpugrammar._generate_code(num_lines)

    return js

def generate_new_sample(template, webgpugrammar):
    result = template
    while '<webgpufuzz>' in result:
        result = result.replace(
            '<webgpufuzz>',
            generate_function_body(webgpugrammar, _N_MAIN_LINES),
            1
        )

    return result


def generate_samples(template, grammar_dir, outfiles):
    extra = ""
    shaders_dir = os.path.join(grammar_dir, "wgsl/*.wgsl")
    shader_files = glob.glob(shaders_dir)

    shaders = []
    for i in range(_N_SHADERS):
        shader_path = random.choice(shader_files)
        with open(shader_path) as fp:
            shader_src = fp.read()
            shaders.append(shader_src)
    
    with open(os.path.join(grammar_dir, template), "r") as fp:
        template_contents = fp.read()

    SHADER_CONST = "<shader%s>"
    for i, shader in enumerate(shaders):
        shader_template = SHADER_CONST % str(i)
        template_contents = template_contents.replace(shader_template, shader)

    extra += parse_entrypoints(shaders) + "\n"
    extra += parse_bindings(shaders) + "\n"

    webgpugrammar = Grammar()
    err = webgpugrammar.parse_from_file(os.path.join(grammar_dir, os.path.join(grammar_dir, 'webgpu.txt')), extra)
    if err > 0:
        print('There were errors parsing grammar')
        return

    for outfile in outfiles:
        result = generate_new_sample(template_contents, webgpugrammar)

        if result is not None:
            print('Writing a sample to ' + outfile)
            try:
                with open(outfile, 'w') as f:
                    f.write(result)
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
    template = os.path.join(fuzzer_dir, "template.html")

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
        generate_samples(template, fuzzer_dir, outfiles)
    else:
        print('Arguments missing')
        print("Usage:")
        print("""--input_dir <directory>. ** not used. **
                --output_dir <directory>. This is the output directory which the fuzzer should write to.
                --no_of_files <n>. This is the number of testcases which the fuzzer should write to the output directory.
                """)

if __name__ == '__main__':
    main()
