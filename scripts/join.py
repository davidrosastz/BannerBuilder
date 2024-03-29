import re
import glob
from pathlib import Path

def sort_key(filename):
    if not re.search(r'/([^/]+)$', filename):
      return 99 

    # Extract the number from the last child of the file path
    last_child = re.search(r'/([^/]+)$', filename).group(1)

    if not re.search(r'^\d+', last_child):
      return 99

    number = int(re.search(r'^\d+', last_child).group())
    return number

current_path = Path(__file__).resolve()
project_directory = current_path.parent.absolute().parent.absolute()

# Wildcard pattern to match HTML files
pattern = f'{project_directory}/*.html'

# Fetch all HTML files in the specified directory
file_paths = glob.glob(pattern)
file_paths = sorted(file_paths, key=sort_key)

# Read the contents of each file and store it in a list
file_contents = []
for file_path in file_paths:
  if 'index' not in file_path and 'menu' not in file_path:
    with open(file_path, 'r', encoding='utf-8') as f:
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
      <link rel="stylesheet" href="style/style.css">
    <title>Banner</title>
    </head>
    <body>
      {combined_body}
    </body>
  </html>
"""

# Write the combined HTML string to a new file
with open(f'index.html', 'w', encoding='utf-8') as f:
    f.write(combined_html)

with open('menu.html', 'w', encoding='utf-8') as f:
    f.write('<html>\n')
    f.write('<body>\n')
    f.write('<ul>\n')
    
    # Add a list item for each HTML file
    for html_file in file_paths:
        html_file = Path(html_file).name
        f.write(f'<li><a href="{html_file}">{html_file}</a></li>\n')
    
    f.write('</ul>\n')
    f.write('</body>\n')
    f.write('</html>\n')
