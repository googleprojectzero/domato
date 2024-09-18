# Simple WebGPU fuzzer

## Setup

1. Populate the `wgsl/` directory with wgsl scripts. I would recomment copying wgsl test files from [tint's tests](https://source.chromium.org/chromium/chromium/src/+/main:third_party/dawn/test/tint/bug/).
2. From here, the usage is the same as [vanilla Domato's](https://github.com/googleprojectzero/domato).

## Bugs
Chrome: [40063883](https://issues.chromium.org/u/0/issues/40063883), [40063356](https://issues.chromium.org/u/0/issues/40063356)

## Building Grammars
This repo also contains a helper script that can be used to assist in generating Domato grammars using Chrome's [WebIDL compiler](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/bindings/scripts/web_idl/README.md;l=1?q=f:md%20web_idl&sq=). It is far from complete but may help others generate grammars faster.
