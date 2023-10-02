#!/bin/bash

for folder in ./bundle/*/ ; do
  ./krane "${folder}anim.bin" "${folder}build.bin" "./output/${folder}"
  ./ktech "${folder}atlas-0.tex" "./output/${folder}"
done
