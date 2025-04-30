#!/usr/bin/env python3
import os
import glob
import datetime

def create_navigation_html():
    """
    Creates a main.html file that serves as a navigation page for all HTML files
    in the /htmls directory.
    """
    # Make sure htmls directory exists
    if not os.path.exists('htmls'):
        os.makedirs('htmls')
        print("Created /htmls directory since it didn't exist.")
    
    # Get all HTML files in the htmls directory
    html_files = glob.glob('htmls/*.html')
    
    # Sort files alphabetically
    html_files.sort()
    
    # Create the main HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML Files Navigator</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        ul {{
            list-style-type: none;
            padding: 0;
        }}
        li {{
            margin: 10px 0;
            padding: 8px 12px;
            background-color: #f5f5f5;
            border-radius: 4px;
            transition: background-color 0.2s;
        }}
        li:hover {{
            background-color: #e0e0e0;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
            display: block;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        .info {{
            font-size: 0.8em;
            color: #666;
            margin-top: 3px;
        }}
        .empty-message {{
            color: #666;
            font-style: italic;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 0.8em;
            color: #666;
            border-top: 1px solid #eee;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    <h1>Satyarthi</h1>
    
    <p>Navigation:</p>
    
    <ul>
"""
    
    # Add each HTML file to the navigation
    if html_files:
        for html_file in html_files:
            file_name = os.path.basename(html_file)
            file_path = html_file
            file_stats = os.stat(file_path)
            file_size = file_stats.st_size
            mod_time = datetime.datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            
            # Format size in KB
            size_kb = file_size / 1024
            
            html_content += f"""        <li>
            <a href="{file_path}" target="_blank">{file_name}</a>
            <div class="info">Size: {size_kb:.1f} KB | Last modified: {mod_time}</div>
        </li>
"""
    else:
        html_content += """        <li class="empty-message">No HTML files found in the /htmls folder.</li>
"""
    
    # Close HTML content
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    html_content += f"""    </ul>
    
    <div class="footer">
        Generated on {current_time}
    </div>
</body>
</html>
"""
    
    # Write to file
    with open('main.html', 'w') as f:
        f.write(html_content)
    
    print(f"Successfully created main.html with links to {len(html_files)} HTML files.")

if __name__ == "__main__":
    create_navigation_html()