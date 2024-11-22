sudo apt-get install libpcre2-dev python3-dev gcc python3-cffi cmake --assume-yes

git submodule init
git submodule update --remote

cd libyang
mkdir build
cd build

cmake ..
make
sudo make install
sudo ldconfig
