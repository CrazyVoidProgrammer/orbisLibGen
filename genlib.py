#!/usr/bin/python
import sys, os, json
from pprint import pprint

#print introduction
print('\n[INFO] PS4 Lib Generator v1\nBy CrazyVoid and Frangarcj\n')

# Lets load template data
print('\n[+] Loading Template Files\n[LOAD] template/stub.template\n[LOAD] cmake.template\n[LOAD] template/stub.template\n')
stub_template_fh = open("template/stub.template", "rb")
#cmake_template_fh = open("template/cmake.template", "rb")
makefile_template_fh = open("template/makefile.template", "rb")

stub_template_content = stub_template_fh.read()
#cmake_template_content = cmake_template_fh.read()
makefile_template_content = makefile_template_fh.read()

stub_template_fh.close()
#cmake_template_fh.close()
makefile_template_fh.close()

def printHelp():
	print('Usage : genlib.py idc_lib_folder')
	print('PARAM 1 - idc_lib_folder is location of idc common lib doc folder\n')
	
def genAssembly(inSymbols, xmodule_name, xlib_name):
	print('[+] Generating Assembly Files ')
	for prxSyms in inSymbols:
		if prxSyms["name"] and prxSyms["hex_id"]:
			tempASMContent = stub_template_content
			tempASMContent = tempASMContent.replace("$MODULE_NAME$", xmodule_name)
			tempASMContent = tempASMContent.replace("$LIBRARY_NAME$", xlib_name)
			tempASMContent = tempASMContent.replace("$ASM_FNAME$", prxSyms["name"])
			tempASMContent = tempASMContent.replace("$FUNCTION_NID$", prxSyms["hex_id"])
			stub_output_name = xmodule_name + "_" + xlib_name + "_" +  prxSyms["name"] + ".S"
			#stub_output_name = xlib_name + "_" + xmodule_name + "_" +  prxSyms["name"] + ".S"
			#stub_output_name = xmodule_name + "_" +  prxSyms["name"] + ".S"
			print("[STUB] Generating : " + stub_output_name)
			output_stub_handle = open("build/" + stub_output_name, "wb")
			output_stub_handle.write(tempASMContent)
			output_stub_handle.close()
		else:
			print('')
	
	
def genMakefile(inSymbols, xmodule_name, xlib_name):
	print('[+] Generating Makefile Files')

	
def genCmake(inSymbols):
	print('[+] Generating CMake Files')


if not os.path.exists('build'):
	os.makedirs('build')
	print('[+] Generating Folder /build/')
	
if len(sys.argv) != 2:
	printHelp()
	sys.exit(0)
	
input_idc_file_loc = sys.argv[1]
print("IDC Folder : " + sys.argv[1])

json_list = []
target_loop = []
target_weak_loop = []
module_obj_loop = []
module_weak_obj_loop = []
temp_makefile = makefile_template_content


for jsonFiles in os.listdir(input_idc_file_loc):
	if jsonFiles.endswith(".sprx.json"):
		print("[SPRX] Loading : " + jsonFiles)
		input_sprx_content = json.load(open(input_idc_file_loc + "/" + jsonFiles))
		
		module_name = input_sprx_content["modules"][0]["name"]
		lib_name = input_sprx_content["modules"][0]["libraries"][0]["name"]
		module_symbols = input_sprx_content["modules"][0]["libraries"][0]["symbols"]
		
		if module_name in json_list:
			print("Module(" + module_name + ") already added to - SKIP")
		else:
			# add to our list
			json_list.append(module_name)
			xcount = 0
			print('MODULE : ' + module_name + " - SPRX : " + lib_name + ".sprx")
			# Lets Generate Asm Files from lib docs
			genAssembly(module_symbols, module_name, lib_name)

			# Need to do this manually to make makefile
			print('[+] Generating Makefile Files')
			target_loop.append(" " + lib_name + "_stub.a")
			target_weak_loop.append(" " + lib_name + "_stub_weak.a")
			
			module_obj_loop.append(lib_name + "_OBJS=")
			module_weak_obj_loop.append(lib_name + "_weak_OBJS=")
			
			for prxSyms in module_symbols:
				if prxSyms["name"] and prxSyms["hex_id"]:
					module_obj_loop.append(" " + module_name + "_" + lib_name + "_" + prxSyms["name"] + ".o")
					module_weak_obj_loop.append(" " + module_name + "_" + lib_name + "_" + prxSyms["name"] + ".wo")
				else:
					print('[MGEN] Skipping Function')
			module_obj_loop.append("\n")
			module_weak_obj_loop.append("\n")

# Join our list to generate needed files
target_loop_joined = ' '.join(target_loop)
target_weak_loop_joined = ' '.join(target_weak_loop)
module_obj_loop_joined = ' '.join(module_obj_loop)
module_weak_obj_loop_joined = ' '.join(module_weak_obj_loop)
# Lets replace our template vars with our loop variables 
temp_makefile = temp_makefile.replace('$TARGETS_LOOP$', target_loop_joined)
temp_makefile = temp_makefile.replace('$TARGET_WEAK_LOOP$', target_weak_loop_joined)
temp_makefile = temp_makefile.replace('$MODULE_OBJS$', module_obj_loop_joined)
temp_makefile = temp_makefile.replace('$MODULE_WEAK_OBJS$', module_weak_obj_loop_joined)
# Everything is done so lets make the makefile
print('\n[+] Generating build/Makefile')
gen_makefile = open("build/Makefile", "wb")
gen_makefile.write(temp_makefile)
gen_makefile.close()
			
print('\n[+] Finished Generating Stub Files \n')
