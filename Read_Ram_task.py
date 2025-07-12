import psutil

# Get virtual memory details
mem = psutil.virtual_memory()

# Convert bytes to GB
total = mem.total / (1024 ** 3)
available = mem.available / (1024 ** 3)
used = mem.used / (1024 ** 3)
percent = mem.percent

# Print results
print("📊 RAM Information:")
print(f"🟢 Total RAM      : {total:.2f} GB")
print(f"🟡 Available RAM  : {available:.2f} GB")
print(f"🔴 Used RAM       : {used:.2f} GB")
print(f"📈 RAM Usage      : {percent}%")
