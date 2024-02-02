#!/bin/sh

# from refs/tags/v1.2.3 get 1.2.3
VERSION=$(echo $GITHUB_REF | sed -E 's/refs\/tags\/v?([0-9]+\.[0-9]+\.[0-9]+)/\1/')
PLACEHOLDER='__version__ = "0.0.dev0"'
VERSION_FILE='icometrix_sdk/_version.py'

# ensure the placeholder is there. If grep doesn't find the placeholder
# it exits with exit code 1 and github actions aborts the build.
grep "$PLACEHOLDER" "$VERSION_FILE"
sed -i "s/$PLACEHOLDER/__version__ = \"${VERSION}\"/g" "$VERSION_FILE"