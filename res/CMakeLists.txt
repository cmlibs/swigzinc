
cmake_minimum_required(VERSION 3.18)

project(SWIGZinc-CIBuild)

include(ExternalProject)

message(STATUS "Running build for non-python reliant libraries.")
message(STATUS "Release tag: ${RELEASE_TAG}")

set(OCD_DIR "${CMAKE_CURRENT_BINARY_DIR}/ocd")
file(MAKE_DIRECTORY ${OCD_DIR})

ExternalProject_Add(build_dependencies
  PREFIX BuildDependencies
  GIT_REPOSITORY "https://github.com/CMLibs/SuperBuild.git"
  GIT_TAG main
  GIT_SHALLOW TRUE
  CMAKE_ARGS -DCMLIBS_SETUP_TYPE=dependencies -DCMLIBS_ROOT=${OCD_DIR}
  INSTALL_COMMAND ""
)

ExternalProject_Add(build_zinc
  DEPENDS build_dependencies
  PREFIX ZincLibrary
  GIT_REPOSITORY "https://github.com/CMLibs/Zinc.git"
  GIT_TAG ${RELEASE_TAG}
  GIT_SHALLOW TRUE
  CMAKE_ARGS -DCMLIBSDEPENDENCIES_DIR=${OCD_DIR}/install/
  INSTALL_COMMAND ""
)

#ExternalProject_Add(build_swigzinc
#  DEPENDS build_zinc
#  PREFIX SWIGZincPackage
#  SOURCE_DIR "${CMAKE_CURRENT_LIST_DIR}/.."
#  CMAKE_ARGS -DZinc_DIR=${CMAKE_CURRENT_BINARY_DIR}/ZincLibrary/src/build_zinc-build -DBUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=${CMAKE_CURRENT_LIST_DIR} -DSKBUILD=TRUE
#  INSTALL_COMMAND ""
#)

#add_custom_target(install-python-bindings
#    COMMAND ${CMAKE_COMMAND} --build . --target install-python-bindings
#    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/SWIGZincPackage/src/build_swigzinc-build
#    DEPENDS build_swigzinc
#)

