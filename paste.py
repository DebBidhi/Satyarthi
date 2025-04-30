import re
import sys
import os
from bs4 import BeautifulSoup, Tag
import markdown
import textwrap

def convert_markdown_to_html_cards(markdown_file_path, char_limit=500):
    """
    Convert a markdown file to HTML where ## headings become cards arranged 2 per row
    with a "See More" option for long content
    
    Args:
        markdown_file_path: Path to the markdown file
        char_limit: Character limit before adding a "See More" button
    """
    # Read markdown file
    with open(markdown_file_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    
    # First convert markdown to HTML using markdown library with extra extensions
    html_content = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get the main heading (h1) if it exists
    main_heading = soup.find('h1')
    main_heading_text = main_heading.text if main_heading else "News Analysis"
    
    # Find all h2 headings
    h2_headings = soup.find_all('h2')
    
    # Create new HTML structure
    new_soup = BeautifulSoup('', 'html.parser')
    
    # Add HTML5 doctype
    doctype = '<!DOCTYPE html>'
    
    # Create HTML structure
    html_tag = new_soup.new_tag('html')
    head_tag = new_soup.new_tag('head')
    
    # Add meta tags
    meta_charset = new_soup.new_tag('meta')
    meta_charset['charset'] = 'UTF-8'
    head_tag.append(meta_charset)
    
    meta_viewport = new_soup.new_tag('meta')
    meta_viewport['name'] = 'viewport'
    meta_viewport['content'] = 'width=device-width, initial-scale=1.0'
    head_tag.append(meta_viewport)
    
    # Add title
    title_tag = new_soup.new_tag('title')
    title_tag.string = main_heading_text
    head_tag.append(title_tag)
    
    # Add favicon link (optional - you can replace with your own favicon)
    favicon = new_soup.new_tag('link')
    favicon['rel'] = 'icon'
    favicon['href'] = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">📰</text></svg>'
    favicon['type'] = 'image/svg+xml'
    head_tag.append(favicon)
    
    # Add CSS styles here (using your modernized CSS)
    style_tag = new_soup.new_tag('style')
    style_tag.string = """
:root {
  --primary-color: #2d3748;
  --secondary-color: #2d3748;
  --accent-color: #805ad5;
  --background-color: #f7fafc;
  --card-bg-color: #ffffff;
  --text-color: #1a202c;
  --light-text: #718096;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

body {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  line-height: 1.5;
  margin: 0;
  padding: 0;
  background-color: var(--background-color);
  color: var(--text-color);
}

header {
  background-color: var(--card-bg-color);
  color: var(--text-color);
  padding: 1.5rem;
  text-align: center;
  box-shadow: var(--shadow-sm);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

h1 {
  margin: 0;
  font-weight: 800;
  font-size: 2.5rem;
  letter-spacing: -0.025em;
}

.subtitle {
  color: var(--light-text);
  margin-top: 0.75rem;
  font-weight: 400;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 1.5rem;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 450px), 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.card {
  background-color: var(--card-bg-color);
  border-radius: 0.75rem;
  box-shadow: var(--shadow-md);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.05);
  height: auto;
  max-height: 600px;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-lg);
}

.card-header {
  padding: 1.5rem 1.5rem 0.75rem;
  position: relative;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: var(--text-color);
}

.card-header::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 1.5rem;
  width: 2rem;
  height: 2px;
  background-color: var(--accent-color);
}

.card-content {
  padding: 1.5rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  max-height: 400px; /* Control the maximum height of content */
}

.card-content p {
  margin-top: 0;
  color: var(--secondary-color);
  line-height: 1.6;
}

.card-content a {
  color: var(--accent-color);
  text-decoration: none;
  transition: color 0.2s;
}

.card-content a:hover {
  color: var(--secondary-color);
  text-decoration: underline;
}

.card-content img {
  max-width: 100%;
  height: auto;
  margin: 1rem 0;
  border-radius: 0.5rem;
}

.card-footer {
  padding: 1rem 1.5rem;
  margin-top: auto;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
  background-color: white;
}

.see-more-btn {
  background-color: var(--accent-color);
  color: white;
  border: none;
  border-radius: 0.5rem;
  padding: 0.65rem 1.25rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.see-more-btn:hover {
  background-color: #6b46c1;
  transform: translateY(-1px);
}

.see-more-btn::after {
  content: '→';
  transition: transform 0.2s;
}

.see-more-btn:hover::after {
  transform: translateX(3px);
}

/* Code block styling */
pre {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
  padding: 1rem;
  overflow-x: auto;
  font-family: 'SF Mono', 'Roboto Mono', Menlo, monospace;
  font-size: 0.875rem;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

/* Table styling */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1rem 0;
}

table, th, td {
  border: 1px solid rgba(0, 0, 0, 0.05);
}

th, td {
  padding: 0.75rem;
  text-align: left;
}

th {
  background-color: #f8f9fa;
  font-weight: 600;
}

tr:nth-child(even) {
  background-color: #f8f9fa;
}

/* Full article modal */
.modal {
  display: none;
  position: fixed;
  z-index: 999;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  animation: fadeIn 0.2s;
}

.modal-content {
  background-color: var(--card-bg-color);
  margin: 5% auto;
  padding: 0;
  width: 80%;
  max-width: 800px;
  border-radius: 1rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  animation: slideIn 0.3s;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.modal-header {
  background-color: var(--card-bg-color);
  color: var(--text-color);
  padding: 1.5rem;
  position: relative;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.close {
  color: var(--light-text);
  position: absolute;
  top: 1.25rem;
  right: 1.5rem;
  font-size: 1.5rem;
  font-weight: 300;
  transition: all 0.2s;
  cursor: pointer;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
}

.close:hover {
  background-color: rgba(0, 0, 0, 0.05);
  color: var(--text-color);
}

.modal-body {
  padding: 2rem;
  max-height: 70vh;
  overflow-y: auto;
}

@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}

@keyframes slideIn {
  from {transform: translateY(-30px); opacity: 0;}
  to {transform: translateY(0); opacity: 1;}
}

/* Footer */
footer {
  background-color: var(--card-bg-color);
  color: var(--light-text);
  text-align: center;
  padding: 2rem 1rem;
  margin-top: 3rem;
  border-top: 1px solid rgba(0, 0, 0, 0.05);
}

footer p {
  margin: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .container {
    padding: 1.5rem 1rem;
  }
  
  .card-container {
    grid-template-columns: 1fr;
  }
  
  h1 {
    font-size: 2rem;
  }
  
  .modal-content {
    width: 95%;
    margin: 5% auto;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  :root {
    --background-color: #121212;
    --card-bg-color: #1e1e1e;
    --text-color: #e0e0e0;
    --light-text: #a0aec0;
    --primary-color: #805ad5;
    --secondary-color: #a0aec0;
  }
  
  pre {
    background-color: #2d3748;
    border-color: #4a5568;
  }
  
  th {
    background-color: #2d3748;
  }
  
  tr:nth-child(even) {
    background-color: #222222;
  }
  
  .card {
    border: 1px solid rgba(255, 255, 255, 0.05);
  }
  
  .card-header, .modal-header {
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
  }
  
  .card-footer {
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }
  
  footer {
    border-top: 1px solid rgba(255, 255, 255, 0.05);
  }
  
  .close:hover {
    background-color: rgba(255, 255, 255, 0.1);
  }
}
    """
    head_tag.append(style_tag)
    
    # Add JavaScript for modal functionality
    script_tag = new_soup.new_tag('script')
    script_content = """
    document.addEventListener('DOMContentLoaded', function() {
        // Get all modals
        var modals = document.querySelectorAll('.modal');
        
        // Get all buttons that open a modal
        var btns = document.querySelectorAll('.see-more-btn');
        
        // Get all elements that close the modal
        var spans = document.querySelectorAll('.close');
        
        // When the user clicks the button, open the modal
        btns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                var modalId = this.getAttribute('data-modal');
                document.getElementById(modalId).style.display = 'block';
                document.body.style.overflow = 'hidden';
            });
        });
        
        // When the user clicks on <span> (x), close the modal
        spans.forEach(function(span) {
            span.addEventListener('click', closeModals);
        });
        
        // When the user clicks anywhere outside of the modal, close it
        window.addEventListener('click', function(event) {
            modals.forEach(function(modal) {
                if (event.target == modal) {
                    closeModals();
                }
            });
        });
        
        function closeModals() {
            modals.forEach(function(modal) {
                modal.style.display = 'none';
            });
            document.body.style.overflow = 'auto';
        }
        
        // Close modal with Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeModals();
            }
        });
    });
    """
    script_tag.string = script_content
    head_tag.append(script_tag)
    
    html_tag.append(head_tag)
    
    # Create body
    body_tag = new_soup.new_tag('body')
    
    # Add header
    header_tag = new_soup.new_tag('header')
    h1_tag = new_soup.new_tag('h1')
    h1_tag.string = main_heading_text
    header_tag.append(h1_tag)
    
    body_tag.append(header_tag)
    
    # Create container
    container_tag = new_soup.new_tag('div')
    container_tag['class'] = 'container'
    
    # Create card container
    card_container = new_soup.new_tag('div')
    card_container['class'] = 'card-container'
    
    # Process each h2 heading and create cards
    for index, h2 in enumerate(h2_headings):
        card_id = f"card-{index}"
        modal_id = f"modal-{index}"
        
        # Create card div
        card_div = new_soup.new_tag('div')
        card_div['class'] = 'card'
        card_div['id'] = card_id
        
        # Create card header
        card_header = new_soup.new_tag('div')
        card_header['class'] = 'card-header'
        
        # Create h2 for card header
        card_h2 = new_soup.new_tag('h2')
        card_h2.string = h2.text
        card_header.append(card_h2)
        card_div.append(card_header)
        
        # Create card content
        card_content = new_soup.new_tag('div')
        card_content['class'] = 'card-content'
        
        # Get content for this card (all elements between this h2 and the next h2)
        content_elements = []
        current = h2.next_sibling
        
        while current and not (isinstance(current, Tag) and current.name == 'h2'):
            if current.name and current.name != 'h1':
                content_elements.append(current)
            current = current.next_sibling
        
        # Convert content elements to HTML string
        content_html = ''.join(str(elem) for elem in content_elements)
        content_soup = BeautifulSoup(content_html, 'html.parser')
        
        # Check if content is longer than char_limit
        content_text = content_soup.get_text()
        is_content_long = len(content_text) > char_limit
        
        # If content is long, truncate it for the card but preserve structure
        if is_content_long:
            # Create a temporary soup to handle truncation while preserving structure
            truncated_html = truncate_html_content(content_soup, char_limit)
            truncated_soup = BeautifulSoup(truncated_html, 'html.parser')
            
            # Add truncated structured content to the card
            card_content.append(truncated_soup)
            
            # Add card footer with "See More" button
            card_footer = new_soup.new_tag('div')
            card_footer['class'] = 'card-footer'
            
            see_more_btn = new_soup.new_tag('button')
            see_more_btn['class'] = 'see-more-btn'
            see_more_btn['data-modal'] = modal_id
            see_more_btn.string = 'See More'
            
            card_footer.append(see_more_btn)
            card_div.append(card_content)
            card_div.append(card_footer)
            
            # Create modal with full content
            modal_div = new_soup.new_tag('div')
            modal_div['id'] = modal_id
            modal_div['class'] = 'modal'
            
            modal_content = new_soup.new_tag('div')
            modal_content['class'] = 'modal-content'
            
            modal_header = new_soup.new_tag('div')
            modal_header['class'] = 'modal-header'
            
            modal_title = new_soup.new_tag('h2')
            modal_title.string = h2.text
            modal_header.append(modal_title)
            
            close_span = new_soup.new_tag('span')
            close_span['class'] = 'close'
            close_span.string = '×'
            modal_header.append(close_span)
            
            modal_body = new_soup.new_tag('div')
            modal_body['class'] = 'modal-body'
            modal_body.append(content_soup)
            
            modal_content.append(modal_header)
            modal_content.append(modal_body)
            modal_div.append(modal_content)
            
            # Add modal to body (outside container)
            body_tag.append(modal_div)
        else:
            # Content is short enough, just add it to the card
            card_content.append(content_soup)
            card_div.append(card_content)
        
        # Add card to container
        card_container.append(card_div)
    
    # Add card container to main container
    container_tag.append(card_container)
    
    # Add container to body
    body_tag.append(container_tag)
    
    # Add footer
    footer_tag = new_soup.new_tag('footer')
    footer_p = new_soup.new_tag('p')
    footer_p.string = f"Generated on {get_current_date()}"
    footer_tag.append(footer_p)
    body_tag.append(footer_tag)
    
    # Add body to html
    html_tag.append(body_tag)
    new_soup.append(html_tag)
    
    # Output HTML file
    name = markdown_file_path.stem
    output_filename = f"htmls/{name}.html"
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(doctype + str(new_soup))
    
    return output_filename

def truncate_html_content(soup, char_limit):
    """
    Truncate HTML content while preserving structure and providing a natural reading experience
    
    Args:
        soup: BeautifulSoup object containing the HTML to truncate
        char_limit: Character limit for truncation
    
    Returns:
        HTML string truncated to char_limit while preserving structure
    """
    # Convert to string and create a new soup to work with
    soup_str = str(soup)
    soup_copy = BeautifulSoup(soup_str, 'html.parser')
    
    # Get total text length
    total_text = soup_copy.get_text()
    
    # If already under limit, return as is
    if len(total_text) <= char_limit:
        return soup_str
    
    # Get all text nodes in order of appearance
    text_nodes = list(soup_copy.find_all(string=True))
    
    # Count characters and find where to truncate
    char_count = 0
    truncate_index = -1
    
    for i, text in enumerate(text_nodes):
        if char_count + len(text) >= char_limit:
            # Found the node where we need to truncate
            truncate_index = i
            break
        char_count += len(text)
    
    # If we found where to truncate
    if truncate_index >= 0:
        # How many more characters we can include from the truncation node
        remaining_chars = char_limit - char_count
        
        if remaining_chars > 0:
            # Get the text to truncate
            text_to_truncate = text_nodes[truncate_index]
            
            # Find a good truncation point (end of sentence or word)
            truncated_text = text_to_truncate[:remaining_chars]
            
            # Try to truncate at the end of a sentence
            sentence_end = max(
                truncated_text.rfind('.'), 
                truncated_text.rfind('!'), 
                truncated_text.rfind('?')
            )
            
            if sentence_end > len(truncated_text) * 0.5:  # If we found a sentence end in the latter half
                truncated_text = truncated_text[:sentence_end+1]
            else:
                # Otherwise truncate at word boundary
                last_space = truncated_text.rfind(' ')
                if last_space > 0:
                    truncated_text = truncated_text[:last_space]
            
            # Replace the text node with truncated version + ellipsis
            text_nodes[truncate_index].replace_with(truncated_text + '...')
            
            # Remove all nodes after the truncation point
            for i in range(truncate_index + 1, len(text_nodes)):
                if text_nodes[i].parent:
                    text_nodes[i].extract()
        else:
            # No remaining chars, just remove this node and all following
            for i in range(truncate_index, len(text_nodes)):
                if text_nodes[i].parent:
                    text_nodes[i].extract()
    
    # Clean up empty tags
    for tag in soup_copy.find_all():
        if len(tag.get_text(strip=True)) == 0 and tag.name not in ['br', 'hr', 'img']:
            # Keep the first paragraph even if empty (to maintain structure)
            if tag.name == 'p' and not tag.find_previous_sibling('p'):
                continue
            tag.extract()
    
    # Add a proper end to the content
    last_p = soup_copy.find_all('p')
    if last_p:
        last_paragraph = last_p[-1]
        last_text = last_paragraph.get_text()
        if not last_text.endswith('...'):
            if last_text:
                last_paragraph.string = last_text + '...'
    
    return str(soup_copy)

def get_current_date():
    """Get current date in a nice format"""
    from datetime import datetime
    return datetime.now().strftime("%B %d, %Y")


def main():
  from pathlib import Path

  # Set the folder path
  folder_path = Path('data')
 # Get all .md files in the folder
  md_files = folder_path.glob('*.md')
  for md_file in md_files:
   convert_markdown_to_html_cards(md_file)
   print("done: ", md_file.stem )

if __name__ == "__main__":
    main()
