#!/usr/bin/python
import sys, os, json
from pprint import pprint
from subprocess import call

#print introduction
print('\nPS4 Stub Generator\nBy CrazyVoid\n')

stub_template_fh = open("data/stub.asm.template", "rb")
stub_template_content = stub_template_fh.read()
stub_template_fh.close()

linker_prefix = "llvm-ar rc "
compiler_prefix = "clang-5.0 -target x86_64-scei-ps4 "

compiler_makefile_data = "\nxobjects:\n\t" + compiler_prefix + "*.S -c\n"

linker_data = []
linker_data.append("\nxstubs:\n\t$(info Compiling Stubs)")

msCount = 0

# Print Help Function
def printHelp():
	print('Usage : generate.py idc_ps4libdoc_location\n')
	print('ps4libdoc location is the system/common/lib folder\n\n')
	

# Generate Asm Function
def genAsm(inSymbols, xmodule_name, xlib_name):
	
	prxFilelist = list()

	global linker_data
	
	linker_temp = []
	fnCount = 0
	
	for prxSyms in inSymbols:
		if prxSyms["name"] and prxSyms["encoded_id"]:
			fnCount += 1
			xstub_filename = (xlib_name + "." + prxSyms["name"] + ".S")
			xobject_filename = (xlib_name + "." + prxSyms["name"] + ".o")
			
			linker_insert = xlib_name + "." + prxSyms["name"] + ".o"
			linker_temp.append(linker_insert + " ")
			
			prxFilelist.append("build/" + xobject_filename)
			
			xstub_content_temp = []
			xstub_content_temp = stub_template_content
			
			xstub_content_temp = xstub_content_temp.replace("$$LIB_NAME$$", xlib_name)
			xstub_content_temp = xstub_content_temp.replace("$$FUNCTION_NAME$$", prxSyms["name"])
			xstub_content_temp = xstub_content_temp.replace("$$NID$$", prxSyms["encoded_id"])
			
			print("[INFO] Generating " + xlib_name + "." + prxSyms["name"] + " Stub\n")
			
			output_stub_fh = open("build/" + xstub_filename, "wb")
			output_stub_fh.write("".join(xstub_content_temp))
			output_stub_fh.close()
		else:
			print("[INFO] Failed to generate stub\n")
			
	if fnCount != 0:
		linkPrefixData = "\n\t" + linker_prefix + xlib_name + ".a "
		linker_data.append(linkPrefixData)
		linker_data.append("".join(linker_temp))
	#linker_data = "".join(linker_temp)
	#linker_data.append("\n" + "".join(linker_temp))		
			
def writeMakefile():
	print("[INFO] Generating Makefile")
	output_makefile_fh = open("build/Makefile", "wb")
	output_makefile_fh.write(compiler_makefile_data)
	output_makefile_fh.write("".join(linker_data))
	output_makefile_fh.close()

			
#Check if there the proper amount of args
if len(sys.argv) != 2:
	printHelp()
	sys.exit(0)
	
# Check if build folder exist, if not create it!
if not os.path.exists('build'):
	os.makedirs('build')
	print('[INFO] Creating Folder Build\n')
else:
	print('[INFO] Build Folder exists\n');
	
	
input_idc_file_loc = sys.argv[1]
print("Stub Documentation File Location : " + sys.argv[1] + "\n")

json_list = []


for jsonFile in os.listdir(input_idc_file_loc):
	if jsonFile.endswith(".sprx.json"):
		print("[INFO] Loading Sprx Documentation File : " + jsonFile + "\n")
		

		input_sprx_content = json.load(open(input_idc_file_loc + "/" + jsonFile))

		
		module_name = input_sprx_content["modules"][0]["name"]
		lib_name = input_sprx_content["modules"][0]["libraries"][0]["name"]
		module_symbols = input_sprx_content["modules"][0]["libraries"][0]["symbols"]
		
		if module_name in json_list:
			print("[HONEYPOT] " + module_name + " has already been parsed and generated\n")
		else:
			# add module to checked list 
			json_list.append(module_name)
			xcount = 0
			print("Module : " + module_name + " - SPRX : " + lib_name + ".sprx\n")
			# Generate the asm files
			genAsm(module_symbols, module_name, lib_name)
		
	else:
		print("[INFO] " + jsonFile + " Is not a sprx documentation\n")

print("[INFO] Finished Generating Stub Source Files\n")
writeMakefile()