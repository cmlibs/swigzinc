# SWIGZinc
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

cmake_minimum_required(VERSION 3.18.0)
cmake_policy(VERSION 3.18.0)

if(POLICY CMP0078)
    cmake_policy(SET CMP0078 NEW)
endif()

if(POLICY CMP0086)
    cmake_policy(SET CMP0086 NEW)
endif()

if(POLICY CMP0094)
    cmake_policy(SET CMP0094 NEW)
endif()

# This is the project name and shows up in IDEs
project(SWIGZinc VERSION 4.0.0 LANGUAGES C CXX)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

find_package(Zinc CONFIG REQUIRED)

include(environmentchecks)

if(NOT IS_MULTI_CONFIG)
  set(_PARAM_ANNOTATION "Choose the type of build, options are: None(CMAKE_CXX_FLAGS or CMAKE_C_FLAGS used) Debug Release RelWithDebInfo MinSizeRel.")
  set(SWIGZINC_BUILD_TYPE "Debug" CACHE STRING "${_PARAM_ANNOTATION}")
  if(DEFINED BUILD_TYPE)
    set(SWIGZINC_BUILD_TYPE ${BUILD_TYPE} CACHE STRING "${_PARAM_ANNOTATION}" FORCE)
  endif()
endif()
unset(BUILD_TYPE CACHE)
set(CMAKE_BUILD_TYPE ${SWIGZINC_BUILD_TYPE} CACHE INTERNAL "Internalise CMAKE_BUILD_TYPE, manipulate via SWIGZINC_BUILD_TYPE" FORCE)

set(_PARAM_ANNOTATION "Enable Python bindings.")
if(PYTHON_BINDINGS_AVAILABLE)
  set(SWIGZINC_PYTHON_BINDINGS ON CACHE BOOL "${_PARAM_ANNOTATION}")
endif()
if(DEFINED PYTHON_BINDINGS AND PYTHON_BINDINGS_AVAILABLE)
  set(SWIGZINC_PYTHON_BINDINGS "${PYTHON_BINDINGS}" CACHE BOOL "${_PARAM_ANNOTATION}" FORCE)
elseif(CLANG_TIDY)
  message(WARNING "Python bindings has been requested but not available!")
endif()
unset(PYTHON_BINDINGS CACHE)

if(IS_MULTI_CONFIG)
    set(CFG_DIR /$<CONFIG>)
endif()

add_subdirectory(src)

enable_testing()
add_subdirectory(tests)

message(STATUS "Summary")
message(STATUS "- Using Zinc: ${Zinc_DIR}")
message(STATUS "- Zinc version: ${Zinc_VERSION}")
message(STATUS "- Python version: ${Python_VERSION}")
message(STATUS "- SWIG version: ${SWIG_VERSION}")

