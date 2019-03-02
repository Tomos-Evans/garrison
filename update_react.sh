#!/bin/bash -xe

rm -rf app/templates
rm -rf app/static

git clone https://github.com/beepboop-tech/grace.git react && cd react && git checkout built

mkdir -p ../app/templates
mkdir -p ../app/static

mv grace/build/* ../app/templates/
mv ../app/templates/static/* ../app/static/

rm -rf ../app/templates/static

cd ..
rm -rf react
