#!/bin/sh

PAYLOAD="${1:-{}}"

NAME=$(echo "$PAYLOAD" | sed 's/.*"name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/')
NAME="${NAME:-World}"

printf '{"message": "Hello, %s! (from shell)"}\n' "$NAME"
