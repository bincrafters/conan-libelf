cmake_minimum_required(VERSION 2.8.11)
project(elf C)

file(GLOB_RECURSE SOURCES "${PROJECT_SOURCE_DIR}/lib/*.c")
file(GLOB_RECURSE HEADERS "${PROJECT_SOURCE_DIR}/lib/*.h")

add_library(${PROJECT_NAME} ${SOURCES})
set_target_properties(${PROJECT_NAME} PROPERTIES PUBLIC_HEADER "${HEADERS}")
target_include_directories(${PROJECT_NAME} SYSTEM PUBLIC "${PROJECT_SOURCE_DIR}/lib")

if(MSVC)
	set_target_properties(${PROJECT_NAME} PROPERTIES WINDOWS_EXPORT_ALL_SYMBOLS TRUE)
endif()

install(TARGETS ${PROJECT_NAME}
    ARCHIVE DESTINATION lib
	LIBRARY DESTINATION lib
	RUNTIME DESTINATION bin
    PUBLIC_HEADER DESTINATION include/libelf
)

install(FILES "${PROJECT_SOURCE_DIR}/lib/libelf.h" DESTINATION include)
install(FILES "${PROJECT_SOURCE_DIR}/lib/gelf.h"   DESTINATION include)
install(FILES "${PROJECT_SOURCE_DIR}/lib/nlist.h"  DESTINATION include)
