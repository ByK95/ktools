#!/bin/bash

for folder in ./files/*/ ; do
  ./krane "${folder}anim.bin" "${folder}build.bin" "${folder}output"
  ./ktech "${folder}atlas-0.tex"
done
