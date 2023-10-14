rm -rf build

mkdir build && cd build && cmake ..

make

cd ../../pipeline/

python -m unittest tests.test_model