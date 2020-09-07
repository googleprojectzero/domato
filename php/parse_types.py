import glob
import re
import sys

fun = re.compile(r"PHP_FUNCTION\((.+)\)")
met = re.compile(r"PHP_METHOD\(([^,]+), (.+)\)")
ftype = re.compile(r'zend_parse_parameters\([^,]+, "(.+)"')

in_func = False
in_meth = False
func = meth = obj = None
objs = set()


if len(sys.argv) != 2:
    print('Usage: %s /path/to/php/source/code' % sys.argv[0])
    sys.exit(1)

def l2f(fun, params):
    in_or = False
    p = []
    for param in params:
        if param in ['i', 'I']:
            p.append('<fuzzint>')
        if param in ['l', 'L', 'n', 'd']:
            p.append('<fuzznumber>')
        elif param in ['z', 'Z']:
            p.append('<fuzzref>')
        elif param in ['s', 'v', 'S']:
            p.append('<fuzzstring>')
        elif param in ['|']:
            in_or = True
            continue
        elif param in ['p', 'P']:
            p.append('<fuzzpath>')
        elif param in ['!', '/']:
            continue
        elif param in ['a', 'A', 'h', 'H']:
            p.append('<fuzzarray>')
        elif param in ['b']:
            p.append('<fuzzbool>')
        elif param in ['C']:
            p.append('<fuzzclass>')
        elif param in ['f']:
            p.append('<fuzzfunction>')
        elif param in ['o', 'O']:
            p.append('<fuzzobject>')
        elif param in ['r']:
            p.append('<fuzzresource>')
        if in_or is True:
            if in_func:
                print("<functioncall> = %s(%s)" % (func, ', '.join(p)))
            elif in_meth:
                print("<methodcall> = <obj_%s>->%s(%s)" % (obj, meth, ', '.join(p)))
    if in_or is False:
        if in_func:
            print("<functioncall> = %s(%s)" % (func, ', '.join(p)))
        elif in_meth:
            print("<methodcall> = <obj_%s>->%s(%s)" % (obj, meth, ', '.join(p)))

for fname in glob.glob(sys.argv[1] + '*/*/*.c'):
    with open(fname) as f:
        in_params = False
        in_or = False
        params = []

        for line in f.readlines():
            if in_func is False and in_meth is False:
                func = fun.search(line)
                if func:
                    in_func = True
                    func = func.group(1)
                    continue
                r = met.search(line)
                if r:
                    in_meth = True
                    obj = r.group(1)
                    objs.add(obj)
                    meth = r.group(2)
                continue

            if 'ZEND_PARSE_PARAMETERS_NONE' in line:
                print("<functioncall> = %s()" % (func if func else meth))
            elif 'ZEND_PARSE_PARAMETERS_END' in line:
                if in_func:
                    print("<functioncall> = %s(%s)" % (func, ', '.join(params)))
                    params = []
                    in_params = False
                    in_or = False
                elif in_meth:
                    print("<methodcall> = <obj_%s>->%s(%s)" % (obj, meth, ', '.join(params)))
                    params = []
                    in_params = False
                    in_or = False
                continue
            elif 'ZEND_PARSE_PARAMETERS_START' in line:
                in_params = True
                params = []
                continue

            if in_or is True:
                if in_func:
                    print("<functioncall> = %s(%s)" % (func, ', '.join(params)))
                elif in_meth:
                    print("<methodcall> = <obj_%s>->%s(%s)" % (obj, meth, ', '.join(params)))

            if in_params is True:
                if 'Z_PARAM_OPTIONAL' in line:
                    in_or = True
                elif 'Z_PARAM_OBJECT_OF_CLASS' in line:
                    params.append('<fuzzobject>')
                elif 'Z_PARAM_STR_OR_OBJ' in line:
                    params.append('<fuzzstring|obj>')
                elif 'Z_PARAM_STR_OR_ARRAY' in line:
                    params.append('<fuzzstring|array>')
                elif 'Z_PARAM_STR_OR_LONG' in line:
                    params.append('<fuzzstring|number>')
                elif 'Z_PARAM_OPTIONAL' in line:
                    in_or = True
                    continue
                elif 'Z_PARAM_LONG' in line or 'Z_PARAM_LONG_OR_NULL' in line:
                    params.append("<fuzznumber>")
                elif 'Z_PARAM_ARRAY_OR_OBJECT' in line:
                    params.append("<fuzzarray|object>")
                elif 'Z_PARAM_ARRAY' in line:
                    params.append("<fuzzarray>")
                elif 'Z_PARAM_OBJ' in line:
                    params.append("<fuzzobject>")
                elif 'Z_PARAM_ZVAL' in line:
                    params.append('<fuzzmixed>')
                elif 'Z_PARAM_BOOL' in line:
                    params.append('<fuzzbool>')
                elif 'Z_PARAM_CLASS' in line:
                    params.append('<fuzzclass>')
                elif 'Z_PARAM_CLASS_OR_OBJ' in line:
                    params.append('<fuzzclass|obj>')
                elif 'Z_PARAM_RESOURCE' in line:
                    params.append('<fuzzresource>')
                elif 'Z_PARAM_PATH' in line:
                    params.append('<fuzzpath>')
                elif 'Z_PARAM_NUMBER' in line:
                    params.append('<fuzznumber>')
                elif 'Z_PARAM_FUNC' in line:
                    params.append('<fuzzfunction>')
                elif 'Z_PARAM_DOUBLE' in line:
                    params.append('<fuzznumber>')
                elif 'Z_PARAM_PATH' in line:
                    params.append('<fuzzstring>')
                elif 'Z_PARAM_VARIADIC' in line:
                    params.append('<fuzzvariadic>')
                elif 'Z_PARAM_STR' in line:
                    params.append('<fuzzstring>')
                elif '_OR_' in line:
                    params.append('<fuzzmixed>')
                else:
                    print('err:' + line)


            p = ftype.search(line)
            if p:
                l2f(func, p.group(1))
                in_func = False
                in_meth = False
                in_params = False
                in_or = False
            elif line.startswith('}') or "/* }}} */" in line:
                in_func = False
                in_meth = False
                in_params = False
                in_or = False

print("\n")
for obj in objs:
    print('<obj_%s> = $vars["%s"]' % (obj, obj))

