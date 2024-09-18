"""
Simple helper script to generate a lot of this grammer with web_idl db.
"""

import web_idl

# Fill this in
PATH_TO_CHROME = ""
web_idl_database_path = '/out/Default/gen/third_party/blink/renderer/bindings/web_idl_database.pickle'
web_idl_database = web_idl.Database.read_from_file(PATH_TO_CHROME + web_idl_database_path)

def is_gpu(ident):
	if "GPU" in ident:
		return True
	return False

def is_promise(ident):
	if "Promise" in ident:
		return True
	return False

def remove_promise_info(s):
	if "OrNullPromise" in s:
		return s[:s.index("OrNullPromise")]
	
	if "Promise" in s:
		return s[:s.index("Promise")]
	
	return s

def parse_enums():
	builder = ""

	for enum in web_idl_database.enumerations:
		if not is_gpu(enum.identifier):
			continue
		
		for value in enum.values:
			builder += "<{}> = \"{}\"\n".format(enum.identifier, value)
		
		builder += "\n"
	
	return builder

def parse_namespaces():
	builder = ""

	for ns in web_idl_database.namespaces:
		if not is_gpu(ns.identifier):
			continue
		
		for const in ns.constants:
			builder += "<{}> = {}.{}\n".format(ns.identifier, ns.identifier, const.identifier)

		builder += "\n"

	return builder

def parse_dictionaries():
	builder = ""

	for dictionary in web_idl_database.dictionaries:
		if not is_gpu(dictionary.identifier):
			continue
	
		print(dictionary.identifier)

def parse_interfaces():
	builder = ""

	for interface in web_idl_database.interfaces:
		if not is_gpu(interface.identifier):
			continue
		

		builder += "#" + ("~"*16) + interface.identifier + ("~"*16) + "#\n"
		for attribute in interface.attributes:
			if attribute.is_readonly:
				continue

			builder += "<{}>.{} = <{}>".format(interface.identifier, attribute.identifier, attribute.idl_type.type_name)
			builder += "\n"

		for operation in interface.operations:
			required_args = operation.num_of_required_arguments
			num_args = len(operation.arguments)

			lifted_args = []
			for argument in operation.arguments:
				lifted_args.append("<{}>".format(argument.idl_type.type_name))

			for i in range(required_args, num_args + 1):
				if operation.return_type.type_name != "Void":
					return_type = remove_promise_info(operation.return_type.type_name)
					builder += "<new {}> = ".format(return_type)

					if is_promise(operation.return_type.type_name):
						builder += "await "

				builder += "<{}>.{}(".format(interface.identifier, operation.identifier)
				builder += "{}".format(",".join(lifted_args[:i]))
				builder += ");\n"

		builder += "\n"
	return builder


def parse_dictionaries():
	builder = ""
	
	for dictionary in web_idl_database.dictionaries:
		if not is_gpu(dictionary.identifier):
			continue
		

		lifted_members = []
		for member in dictionary.members:
			lifted_members.append("{}: <{}>".format(member.identifier, member.idl_type.type_name))

		builder += "<{}> = ".format(dictionary.identifier)
		builder += "{ "
		builder += ", ".join(lifted_members)
		builder += " };"
		builder += "\n"

	return builder

if __name__ == "__main__":
	enums = parse_enums()
	namespaces = parse_namespaces()
	interfaces = parse_interfaces()
	dictionaries = parse_dictionaries()
	print(enums)
	print(namespaces)
	print(interfaces)
	print(dictionaries)
