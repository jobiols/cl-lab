#!/usr/bin/env bash
# run test suite for vhing

CLIENT="lab"

echo $CLIENT"_test"

oe -Q curso -c $CLIENT -d $CLIENT"_test"
