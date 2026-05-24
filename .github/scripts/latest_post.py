import os
import re
import frontmatter
from pyhere import here

# get the latest post that is published on the website
def get_posts():
  posts = os.listdir('website/_site/posts')
  posts.sort(reverse = True)
  return posts

# get_posts()[0]

# get the title, subtitle, date of the post,
# and the categories that are covered in the post
def get_post_metadata(post):
  post = frontmatter.load(f'website/posts/{post}/index.qmd')
  
  title = post['title']
  subtitle = post['subtitle']
  date = post['date']
  categories = post['categories']

  return title, subtitle, date, categories

# get_post_metadata(get_posts()[0])

# Build the URL of the published post from the filename
def get_post_url(post):
  url = 'https://jonathanapedroza.com/posts/' + post +'/'
  return url

# get_post_url(get_posts()[0])

def update_readme():
  readme_path = "README.md"
    
  # 1. Gather newest post data
  newest_post_folder = get_posts()[0]
  title, subtitle, date, categories = get_post_metadata(newest_post_folder)
  url = get_post_url(newest_post_folder)
  
  category_tags = " ".join([f"<code>{cat}</code>" for cat in categories]) if categories else ""
  
  # 2. Build the exact HTML string
  blog_html = (
      f"Newest blog post:<br>\n"
      f"<strong><a href='{url}'>{title} {subtitle}</a></strong> - <em>{date}</em><br>\n"
      f"{category_tags}\n"
  )
  
  # 3. Define exact delimiter tags matching your README
  start_tag = ""
  end_tag = ""
  
  # 4. Read the profile README
  with open(readme_path, "r", encoding="utf-8") as f:
      readme_content = f.read()
  # Verify the tags exist to prevent errors
  if start_tag not in readme_content or end_tag not in readme_content:
      print("Error: Could not find the exact comment tags in your README.md!")
      return
    
  # 5. Split using the EXACT variable names defined above
  before_blog = readme_content.split(start_tag)[0]
  after_blog = readme_content.split(end_tag)[1]
  # Reassemble the file cleanly
  updated_content = f"{before_blog}{start_tag}\n{blog_html}{end_tag}{after_blog}"
  
  # 6. Save the file back down
  with open(readme_path, "w", encoding="utf-8") as f:
      f.write(updated_content)
      
  print(f"Successfully and cleanly updated the README with: '{title}'")
    
if __name__ == "__main__":
    update_readme()
