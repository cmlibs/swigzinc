include(TestUndefinedSymbolsAllowed)

test_undefined_symbols_allowed()

if(CMAKE_VERSION VERSION_GREATER_EQUAL 3.18 AND CMAKE_SYSTEM_NAME STREQUAL "Linux")
  set(_FIND_PYTHON_DEVELOPMENT_TYPE Development.Module)
  set(FIND_PYTHON_DEVELOPMENT_MODULE TRUE)
else()
  set(_FIND_PYTHON_DEVELOPMENT_TYPE Development)
endif()

find_package(Python COMPONENTS Interpreter ${_FIND_PYTHON_DEVELOPMENT_TYPE})
find_package(SWIG)

get_property(IS_MULTI_CONFIG GLOBAL PROPERTY GENERATOR_IS_MULTI_CONFIG)

if (Python_VERSION VERSION_GREATER 3.6)
  set(HAVE_SUITABLE_PYTHON TRUE)
endif()

if (SWIG_VERSION VERSION_GREATER 4.0)
    set(HAVE_SUITABLE_SWIG TRUE)
endif()

if (HAVE_SUITABLE_PYTHON AND HAVE_SUITABLE_SWIG)
    set(PYTHON_BINDINGS_AVAILABLE TRUE)
endif()

