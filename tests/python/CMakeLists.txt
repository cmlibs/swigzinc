set(PYTHONTESTS )

# Add python interface tests
set(PYTHON_TESTDIRS
    field_tests
    graphics_tests
    imageprocessing_tests
    import_tests
    logger_tests
    material_tests
    region_tests
    sceneviewer_tests
)

foreach(TESTDIR ${PYTHON_TESTDIRS})
    string(REPLACE "_" "" TESTNAME ${TESTDIR})
    add_test(NAME Python_Bindings_${TESTNAME}
        COMMAND ${Python_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/${TESTDIR}/${TESTNAME}.py
    )
    list(APPEND PYTHONTESTS Python_Bindings_${TESTNAME})
endforeach()

# Also add a test to see if simple importing of the libraries works
set(TESTNAME import)
add_test(NAME Python_Bindings_${TESTNAME}
    COMMAND ${Python_EXECUTABLE} -c "from cmlibs.zinc.context import Context"
)
list(APPEND PYTHONTESTS Python_Bindings_${TESTNAME})

# Common test settings
if (WIN32)
    set(PYTHONPATH_SEP "\\;") # Needs to be \; to prevent cmake from expanding into a list
else()
    set(PYTHONPATH_SEP ":")
endif()

# Set the correct python path to have it find the cmlibs package
file(TO_NATIVE_PATH "${PROJECT_BINARY_DIR}/src/python${CFG_DIR}" NATIVE_PYTHON_BINDINGS_DIR)
# This is just needed by imageprocessing_tests and field_tests (they need a pythonpath at the python/tests dir)
file(TO_NATIVE_PATH "${CMAKE_CURRENT_SOURCE_DIR}" NATIVE_TEST_BASE_DIR)
foreach(_TEST ${PYTHONTESTS})
    set_tests_properties(${_TEST} PROPERTIES
        ENVIRONMENT "PYTHONPATH=${NATIVE_PYTHON_BINDINGS_DIR}${PYTHONPATH_SEP}${NATIVE_TEST_BASE_DIR};${PATH_DEF}"
    )
endforeach()

