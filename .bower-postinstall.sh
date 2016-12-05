#!/bin/bash

#
# script to run after bower install js libs
#
# - remove source and other files not needed in production
# - move the distribution files up a level in the directory
#

# this script is called in bower context, so pwd is
# PROJECT_DIR/static

### for bootstrap
for extension in md js json
do
    rm vendor/bootstrap/*.${extension}
done

for dir in fonts grunt js nuget Gemfile less
do
    rm -rf vendor/bootstrap/${dir}*
done

for file in css fonts js
do
    mv vendor/bootstrap/dist/${file} vendor/bootstrap/
done
rm -rf vendor/bootstrap/dist


### for datatables
for extension in md json
do
    rm vendor/datatables/*.${extension}
done

for file in css images js
do
    mv vendor/datatables/media/${file} vendor/datatables/
done
rm -rf vendor/datatables/media


### for jquery
for extension in md json
do
    rm vendor/jquery/*.${extension}
done

for dir in external src
do
    rm -rf vendor/jquery/${dir}*
done

mv vendor/jquery/dist/* vendor/jquery
rm -rf vendor/jquery/dist


### for font-awesome
for extension in json txt
do
    rm vendor/font-awesome/*.${extension}
done

for dir in less scss
do
    rm -rf vendor/font-awesome/${dir}*
done


### d3 is good enough!
