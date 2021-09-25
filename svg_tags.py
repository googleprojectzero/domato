#   Domato - SVG types
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
