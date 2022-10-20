#!/bin/bash

yarn config set registry https://registry.npmmirror.com/

yarn install

yarn run prod
