Script and grammar for fuzzing Canvas API based on CanvasRenderingContext2D specification found at https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D

*** Example usage ***

Running the generate_one_case.py script will yield a sample fuzzed case:

```
ctx.clearHitRegions();
/* newvar{fuzzvar00001:path2d} */ var fuzzvar00001 = new Path2D('M1 0 H -1 V 0 H 10 L 1 1');
if (!fuzzvar00001) { fuzzvar00001 = GetVariable(fuzzervars, 'path2d'); } else { SetVariable(fuzzvar00001, 'path2d');  }
ctx.stroke(fuzzvar00001);
console.log(ctx.isPointInPath(fuzzvar00001, 1073741824, 2147483647, "nonzero"));
console.log(ctx.isPointInStroke(fuzzvar00001, -2147483648, 2147483647));
ctx.stroke(fuzzvar00001);
ctx.fill(fuzzvar00001, "evenodd");
console.log(ctx.isPointInPath(fuzzvar00001, -1, 0, "nonzero"));
console.log(ctx.isPointInStroke(fuzzvar00001, -1073741824, 2147483648));
console.log(ctx.isPointInStroke(fuzzvar00001, 536870912, 268435456));
console.log(ctx.isPointInStroke(fuzzvar00001, 268435456, -32769));
ctx.clip(fuzzvar00001, "nonzero");
/* newvar{fuzzvar00002:path2d} */ var fuzzvar00002 = new Path2D(fuzzvar00001);
if (!fuzzvar00002) { fuzzvar00002 = GetVariable(fuzzervars, 'path2d'); } else { SetVariable(fuzzvar00002, 'path2d');  }
console.log(ctx.isPointInPath(fuzzvar00002, -32769, 32768, "nonzero"));
ctx.clip(fuzzvar00002, "nonzero");
console.log(ctx.isPointInPath(fuzzvar00001, -32769, 268435456, "evenodd"));
ctx.clip(fuzzvar00001, "nonzero");
ctx.bezierCurveTo(-2147483648, -2147483648, 268435456, 4294967295, 2147483647, 65535);
ctx.fill(fuzzvar00001, "nonzero");
ctx.fill(fuzzvar00001, "evenodd");
/* newvar{fuzzvar00003:path2d} */ var fuzzvar00003 = new Path2D(fuzzvar00002);
if (!fuzzvar00003) { fuzzvar00003 = GetVariable(fuzzervars, 'path2d'); } else { SetVariable(fuzzvar00003, 'path2d');  }
```

Your mileage may vary so feel free to modify/edit template.html.


