#!/bin/sh

OUTPUT_DIR="/pcap"
mkdir -p "$OUTPUT_DIR"

FILENAME="capture_$(date +%Y%m%d_%H%M%S).pcap"

echo "Starting tcpdump capture -> $OUTPUT_DIR/$FILENAME"
tcpdump -i any -w "$OUTPUT_DIR/$FILENAME" -v

exec "$@"
