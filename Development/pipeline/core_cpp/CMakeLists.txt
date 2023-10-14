# Minimal CMake version

cmake_minimum_required(VERSION 3.12)
project(GesturesApp)

# set(PYTHON_EXECUTABLE /home/karimelq/miniconda3/envs/DL_DEV/bin/python3.7) #Fix python version for pybind
# Find the OpenCV library and include its header files
find_package(OpenCV REQUIRED)

# Add your main.cpp and Camera.cpp source files
add_executable(App main.cpp camera_handler.cpp hand_detector.cpp interface_handler.cpp)

# find_package(pybind11 REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/tflite_src/include/)
include_directories(.)


# lib has 1 file: libtensorflowlite.so
ADD_LIBRARY(tensorflowlite SHARED IMPORTED)
set_property(TARGET tensorflowlite PROPERTY IMPORTED_LOCATION ${CMAKE_CURRENT_SOURCE_DIR}/lib/libtensorflowlite.so)

# Find the Qt packages
find_package(Qt5 COMPONENTS Widgets REQUIRED)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)

# Pybind
# add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/pybind11)
# pybind11_add_module(hand_detector_wrapped MODULE hand_detector.cpp)
# set_target_properties(hand_detector_wrapped PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR})
# link_directories(${CMAKE_SOURCE_DIR}/lib) # so that target link lib find tensorflowlite
# target_link_libraries(hand_detector_wrapped PRIVATE pybind11::module tensorflowlite ${OpenCV_LIBS} ${Python_LIBRARIES} )

#App
target_link_libraries(
    App
    PUBLIC tensorflowlite
    PRIVATE ${OpenCV_LIBS}
    PRIVATE Qt5::Widgets
)