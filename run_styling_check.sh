#!/bin/sh
set -eu

pydocstyle --convention=numpy --add-ignore=D105 commands
