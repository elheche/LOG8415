#!/bin/bash

PID="/home/ubuntu/server/pid_file"

sudo kill "$(cat $PID)"
