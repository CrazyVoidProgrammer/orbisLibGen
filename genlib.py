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
core_stub_template_fh = open("template/core_stub.template", "rb")

stub_template_content = stub_template_fh.read()
#cmake_template_content = cmake_template_fh.read()
makefile_template_content = makefile_template_fh.read()
core_stub_template_content = core_stub_template_fh.read()


stub_template_fh.close()
#cmake_template_fh.close()
makefile_template_fh.close()
core_stub_template_fh.close()

def printHelp():
	print('Usage : genlib.py idc_lib_folder')
	print('PARAM 1 - idc_lib_folder is location of idc common lib doc folder\n')
	
def genAssembly(inSymbols, xmodule_name, xlib_name):
	print('[+] Generating Assembly Files ')
	xstub_filename = (lib_name + ".S")
	xstub_content_temp = []
	xstub_replace_temp = core_stub_template_content
	cxstub = ""

	
	for prxSyms in inSymbols:
		if prxSyms["name"] and prxSyms["hex_id"]:

			cxstub = cxstub.replace("$$LIB_NAME$$", lib_name)
			cxstub = cxstub.replace("$$FUNCTION_NAME$$", prxSyms["name"])
			cxstub = cxstub.replace("$$NID$$", prxSyms["hex_id"])
			
			xstub_content_temp.append("\n" + cxstub)

			# Resets template var with template data
			cxstub = core_stub_template_content 
		else:
			print('[ERROR] Invalid Function \n')
			
	print("[STUB] Generating : " + xstub_filename)
	output_stubx_handle = open("build/" + xstub_filename, "wb")
	output_stubx_handle.write("".join(xstub_content_temp))
	output_stubx_handle.close()
	
	
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
			target_loop.append(" " + lib_name + ".a")
			target_weak_loop.append(" " + lib_name + "_stub_weak.a")
			
			# Open Stub Filename
			#stub_filename = lib_name + ".S"
			#stub_content_temp = []
			#stub_replace_temp = core_stub_template_content
			
			for prxSyms in module_symbols:
				if prxSyms["name"] and prxSyms["hex_id"]:
					module_obj_loop.append(" " + module_name + "_" + lib_name + "_" + prxSyms["name"] + ".o")
					module_weak_obj_loop.append(" " + module_name + "_" + lib_name + "_" + prxSyms["name"] + ".wo")
					
#					stub_replace_temp = stub_replace_temp.replace("$$LIB_NAME$$", lib_name)
#					stub_replace_temp = stub_replace_temp.replace("$$FUNCTION_NAME$$", prxSyms["name"])
#					stub_replace_temp = stub_replace_temp.replace("$$NID$$", prxSyms["hex_id"])
#					stub_content_temp.append(stub_replace_temp + "\n")
#					stub_replace_temp = ""
				else:
					print('[MGEN] Skipping Function')

					
#	print("[STUB] Generating : " + stub_filename)
#	output_stubx_handle = open("build/" + stub_filename, "wb")
#	output_stubx_handle.write("".join(stub_content_temp))
#	output_stubx_handle.close()
			
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