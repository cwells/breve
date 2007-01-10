#!/bin/bash

rm -rf Breve.egg-info dist build
find . -name "*.pyc" -exec rm {} \;
find . -name "*~" -exec rm {} \;
