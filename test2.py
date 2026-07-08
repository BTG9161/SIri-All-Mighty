import sys

# Efficiently stream and process data line-by-line
print("Paste text or pipe a file (Press Ctrl+D/Ctrl+Z to finish):")
for line in sys.stdin:
    clean_line = line.rstrip() # Removes the trailing newline character
    print(f"Processed: {clean_line}")
