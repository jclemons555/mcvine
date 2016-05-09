#
set(PACKAGE_NAME "instrument")


if("${BUILDING_MCVINE}" STREQUAL "")

  set(VERSION "0.1")
  set(AUTHOR "Jiao Lin")
  set(AUTHOR_EMAILE "jiao.lin@gmail.com")
  set(VENDOR "DANSE")
  set(SUMMARY "Neutron instrument representation")
  set(LICENSE "BSD")
  set(RPM_APP_GROUP "Development/Tools")
  set(GITHUB_URL "https://github.com/danse-inelastic/instrument")
  # this is released with danse.ins packages
  set(DEP_DANSE_PKGS "danse.ins")

  #
  cmake_minimum_required (VERSION 2.8)
  project (${PACKAGE_NAME})
  # get cmake_utils
  execute_process(
    COMMAND rm -rf cmake_utils
    COMMAND git clone https://github.com/danse-inelastic/cmake_utils
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    )
  set(CMAKE_MODULE_PATH ${PROJECT_BINARY_DIR}/cmake_utils)

  # utils
  include(System) # system info
  include(Dirs)   # directory structure
  include(TestUtils)

  # needs python
  find_package ( PythonLibs REQUIRED )
  find_package ( PythonInterp REQUIRED )
  # python installation path
  set(INSTALL_PY_PATH "${INSTALL_LIB_DIR}/python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}/site-packages")

  #
  enable_testing()
else("${BUILDING_MCVINE}" STREQUAL "")
  set(EXPORT_SHARE ${EXPORT_SHARE}/instrument)
endif()

# python
file(
  COPY ${PACKAGE_NAME} 
  DESTINATION ${EXPORT_PYTHON}/
  FILES_MATCHING PATTERN "*.py"
  )

# app
file(COPY applications/ DESTINATION ${EXPORT_BIN}/
  FILES_MATCHING PATTERN "*.py"
  )

# share
file(COPY share/ DESTINATION ${EXPORT_SHARE}/)

# tests
set(BUILD_TESTS_PATH ${TESTS_DIR}/${PACKAGE_NAME})
# copy tests to build
# file(COPY tests/ DESTINATION ${BUILD_TESTS_PATH})
# add python tests
# PYUNITTEST_ADD_TESTS_IN_DIR( ${BUILD_TESTS_PATH} ${PACKAGE_NAME})
