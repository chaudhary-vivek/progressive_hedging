# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/Cellar/cmake/3.28.2/bin/cmake

# The command to remove a file.
RM = /usr/local/Cellar/cmake/3.28.2/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/vivekchaudhary/.cargo/registry/src/index.crates.io-6f17d22bba15001f/highs-sys-1.6.2/HiGHS

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build

# Include any dependencies generated for this target.
include examples/CMakeFiles/call_highs_from_c.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/CMakeFiles/call_highs_from_c.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/call_highs_from_c.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/call_highs_from_c.dir/flags.make

examples/CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.o: examples/CMakeFiles/call_highs_from_c.dir/flags.make
examples/CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.o: /Users/vivekchaudhary/.cargo/registry/src/index.crates.io-6f17d22bba15001f/highs-sys-1.6.2/HiGHS/examples/call_highs_from_c.c
examples/CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.o: examples/CMakeFiles/call_highs_from_c.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=/Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object examples/CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.o"
	cd /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/examples && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT examples/CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.o -MF CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.o.d -o CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.o -c /Users/vivekchaudhary/.cargo/registry/src/index.crates.io-6f17d22bba15001f/highs-sys-1.6.2/HiGHS/examples/call_highs_from_c.c

examples/CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.i"
	cd /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/examples && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /Users/vivekchaudhary/.cargo/registry/src/index.crates.io-6f17d22bba15001f/highs-sys-1.6.2/HiGHS/examples/call_highs_from_c.c > CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.i

examples/CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.s"
	cd /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/examples && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /Users/vivekchaudhary/.cargo/registry/src/index.crates.io-6f17d22bba15001f/highs-sys-1.6.2/HiGHS/examples/call_highs_from_c.c -o CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.s

# Object files for target call_highs_from_c
call_highs_from_c_OBJECTS = \
"CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.o"

# External object files for target call_highs_from_c
call_highs_from_c_EXTERNAL_OBJECTS =

bin/call_highs_from_c: examples/CMakeFiles/call_highs_from_c.dir/call_highs_from_c.c.o
bin/call_highs_from_c: examples/CMakeFiles/call_highs_from_c.dir/build.make
bin/call_highs_from_c: lib/libhighs.a
bin/call_highs_from_c: /Library/Developer/CommandLineTools/SDKs/MacOSX14.4.sdk/usr/lib/libz.tbd
bin/call_highs_from_c: examples/CMakeFiles/call_highs_from_c.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=/Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable ../bin/call_highs_from_c"
	cd /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/call_highs_from_c.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/call_highs_from_c.dir/build: bin/call_highs_from_c
.PHONY : examples/CMakeFiles/call_highs_from_c.dir/build

examples/CMakeFiles/call_highs_from_c.dir/clean:
	cd /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/examples && $(CMAKE_COMMAND) -P CMakeFiles/call_highs_from_c.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/call_highs_from_c.dir/clean

examples/CMakeFiles/call_highs_from_c.dir/depend:
	cd /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/vivekchaudhary/.cargo/registry/src/index.crates.io-6f17d22bba15001f/highs-sys-1.6.2/HiGHS /Users/vivekchaudhary/.cargo/registry/src/index.crates.io-6f17d22bba15001f/highs-sys-1.6.2/HiGHS/examples /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/examples /Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/examples/CMakeFiles/call_highs_from_c.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : examples/CMakeFiles/call_highs_from_c.dir/depend

