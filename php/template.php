<?php

function templateFunction($templateParameter) {
	return 0;
}

function templateGenerator() {
	yield 0;
}

class TemplateClass {
	var $templateProperty;
	const TEMPLATE_CONSTANT = 0;
	function templateMethod() {
		return 0;
	}
}

$vars = array(
	"stdClass"                       => new stdClass(),
	"Exception"                      => new Exception(),
	"ErrorException"                 => new ErrorException(),
	"Error"                          => new Error(),
	"CompileError"                   => new CompileError(),
	"ParseError"                     => new ParseError(),
	"TypeError"                      => new TypeError(),
	"ArgumentCountError"             => new ArgumentCountError(),
	"ArithmeticError"                => new ArithmeticError(),
	"DivisionByZeroError"            => new DivisionByZeroError(),
	"ClosedGeneratorException"       => new ClosedGeneratorException(),
	"DateTime"                       => new DateTime(),
	"DateTimeImmutable"              => new DateTimeImmutable(),
	"DateTimeZone"                   => new DateTimeZone("America/Chicago"),
	"DateInterval"                   => new DateInterval("P2Y4DT6H8M"),
	"DatePeriod"                     => new DatePeriod("R4/2012-07-01T00:00:00Z/P7D"),
	"LibXMLError"                    => new LibXMLError(),
	"DOMException"                   => new DOMException(),
	"DOMStringList"                  => new DOMStringList(),
	"DOMNameList"                    => new DOMNameList(),
	"DOMImplementationList"          => new DOMImplementationList(),
	"DOMImplementationSource"        => new DOMImplementationSource(),
	"DOMImplementation"              => new DOMImplementation(),
	"DOMNode"                        => new DOMNode(),
	"DOMNameSpaceNode"               => new DOMNameSpaceNode(),
	"DOMDocumentFragment"            => new DOMDocumentFragment(),
	"DOMDocument"                    => new DOMDocument(),
	"DOMNodeList"                    => new DOMNodeList(),
	"DOMNamedNodeMap"                => new DOMNamedNodeMap(),
	"DOMCharacterData"               => new DOMCharacterData(),
	"DOMAttr"                        => new DOMAttr("artr"),
	"DOMElement"                     => new DOMElement("root"),
	"DOMText"                        => new DOMText(),
	"DOMComment"                     => new DOMComment(),
	"DOMTypeinfo"                    => new DOMTypeinfo(),
	"DOMUserDataHandler"             => new DOMUserDataHandler(),
	"DOMDomError"                    => new DOMDomError(),
	"DOMErrorHandler"                => new DOMErrorHandler(),
	"DOMLocator"                     => new DOMLocator(),
	"DOMConfiguration"               => new DOMConfiguration(),
	"DOMCdataSection"                => new DOMCdataSection("root value"),
	"DOMDocumentType"                => new DOMDocumentType(),
	"DOMNotation"                    => new DOMNotation(),
	"DOMEntity"                      => new DOMEntity(),
	"DOMEntityReference"             => new DOMEntityReference("nbsp"),
	"DOMProcessingInstruction"       => new DOMProcessingInstruction("php"),
	"DOMStringExtend"                => new DOMStringExtend(),
	"DOMXPath"                       => new DOMXPath(new DOMDocument()),
	"finfo"                          => new finfo(),
	"JsonException"                  => new JsonException(),
	"LogicException"                 => new LogicException(),
	"BadFunctionCallException"       => new BadFunctionCallException(),
	"BadMethodCallException"         => new BadMethodCallException(),
	"DomainException"                => new DomainException(),
	"InvalidArgumentException"       => new InvalidArgumentException(),
	"LengthException"                => new LengthException(),
	"OutOfRangeException"            => new OutOfRangeException(),
	"RuntimeException"               => new RuntimeException(),
	"OutOfBoundsException"           => new OutOfBoundsException(),
	"OverflowException"              => new OverflowException(),
	"RangeException"                 => new RangeException(),
	"UnderflowException"             => new UnderflowException(),
	"UnexpectedValueException"       => new UnexpectedValueException(),
	"SplFileObject"                  => new SplFileObject(__FILE__),
	"SplTempFileObject"              => new SplTempFileObject(),
	"SplDoublyLinkedList"            => new SplDoublyLinkedList(),
	"SplQueue"                       => new SplQueue(),
	"SplStack"                       => new SplStack(),
	"SplMinHeap"                     => new SplMinHeap(),
	"SplMaxHeap"                     => new SplMaxHeap(),
	"SplPriorityQueue"               => new SplPriorityQueue(),
	"SplFixedArray"                  => new SplFixedArray(),
	"SplObjectStorage"               => new SplObjectStorage(),
	"MultipleIterator"               => new MultipleIterator(),
	"SessionHandler"                 => new SessionHandler(),
	"ReflectionException"            => new ReflectionException(),
	"Reflection"                     => new Reflection(),
	"ReflectionFunction"             => new ReflectionFunction("templateFunction"),
	"ReflectionGenerator"            => new ReflectionGenerator(templateGenerator()),
	"ReflectionParameter"            => new ReflectionParameter("templateFunction", "templateParameter"),
	"ReflectionType"                 => (new ReflectionClass("ZipArchive"))->getMethod("getCommentName")->getReturnType(),
	"ReflectionNamedType"            => new ReflectionNamedType(),
	"ReflectionMethod"               => new ReflectionMethod("TemplateClass", "templateMethod"),
	"ReflectionClass"                => new ReflectionClass("TemplateClass"),
	"ReflectionObject"               => new ReflectionObject(new TemplateClass()),
	"ReflectionProperty"             => new ReflectionProperty("TemplateClass", "templateProperty"),
	"ReflectionClassConstant"        => new ReflectionClassConstant("TemplateClass", "TEMPLATE_CONSTANT"),
	"ReflectionExtension"            => new ReflectionExtension("Reflection"),
	"__PHP_Incomplete_Class"         => new __PHP_Incomplete_Class(),
	"php_user_filter"                => new php_user_filter(),
	"Directory"                      => new Directory(),
	"AssertionError"                 => new AssertionError(),
	"SimpleXMLElement"               => new SimpleXMLElement("<a>a</a>"),
	"SimpleXMLIterator"              => new SimpleXMLIterator("<a>a</a>"),
	"PharException"                  => new PharException(),
	"Phar"                           => new Phar("/tmp/fuzz.phar"),
	"PharData"                       => new PharData("/tmp/fuzz.tar"),
	"PharFileInfo"                   => new PharFileInfo("phar:///tmp/fuzz.phar/fuzz.txt"),
	"XMLReader"                      => new XMLReader(),
	"XMLWriter"                      => new XMLWriter(),
	"CURLFile"                       => new CURLFile("/tmp/fuzz"),
	"ZipArchive"                     => new ZipArchive(),
	
	/* - Instantiation not allowed -
	"ReflectionZendExtension"        => new ReflectionZendExtension(),
	"ReflectionFunctionAbstract"     => new ReflectionFunctionAbstract(),
	"PDOException"                   => new PDOException(),
	"PDO"                            => new PDO(),
	"PDOStatement"                   => new PDOStatement(),
	"SplHeap"                        => new SplHeap(),
	"PDORow"                         => new PDORow(),
	"RecursiveIteratorIterator"      => new RecursiveIteratorIterator(),
	"IteratorIterator"               => new IteratorIterator(),
	"FilterIterator"                 => new FilterIterator(),
	"RecursiveFilterIterator"        => new RecursiveFilterIterator(),
	"CallbackFilterIterator"         => new CallbackFilterIterator(),
	"RecursiveCallbackFilterIterator" => new RecursiveCallbackFilterIterator(),
	"ParentIterator"                 => new ParentIterator(),
	"LimitIterator"                  => new LimitIterator(),
	"CachingIterator"                => new CachingIterator(),
	"RecursiveCachingIterator"       => new RecursiveCachingIterator(),
	"NoRewindIterator"               => new NoRewindIterator(),
	"AppendIterator"                 => new AppendIterator(),
	"InfiniteIterator"               => new InfiniteIterator(),
	"RegexIterator"                  => new RegexIterator(),
	"RecursiveRegexIterator"         => new RecursiveRegexIterator(),
	"EmptyIterator"                  => new EmptyIterator(),
	"RecursiveTreeIterator"          => new RecursiveTreeIterator(),
	"ArrayObject"                    => new ArrayObject(),
	"ArrayIterator"                  => new ArrayIterator(),
	"RecursiveArrayIterator"         => new RecursiveArrayIterator(),
	"SplFileInfo"                    => new SplFileInfo(),
	"DirectoryIterator"              => new DirectoryIterator(),
	"FilesystemIterator"             => new FilesystemIterator(),
	"RecursiveDirectoryIterator"     => new RecursiveDirectoryIterator(),
	"GlobIterator"                   => new GlobIterator(),
	"HashContext"                    => new HashContext(),
	"Closure"                        => new Closure(),
	"Generator"                      => new Generator(),
	 */
);

// TODO randomize those as well
$ref_bool = true;
$ref_int = 1337;
$ref_string= "bla";
$ref_array = array(1.0, 2, -3e3);
$ref_object = new StdClass();
$ref_resource = fopen("/dev/null", "r");
$ref_path = "/dev/null";

<phpfuzzer>

?>
