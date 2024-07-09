# Generated by CMake

if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" LESS 2.8)
   message(FATAL_ERROR "CMake >= 2.8.0 required")
endif()
if(CMAKE_VERSION VERSION_LESS "2.8.3")
   message(FATAL_ERROR "CMake >= 2.8.3 required")
endif()
cmake_policy(PUSH)
cmake_policy(VERSION 2.8.3...3.26)
#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Protect against multiple inclusion, which would fail when already imported targets are added once more.
set(_cmake_targets_defined "")
set(_cmake_targets_not_defined "")
set(_cmake_expected_targets "")
foreach(_cmake_expected_target IN ITEMS highs::highs)
  list(APPEND _cmake_expected_targets "${_cmake_expected_target}")
  if(TARGET "${_cmake_expected_target}")
    list(APPEND _cmake_targets_defined "${_cmake_expected_target}")
  else()
    list(APPEND _cmake_targets_not_defined "${_cmake_expected_target}")
  endif()
endforeach()
unset(_cmake_expected_target)
if(_cmake_targets_defined STREQUAL _cmake_expected_targets)
  unset(_cmake_targets_defined)
  unset(_cmake_targets_not_defined)
  unset(_cmake_expected_targets)
  unset(CMAKE_IMPORT_FILE_VERSION)
  cmake_policy(POP)
  return()
endif()
if(NOT _cmake_targets_defined STREQUAL "")
  string(REPLACE ";" ", " _cmake_targets_defined_text "${_cmake_targets_defined}")
  string(REPLACE ";" ", " _cmake_targets_not_defined_text "${_cmake_targets_not_defined}")
  message(FATAL_ERROR "Some (but not all) targets in this export set were already defined.\nTargets Defined: ${_cmake_targets_defined_text}\nTargets not yet defined: ${_cmake_targets_not_defined_text}\n")
endif()
unset(_cmake_targets_defined)
unset(_cmake_targets_not_defined)
unset(_cmake_expected_targets)


# Create imported target highs::highs
add_library(highs::highs STATIC IMPORTED)

set_target_properties(highs::highs PROPERTIES
  INTERFACE_COMPILE_DEFINITIONS "LIBHIGHS_STATIC_DEFINE"
  INTERFACE_INCLUDE_DIRECTORIES "/Users/vivekchaudhary/.cargo/registry/src/index.crates.io-6f17d22bba15001f/highs-sys-1.6.2/HiGHS/src;/Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build;/Users/vivekchaudhary/.cargo/registry/src/index.crates.io-6f17d22bba15001f/highs-sys-1.6.2/HiGHS;/Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build"
  INTERFACE_LINK_LIBRARIES "ZLIB::ZLIB;Threads::Threads"
)

# Import target "highs::highs" for configuration "Release"
set_property(TARGET highs::highs APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(highs::highs PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "C;CXX"
  IMPORTED_LOCATION_RELEASE "/Users/vivekchaudhary/Documents/progressive_hedging/rust_from_scratch/target/debug/build/highs-sys-f592e10caca23b3b/out/build/lib/libhighs.a"
  )

# This file does not depend on other imported targets which have
# been exported from the same project but in a separate export set.

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
cmake_policy(POP)
