#   Domato - grammar parser and generator
#   --------------------------------------
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


import generator
import argparse
import os

def get_parser():
    
    parser = argparse.ArgumentParser(description="DOMATO (A DOM FUZZER)")
    
    parser.add_argument("-f", "--file", 
    help="File name which is to be generated in the same directory")

    parser.add_argument('-o', '--output_dir', type=str,
                    help='The output directory to put the generated files in')

    parser.add_argument('-n', '--no_of_files', type=int,
                    help='number of files to be generated')

    return parser

def main():

    with open(os.path.join(os.path.dirname(__file__), "template.html"), "r") as f:
            template = f.read()
            f.close()

    parser = get_parser()
    
    args = parser.parse_args()

    if args.file:
        with open(args.file, "w") as f:
            result = generator.generate_samples(template)
            f.write(result)

    elif args.output_dir:
        if not args.no_of_files:
            print("Please use switch -n to specify the number of files")
        else:
            print('Running on ClusterFuzz')
            out_dir = args.output_dir
            nsamples = args.no_of_files
            print('Output directory: ' + out_dir)
            print('Number of samples: ' + str(nsamples))

            if not os.path.exists(out_dir):
                os.mkdir(out_dir)

            outfiles = []
            for i in range(nsamples):
                outfiles.append(os.path.join(out_dir, 'fuzz-' + str(i).zfill(5) + '.html'))

            for outfile in outfiles:
                print('Writing a sample to ' + outfile)
                try:
                    with open(outfile, 'w') as f:
                        result = generator.generate_samples(template)
                        f.write(result)
                        f.close()
                except IOError:
                    print('Error writing to output')

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
