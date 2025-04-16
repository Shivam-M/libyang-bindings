sudo apt-get install libpcre2-dev python3-dev gcc python3-cffi cmake valgrind --assume-yes

git submodule init
git submodule update

sh extra/build_common.sh libyang
sh extra/build_common.sh cJSON