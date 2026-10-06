#!/bin/env bash

if [[ $1 == "pyshacl" ]]; then
    pyshacl -a -im -s eq.shapes.ttl -e cim17.vocab.ttl -i rdfs -df turtle -sf turtle -ef turtle eq.example.ttl
elif [[ $1 == "topbraid" ]]; then
    /opt/shacl/bin/shaclvalidate.sh -shapesfile eq.shapes.ttl -datafile eq.example.ttl
else
    java -jar /opt/eu-shacl-validator.jar -contentToValidate $1 text/turtle -loadImports true -mergeModelsBeforeValidation true -externalShapes $2 text/turtle
fi
