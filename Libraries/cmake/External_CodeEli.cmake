set(codeeli_source  "${CMAKE_BINARY_DIR}/CODEELI-prefix/src/CODEELI")

if(MSVC)
  get_filename_component(_self_dir ${CMAKE_CURRENT_LIST_FILE} PATH)

  set(codeeli_patch_command PATCH_COMMAND ${CMAKE_COMMAND} -E copy
    ${_self_dir}/../CodeEli_cmake_msvc2015.patch ${codeeli_source}/cmake/CodeEli_cmake_msvc2015.patch
    COMMAND
    COMMAND git apply ${codeeli_source}/cmake/CodeEli_cmake_msvc2015.patch)
else()
  set(codeeli_patch_command "")
endif()

ExternalProject_Add( CODEELI
	URL ${CMAKE_SOURCE_DIR}/Code-Eli-fe8e29569fca.zip
	CMAKE_ARGS -DCMAKE_INSTALL_PREFIX:PATH=<INSTALL_DIR>
		-DCMAKE_C_COMPILER=${CMAKE_C_COMPILER}
		-DCMAKE_CXX_COMPILER=${CMAKE_CXX_COMPILER}
		-DCMAKE_CXX_FLAGS=${CMAKE_CXX_FLAGS}
		-DCMAKE_C_FLAGS=${CMAKE_C_FLAGS}
		-DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
    PATCH_COMMAND ${codeeli_patch_command}
	BUILD_COMMAND ""
	INSTALL_COMMAND ""
)
ExternalProject_Get_Property( CODEELI BINARY_DIR SOURCE_DIR )
SET( CODEELI_INSTALL_DIR ${BINARY_DIR} ${SOURCE_DIR})