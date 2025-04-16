if [ -z "$1" ]; then
  echo "Error - no submodule name provided (libyang/cJSON): $0 <submodule>"
  exit 1
fi

SUBMODULE=$1

cd $SUBMODULE
rm -rf build
mkdir build
cd build

cmake ..
make
sudo make install
sudo ldconfig
