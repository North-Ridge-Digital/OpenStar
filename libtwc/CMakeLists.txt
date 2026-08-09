cmake_minimum_required(VERSION 3.10)
project(twc LANGUAGES C CXX)

set(TWC_SOURCES
    ${CMAKE_CURRENT_SOURCE_DIR}/src/V4L2.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/AudioMixer.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/src/VBI.cpp
)

set(TWC_PUBLIC_HEADERS
    ${CMAKE_CURRENT_SOURCE_DIR}/include/twc/AudioMixer.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/include/twc/V4L2.hpp
    ${CMAKE_CURRENT_SOURCE_DIR}/include/twc/VBI.hpp
)

add_library(twc STATIC ${TWC_SOURCES})

target_include_directories(twc PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/../include
)

set_target_properties(twc PROPERTIES
    C_STANDARD 99
    CXX_STANDARD 17
    POSITION_INDEPENDENT_CODE ON
)
