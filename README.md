# OrbisLibGen
## Version 1.00

This python script is used to generate stub files for the Orbis Open Source SDK!
This tool is in the release phase of development and is usable for production use now!

This tool was written by **CrazyVoid** 

If you wish to contribute to this tool, please verify or attempt to verify it works on all platforms before pushing changes
Windows, Linux, Mac

### Steps to use this tool

#### 1: Run our script and point it to idc ps4libdoc system/common/lib folder
##### ./generate.py ps4libdoc/system/common/lib

#### 2: Cd into the build folder
##### cd build

#### 3: Lets Compile our Asm files into objects
##### make xobjects

#### 4: Lets make this objects a lib
##### make xstubs


Once all the stubs are compiled into their respected .a files.
Copy all .a to you're sdk lib folder!

### Improved Instructions and Description will come in the future!
