# Minimal CMake version

cmake_minimum_required(VERSION 3.12)
project(GesturesApp)

# set(PYTHON_EXECUTABLE /home/karimelq/miniconda3/envs/DL_DEV/bin/python3.7)
find_package(OpenCV REQUIRED)

#
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../pipeline/core_cpp/tflite_src/include/)
include_directories(.)

# lib has 1 file: libtensorflowlite.so
ADD_LIBRARY(tensorflowlite SHARED IMPORTED)
set_property(TARGET tensorflowlite PROPERTY IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/../pipeline/core_cpp/lib/libtensorflowlite.so)

#Add pybind
add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/pybind11)
pybind11_add_module(hand_detector_wrapped MODULE hand_detector.cpp)
set_target_properties(hand_detector_wrapped PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}../../pipeline)
link_directories(${CMAKE_SOURCE_DIR}/lib) # so that target link lib find tensorflowlite
target_link_libraries(hand_detector_wrapped PRIVATE pybind11::module tensorflowlite ${OpenCV_LIBS} ${Python_LIBRARIES} )