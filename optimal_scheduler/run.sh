#!/usr/bin/with-contenv bashio

# ==============================================================================
# Start the example service
# s6-overlay docs: https://github.com/just-containers/s6-overlay
# ==============================================================================

# Add your code here

# Declare variables
declare message

## Get the 'message' key from the user config options.
message=$(bashio::config 'message')

## Print the message the user supplied, defaults to "Hello World..."
bashio::log.info "${message:="Hello World..."}"

## Run your program
#exec /usr/bin/my_program
#python Abstraction/main.py