import re
import glob
from pathlib import Path

current_path = Path(__file__).resolve()
project_directory = current_path.parent.absolute().parent.absolute()

# Wildcard pattern to match HTML files
pattern = f'{project_directory}/*.html'

# Fetch all HTML files in the specified directory
file_paths = glob.glob(pattern)

# Read the contents of each file and store it in a list
file_contents = []
for file_path in file_paths:
  if 'combined' not in file_path:
    with open(file_path, 'r') as f:
        file_contents.append(f.read())

# Extract the contents of the <body> element from each file
body_contents = []
for html in file_contents:
    body_match = re.search(r'<body>(.*?)</body>', html, re.DOTALL)
    if body_match:
        body_contents.append(body_match.group(1))
    else:
        body_contents.append('')

# Join the contents of all the <body> elements into a single string
combined_body = ''.join(body_contents)

# Wrap the combined <body> element in a new HTML document
combined_html = f"""
  <!DOCTYPE html>
  <html>
    <head>
      <meta charset="utf-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="stylesheet" href="style/bootstrap-custom.css">
    <title>Hello, world!</title>
    </head>
    <body>
      {combined_body}
    </body>
  </html>
"""

# Write the combined HTML string to a new file
with open('combined.html', 'w') as f:
    f.write(combined_html)