#!/bin/bash

if [ ! -e $1 ] 
then
    mkdir $1
fi
rm ${1}/*
cp tmva.cxx ${1}/
cd $1
root -l tmva.cxx
cd ..
