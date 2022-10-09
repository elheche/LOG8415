#!/bin/bash

DIR="/home/ubuntu/server/"
PID="pid_file"

sudo kill "$(cat $DIR$PID)"
