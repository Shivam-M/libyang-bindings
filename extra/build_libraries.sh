if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "assumed dependencies installed"
    # brew install cmake llvm pcre2 libffi
else
    sudo apt-get install libpcre2-dev python3-dev gcc python3-cffi cmake valgrind --assume-yes
fi

git submodule init
git submodule update

sh extra/build_common.sh libyang
sh extra/build_common.sh cJSON
