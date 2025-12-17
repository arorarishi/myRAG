from markitdown import MarkItDown
print("MarkItDown imported successfully")
try:
    md = MarkItDown()
    print("MarkItDown initialized successfully")
except Exception as e:
    print(f"Error initializing MarkItDown: {e}")
