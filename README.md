# Domato 🍅
#### A DOM fuzzer

Written and maintained by Ivan Fratric, <ifratric@google.com>

Copyright 2017 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

#### Usage

To see the usage information run the following command:

`python3 generator.py --help`

To generate a single .html sample run:

`python generator.py --file <output file>`

To generate a single .html sample run using a template you wrote:

`python generator.py --file <output file> --template <your custom template file>`

To generate multiple samples with a single call run:

`python generator.py --output_dir <output directory> --no_of_files <number of output files>`

The generated samples will be placed in the specified directory and will be named as fuzz-&lt;number&gt;.html, e.g. fuzz-00001.html, fuzz-00002.html etc. Generating multiple samples is faster because the input grammar files need to be loaded and parsed only once.

#### Code organization

generator.py contains the main script. It uses grammar.py as a library and contains additional helper code for DOM fuzzing.

grammar.py contains the generation engine that is mostly application-agnostic and can thus be used in other (i.e. non-DOM) generation-based fuzzers. As it can be used as a library, its usage is described in a separate section below.

.txt files contain grammar definitions. There are 3 main files, html.txt, css.txt and js.txt which contain HTML, CSS and JavaScript grammars, respectively. These root grammar files may include content from other files.

#### Using the generation engine and writing grammars

To use the generation engine with a custom grammar, you can use the following python code:

```
from grammar import Grammar

my_grammar = Grammar()
my_grammar.parse_from_file('input_file.txt')
result_string = my_grammar.generate_symbol('symbol_name')

```

The following sections describe the syntax of the grammar files.

##### Basic syntax

Domato is based on an engine that, given a context-free grammar in a simple format specified below, generates samples from that grammar.

A grammar is described as a set of rules in the following basic format:

`<symbol> = a mix of constants and <other_symbol>s`

Each grammar rule contains a left side and the right side separated by the equal character. The left side contains a symbol, while the right side contains the details on how that symbol may be expanded. When expanding a symbol, all symbols on the right-hand side are expanded recursively while everything that is not a symbol is simply copied to the output. Note that a single rule can't span over multiple lines of the input file.

Consider the following simplified example of a part of the CSS grammar:

```
<cssrule> = <selector> { <declaration> }
<selector> = a
<selector> = b
<declaration> = width:100%
```

If we instruct the grammar engine to parse that grammar and generate 'cssrule', we may end up with either:

`a { width:100% }`

or

`b { width:100% }`

Note there are two rules for the 'selector' symbol. In such cases, when the generator is asked to generate a 'selector', it will select the rule to use at random. It is also possible to specify the probability of the rule using the 'p' attribute, for example:

```
<selector p=0.9> = a
<selector p=0.1> = b
```

In this case, the string 'a' would be output more often than 'b'.

There are other attributes that can be applied to symbols in addition to the probability. Those are listed in a separate section.

Consider another example for generating html samples:

```
<html> = <lt>html<gt><head><body><lt>/html<gt>
<head> = <lt>head<gt>...<lt>/head<gt>
<body> = <lt>body<gt>...<lt>/body<gt>
```

Note that since the '<' and '>' have a special meaning in the grammar syntax, so here we are using `<lt>` and `<gt>` instead. These symbols are built in and don't need to be defined by the user. A list of all built-in symbols is provided in a separate section.

##### Generating programming language code

To generate programming language code, a similar syntax can be used, but there are a couple of differences. Each line of the programming language grammar is going to correspond to the line of the output. Because of that, the grammar syntax is going to be more free-form to allow expressing constructs in various programming languages. Secondly, when a line is generated, in addition to outputting the line, one or more variables may be created and those variables may be reused when generating other lines. Again, let's take a look of the simplified example:

```
!varformat fuzzvar%05d
!lineguard try { <line> } catch(e) {}

!begin lines
<new element> = document.getElementById("<string min=97 max=122>");
<element>.doSomething();
!end lines
```

If we instruct the engine to generate 5 lines, we may end up with something like:

```
try { var00001 = document.getElementById("hw"); } catch(e) {}
try { var00001.doSomething(); } catch(e) {}
try { var00002 = document.getElementById("feezcqbndf"); } catch(e) {}
try { var00002.doSomething(); } catch(e) {}
try { var00001.doSomething(); } catch(e) {}
```

Note that

