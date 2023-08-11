# SWIGZinc Library
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

if (CMAKE_CONFIGURATION_TYPES)
    set(CFG_DIR /$<CONFIG>)
    set(CFG_INSTALL_DIR /\${CMAKE_INSTALL_CONFIG_NAME})
endif ()

# Create Python bindings for the Zinc library.
set(ZINC_PYTHON_PREFERRED_VERSION "" CACHE STRING "Identify your preferred version of Python to locate, if not set the first available Python is used. [3.7, 3.8, 3.9, ...]")

# SWIG has already been found at this point.
include(${SWIG_USE_FILE})

# We have to set the include directories onto the directory because the swig
# wrapping process requires the include directories.
#include_directories(${ZINC_API_INCLUDE_DIR} ${PYTHON_INCLUDE_DIRS})

# Suppress the overload operator warning for Python.
set(CMAKE_SWIG_FLAGS -w381 -w382 -w361 -w362 ${PYTHONLIBS_SWIG_FLAGS})

set(INTERFACE_SRCS
    ../interface/context.i
    ../interface/differentialoperator.i
    ../interface/element.i
    ../interface/field.i
    ../interface/fieldmodule.i
    ../interface/fieldcache.i
    ../interface/fieldassignment.i
    ../interface/fieldparameters.i
    ../interface/fieldrange.i
    ../interface/fieldsmoothing.i
    ../interface/font.i
    ../interface/glyph.i
    ../interface/graphics.i
    ../interface/light.i
    ../interface/logger.i
    ../interface/material.i
    ../interface/optimisation.i
    ../interface/node.i
    ../interface/scene.i
    ../interface/scenecoordinatesystem.i
    ../interface/scenefilter.i
    ../interface/scenepicker.i
    ../interface/sceneviewer.i
    ../interface/sceneviewerinput.i
    ../interface/selection.i
    ../interface/shader.i
    ../interface/spectrum.i
    ../interface/region.i
    ../interface/result.i
    ../interface/status.i
    ../interface/stream.i
    ../interface/streamimage.i
    ../interface/streamregion.i
    ../interface/streamscene.i
    ../interface/tessellation.i
    ../interface/timekeeper.i
    ../interface/timenotifier.i
    ../interface/timesequence.i)

set_source_files_properties(${INTERFACE_SRCS} PROPERTIES CPLUSPLUS ON USE_TARGET_INCLUDE_DIRECTORIES TRUE)

set(BASE_PYTHON_PACKAGE_DIR "${CMAKE_CURRENT_BINARY_DIR}${CFG_DIR}")
set(CMLIBS_PYTHON_PACKAGE_DIR "${BASE_PYTHON_PACKAGE_DIR}/cmlibs")
set(ZINC_PYTHON_PACKAGE_DIR "${CMLIBS_PYTHON_PACKAGE_DIR}/zinc")
set(CMAKE_SWIG_OUTDIR "${CMAKE_CURRENT_BINARY_DIR}/modules_python_files")

set(SWIG_MODULE_TARGETS )
set(MODULE_PY_FILES )
set(SETUP_PY_PACKAGE_FILES "'$<TARGET_FILE_NAME:zinc>'")

if (NOT WIN32)
    list(APPEND SETUP_PY_PACKAGE_FILES "'$<TARGET_SONAME_FILE_NAME:zinc>'")
    set(_GENERATOR_EXPRESSION_ZINC_SONAME $<TARGET_SONAME_FILE:zinc>)
endif ()
foreach(SWIG_INTERFACE ${INTERFACE_SRCS})
    get_filename_component(MODULE_NAME ${SWIG_INTERFACE} NAME_WE)
    list(APPEND MODULE_PY_FILES ${MODULE_NAME}.py)
    swig_add_library(${MODULE_NAME}
      LANGUAGE python
      SOURCES ${SWIG_INTERFACE})
    target_link_libraries(${MODULE_NAME} PUBLIC zinc)

    if(FIND_PYTHON_DEVELOPMENT_MODULE)
      set(_PYTHON_LINK_TARGET Python::Module)
    else()
      set(_PYTHON_LINK_TARGET Python::Python)
    endif()

    if (APPLE)
      # Specifically allow dynamic lookup, here we are really targetting Python symbols.
      set_target_properties(${MODULE_NAME} PROPERTIES LINK_FLAGS "-undefined dynamic_lookup")
      # But, we do need to know about the Python include directories.
      target_include_directories(${MODULE_NAME} PRIVATE ${Python_INCLUDE_DIRS})
    elseif (UNDEFINED_SYMBOLS_ALLOWED)
      # Linker allows undefined symbols, so let's not link Python.
      # But, we do need to know about the Python include directories.
      target_include_directories(${MODULE_NAME} PRIVATE ${Python_INCLUDE_DIRS})
    else()
      target_link_libraries(${MODULE_NAME} PRIVATE ${_PYTHON_LINK_TARGET})
    endif()

    # Disable use of Debug Python libraries when not present on Windows
    # See http://stackoverflow.com/questions/11311877/creating-a-dll-from-a-wrapped-cpp-file-with-swig
    if (WIN32)
        if (NOT PYTHON_DEBUG_LIBRARY)
            target_compile_definitions(${MODULE_NAME} PRIVATE $<$<CONFIG:Debug>:SWIG_PYTHON_INTERPRETER_NO_DEBUG>)
        endif()
    endif()
    set_target_properties(${MODULE_NAME} PROPERTIES
        DEBUG_POSTFIX ""
        CXX_VISIBILITY_PRESET hidden
        BUILD_WITH_INSTALL_RPATH TRUE
        LIBRARY_OUTPUT_DIRECTORY ${ZINC_PYTHON_PACKAGE_DIR}
        RUNTIME_OUTPUT_DIRECTORY ${ZINC_PYTHON_PACKAGE_DIR}
    )
    if (APPLE)
        set_target_properties(${MODULE_NAME} PROPERTIES
            INSTALL_RPATH "@loader_path/")
    elseif (UNIX)
        set_target_properties(${MODULE_NAME} PROPERTIES
            INSTALL_RPATH "\$ORIGIN/")
    endif ()
    list(APPEND SWIG_MODULE_TARGETS ${MODULE_NAME})
    list(APPEND SETUP_PY_PACKAGE_FILES "'$<TARGET_FILE_NAME:${MODULE_NAME}>'")
