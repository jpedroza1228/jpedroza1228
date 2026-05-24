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
    
  newest_post_folder = get_posts()[0]
  title, subtitle, date, categories = get_post_metadata(newest_post_folder)
  url = get_post_url(newest_post_folder)
  
  category_tags = " ".join([f"<code>{cat}</code>" for cat in categories]) if categories else ""
  
  blog_html = (
    f'Newest blog post:<br>\n'
    f'<strong><a href="{url}">{title} {subtitle}</a></strong><br>\n'
    f'Published date: {date}<br>\n'
    f'Topics covered: {category_tags}\n'
  )
  
  with open(readme_path, "r", encoding="utf-8") as f:
    readme_content = f.read()
        
  target_heading = "## Blog Posts"

  if target_heading not in readme_content:
    print(f"Error: Could not find '{target_heading}' in your README.md!")
    return

  before_heading = readme_content.split(target_heading)[0]
  
  raw_after_heading = readme_content.split(target_heading, 1)[1]

  next_section_target = "<h2>GitHub Stats</h2>"
  if next_section_target in raw_after_heading:
    after_blog_content = raw_after_heading.split(next_section_target)[1]
    rest_of_file = f"\n\n{next_section_target}{after_blog_content}"
  else:
    rest_of_file = raw_after_heading
  
  updated_content = f"{before_heading}{target_heading}\n\n{blog_html}{rest_of_file}"
  
  with open(readme_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

if __name__ == "__main__":
  update_readme()
