#!/bin/bash -xe

rm -rf app/templates
rm -rf app/static

git clone https://github.com/beepboop-tech/grace-material.git react && cd react && cd grace

npm install
npm run build

# cd react
# cd grace

cd ..

mkdir -p ../app/templates
mkdir -p ../app/static

mv grace/build/* ../app/templates/
mv ../app/templates/static/* ../app/static/

rm -rf ../app/templates/static

cd ..
rm -rf react