endforeach()

add_custom_target(collect_python_binding_files ALL
    COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_SWIG_OUTDIR} ${CMAKE_CURRENT_BINARY_DIR}${CFG_DIR}/cmlibs/zinc
    COMMAND ${CMAKE_COMMAND} -E copy_if_different $<TARGET_FILE:zinc> ${_GENERATOR_EXPRESSION_ZINC_SONAME} ${CMAKE_CURRENT_BINARY_DIR}${CFG_DIR}/cmlibs/zinc
)
add_dependencies(collect_python_binding_files ${SWIG_MODULE_TARGETS})

set(PYZINC_ARCHITECTURE ${CMAKE_SYSTEM_PROCESSOR})
if(WIN32)
    # Sometimes we cross-compile on Windows so we'll set
    # the PYZINC_ARCHITECTURE manually
    if(CMAKE_SIZEOF_VOID_P EQUAL 4)
        set(PYZINC_ARCHITECTURE x86)
    else()
        set(PYZINC_ARCHITECTURE amd64)
    endif()
endif()
if(APPLE)
    set(PYZINC_ARCHITECTURE universal)
endif()

# Get a pretty system name.
#GET_SYSTEM_NAME(SYSTEM_NAME)
set(PYPI_PACKAGE_NAME cmlibs.zinc)
set(PYPI_SOURCE_TARGZ_VERSION "${Zinc_VERSION}-${PYZINC_ARCHITECTURE}-${CMAKE_SYSTEM_NAME}-Python${Python_VERSION_MAJOR}.${Python_VERSION_MINOR}")

################################################################
# Generate the required package files
set(ADDITIONAL_PACKAGE_FILES
    CHANGES.txt
    LICENSE.txt
    README.rst
    docs/main.rst)

# 1. Configure stage
set(SETUP_PY_PACKAGE_FILES_STR "${SETUP_PY_PACKAGE_FILES}")
string(REPLACE ";" "," SETUP_PY_PACKAGE_FILES_STR "${SETUP_PY_PACKAGE_FILES_STR}")
set(SETUP_PRE_GEN_PY_FILE "${CMAKE_CURRENT_BINARY_DIR}/setup.pre_gen.py")
configure_file(setup.in.py ${SETUP_PRE_GEN_PY_FILE} @ONLY)

if (WIN32)
    file(TO_NATIVE_PATH "${CMAKE_INSTALL_PREFIX}/${ZINC_INSTALL_BIN_DIR}" NATIVE_PATH)
else()
    file(TO_NATIVE_PATH "${CMAKE_INSTALL_PREFIX}/${ZINC_INSTALL_LIB_DIR}" NATIVE_PATH)
endif()
configure_file(zinc__init__.in.py "${CMAKE_CURRENT_BINARY_DIR}/zinc__init__.py" @ONLY)

foreach(_file ${ADDITIONAL_PACKAGE_FILES})
    configure_file("${CMAKE_CURRENT_SOURCE_DIR}/${_file}" "${CMAKE_CURRENT_BINARY_DIR}/${_file}")
endforeach()
#set(MANIFEST_IN_FILE "${CMAKE_CURRENT_BINARY_DIR}/MANIFEST.in")
#configure_file( "${CMAKE_CURRENT_SOURCE_DIR}/MANIFEST.in" "${MANIFEST_IN_FILE}")

# 2. Generate stage - takes care of all the build types (think of multiconf environment like VS)
file(GENERATE OUTPUT "${BASE_PYTHON_PACKAGE_DIR}/setup.py"
    INPUT "${SETUP_PRE_GEN_PY_FILE}"
)
# cmlibs __init__.py does not need to be configured (yet)
file(GENERATE OUTPUT "${CMLIBS_PYTHON_PACKAGE_DIR}/__init__.py"
    INPUT "${CMAKE_CURRENT_SOURCE_DIR}/cmlibs__init__.py"
)
file(GENERATE OUTPUT "${ZINC_PYTHON_PACKAGE_DIR}/__init__.py"
    INPUT "${CMAKE_CURRENT_BINARY_DIR}/zinc__init__.py"
)
foreach(_file ${ADDITIONAL_PACKAGE_FILES})
    file(GENERATE OUTPUT "${BASE_PYTHON_PACKAGE_DIR}/${_file}"
        INPUT "${CMAKE_CURRENT_BINARY_DIR}/${_file}"
    )
endforeach()

#################################
# Create tarball
set(PYPI_SOURCE_TARGZ "${CMAKE_CURRENT_BINARY_DIR}${CFG_DIR}/${PYPI_PACKAGE_NAME}-${PYPI_SOURCE_TARGZ_VERSION}.tar.gz")
add_custom_target(python_bindings_tarball
    COMMAND ${CMAKE_COMMAND} -E tar czf ${PYPI_SOURCE_TARGZ} -- $<CONFIG>/cmlibs setup.py ${ADDITIONAL_PACKAGE_FILES}
)

include(${CMAKE_CURRENT_LIST_DIR}/InstallConfig.cmake)

if (BUILD_TESTS)
    add_subdirectory(tests)
endif ()