- programming language lines are enclosed in '!begin lines' and '!end lines' statement. This gives the grammar parser the necessary information that the lines in-between are programming language lines and are thus parsed differently.
- We used `<new element>` instead of `<element>`. This instructs the generator to create a new variable of type 'element' instead of generating the 'element' symbol.
- `<string>` is one of the built-in symbols so no need to define it.
- [optional] You can use !varformat statement to define the format of variables you want to use.
- [optional] You can use !lineguard statement to define additional code that gets inserted around every line in order to catch exceptions or perform other tasks. This is so you wouldn't need to write it for every line separately.
- In addition to '!begin lines' and '!end lines' you can also use '!begin helperlines' and '!end helperlines' to define lines of code that will only ever be used if required when generating other lines (for example, helper lines might generate variables needed by the 'main' code, but you don't ever want those helper lines to end up in the output when they are not needed).

##### Comments

Everything after the first '#' character on the line is considered a comment, so for example:

```
#This is a comment
```


##### Preventing infinite recursions

The grammar syntax has a way of telling the fuzzer which rules are nonrecursive and can be safe to use even if the maximum level of recursion has been reached. This is done with the ‘nonrecursive’ attributes. An example is given below.

```
!max_recursion 10
<test root=true> = <foobar>
<foobar> = foo<foobar>
<foobar nonrecursive> = bar
```

Firstly, an optional ‘!max_recursion’ statement defines the maximum recursion depth level (50 by default). Notice that the second production rule for ‘foobar’ is marked as non-recursive. If ever the maximum recursion level is reached the generator will force using the non-recursive rule for ‘foobar’ symbol, thus preventing infinite recursion.

##### Including and importing other grammar files

In Domato, including and importing grammars are two different context.

Including is simpler. You can use:

```
!include other.txt
```

to include rules from other.txt into the currently parsed grammar.

Importing works a bit differently:

```
!import other.txt
```

tells the parser to create a new Grammar() object that can then be referenced from the current grammar by using the special `<import>` symbol, for example like this:

```
<cssrule> = <import from=css.txt symbol=rule>
```

You can think about importing and including in terms of namespaces: !include will put the included grammar into the single namespace, while !import will create a new namespace which can then be accessed using the `<import>` symbol and the namespace specified via the 'from' attribute.

##### Including Python code

Sometimes you might want to call custom Python code in your grammar. For example, let’s say you want to use the engine to generate a http response and you want the body length to match the 'Size' header. Since this is something not possible with normal grammar rules, you can include custom Python code to accomplish it like this:

```
!begin function savesize
  context['size'] = ret_val
!end function

!begin function createbody
  n = int(context['size'])
  ret_val = 'a' * n
!end function

<foo root> = <header><cr><lf><body>
<header> = Size: <int min=1 max=20 beforeoutput=savesize>
<body> = <call function=createbody>
```

The python functions are defined between ‘!begin function <function_name>’ and ‘!end function’ commands. The functions can be called in two ways: using ‘beforeoutput’ attribute and using `<call>` symbol.

By specifying the ‘beforeoutput’ attribute in some symbol, the corresponding function will be called when this symbol is expanded, just before the result of the expansion is output to the sample. The expansion result will be passed to the function in the ret_val variable. The function is then free to modify ret_val, store it for later use or perform any other operations.

When using a special `<call>` symbol, the function (specified in a ‘function’ attribute) will be called when the symbol is encountered during language generation. Any value stored by the function in ret_val will be considered the result of the expansion (ret_val gets included in the sample).

Your python code has access to the following variables:

- `context` - a dictionary that is passed through the whole sample generation. You can use it to store values (such as storing the size in an example above) and retrieve them in the rules that fire subsequently.
- `attributes` - a dictionary corresponding to the symbol currently being processed. You can use it to pass parameters to your functions. For example if you used something like `<call function=func foo=bar>` to call your function attributes\[‘foo’\] will be set to ‘bar’.
- `ret_val` - The value that will be output as a result of the function call. It is initialized to an empty value when using `<call>` symbol to call a function, otherwise it will be initialized to the value generated by the symbol.

##### Built-in symbols

The following symbols have a special meaning and should not be redefined by users:

- `<lt>` - ‘<’ character
- `<gt>` - ‘>’ character
- `<hash>` - ‘#’ character
- `<cr>` - CR character
- `<lf>` - LF character
- `<space>` - space character
- `<tab>` - tab character
- `<ex>` - ‘!’ character
- `<char>` - can be used to generate an arbitrary ascii character using ‘code’ attribute. For example `<char code=97>` corresponds to ‘a’. Generates random character if not specified. Supports ‘min’ and ‘max’ attribute.
- `<hex>` - generates a random hex digit.
- `<int>`, `<int 8>`, `<uint8>`, `<int16>`, `<uint16>`, `<int32>`, `<uint32>`, `<int64>`, `<uint64>` - can be used to generate random integers. Supports ‘min’ and ‘max’ attribute that can be used to limit the range of integers that will be generated. Supports the ‘b’ and ‘be’ attribute which makes the output binary in little/big endian format instead of text output.
- `<float>`, `<double>` - generates a random floating-point number. Supports ‘min’ and ‘max’ attribute (0 and 1 if not specified). Supports ‘b’ attribute which makes the output binary.
- `<string>` - generates a random string. Supports ‘min’ and ‘max’ attributes which control the minimum and maximum charcode generated as well as ‘minlength’ and ‘maxlength’ attributes that control the length of the string.
- `<htmlsafestring>` - same as `<string>` except HTML metacharacters will be escaped, making it safe to embed the string as part of HTML text or attribute values.
- `<lines>` - outputs the given number (via ‘count’ attribute) lines of code. See the section on generating programming language code for example.
- `<import>` - imports a symbol from another grammar, see the section on including external grammars for details.
- `<call>` - calls a user-defined function corresponding to the function attribute. See the section on including Python code in the grammar for more info.

##### Symbol attributes

The following attributes are supported:

- root - marks a symbol as the root symbol of the grammar. The only supported value is ‘true’. When GenerateSymbol() is called, if no argument is specified, the root symbol will be generated.
- nonrecursive - gives the generator a hint that this rule doesn’t contain recursion loops and is used to prevent infinite recursions. The only supported value is ‘true’.
- new - used when generating programming languages to denote that a new variable is created here rather than expanding the symbol as usual. The only supported value is ‘true’.
- from, symbol - used when importing symbols from other grammars, see ‘Including external grammars’ section.
- count - used in lines symbol to specify the number of lines to be created.
- id - used to mark that several symbols should share the same value. For example in the rule `‘doSomething(<int id=1>, <int id=1>)’` both ints would end up having the same value. Only the first instance is actually expanded, the second is just copied from the first.
- min, max - used in generation of numeric types to specify the minimum and maximum value. Also used to limit the set of characters generated in strings.
- b, be - used in numeric types to specify binary little-endian (‘b’) or big-endian (‘be’) output.
- code - used in char symbol to specify the exact character to output by its code.
- minlength, maxlength - used when generating strings to specify the minimum and maximum length.
- up - used in hex symbol to specify uppercase output (lowercase is the default).
- function - used in the `<call>` symbol, see ‘Including Python code’ section for more info.
- beforeoutput - used to call user-specified functions, see ‘Including Python’.

#### Bug Showcase

Some of the bugs that have been found with Domato:

 - Apple Safari: CVE-2017-2369, CVE-2017-2373, CVE-2017-2362, CVE-2017-2454, CVE-2017-2455, CVE-2017-2459, CVE-2017-2460, CVE-2017-2466, CVE-2017-2471, CVE-2017-2476, CVE-2017-7039, CVE-2017-7040, CVE-2017-7041, CVE-2017-7042, CVE-2017-7043, CVE-2017-7046, CVE-2017-7048, CVE-2017-7049, CVE-2017-13796, CVE-2017-13792, CVE-2017-13797, CVE-2017-13795, CVE-2017-13785, CVE-2017-13784, CVE-2017-13783, CVE-2017-13802, CVE-2017-13794, CVE-2017-13798, CVE-2017-13791, CVE-2018-4089, CVE-2018-4200, CVE-2018-4197, CVE-2018-4318, CVE-2018-4317, CVE-2018-4314, CVE-2018-4306, CVE-2018-4312, CVE-2018-4315, CVE-2018-4323, CVE-2018-4328
 - Google Chrome: Issues 666246 and 671328
 - Microsoft Internet Explorer 11: CVE-2017-0037, CVE-2017-0059, CVE-2017-0202, CVE-2017-8594, CVE-2018-0866
 - Microsoft Edge: CVE-2017-0037, CVE-2017-8496, CVE-2017-8652, CVE-2017-8644
 - Microsoft JScript: CVE-2017-11903, CVE-2017-11855, CVE-2017-11793, CVE-2017-11906, CVE-2017-11907, CVE-2018-0935, CVE-2018-8353, CVE-2018-8631
 - Microsoft VBScript: CVE-2018-8544, CVE-2018-8552, CVE-2018-8625
 - Mozilla Firefox: CVE-2017-5404, CVE-2017-5447, CVE-2017-5465

#### Disclaimer

This is not an official Google product.

