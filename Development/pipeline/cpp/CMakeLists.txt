# Minimal CMake version

cmake_minimum_required(VERSION 3.10)
project(GesturesApp)

# Add your main.cpp and Camera.cpp source files
add_executable(App main.cpp camera_handler.cpp hand_detector.cpp interface_handler.cpp)

# Find the OpenCV library and include its header files
find_package(OpenCV REQUIRED)
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


target_link_libraries(
    App
    PUBLIC tensorflowlite
    PRIVATE ${OpenCV_LIBS}
    PRIVATE Qt5::Widgets
)