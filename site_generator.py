import os.path
import os
import json
import markdown
from jinja2 import Environment, FileSystemLoader


def get_config_from_json_file(json_file):
    with open(json_file) as json_file:
        return json.load(json_file)


def add_html_pathes_for_articles(site_config, folder_for_html):
    for article in site_config['articles']:
        article['path_to_html'] = os.path.join(
            folder_for_html,
            os.path.splitext(article['source'])[0] + '.html'
        )


def create_site_directories(site_config):
    for article in site_config['articles']:
        directory = os.path.dirname(article['path_to_html'])
        if not os.path.exists(directory):
            os.makedirs(directory)


def get_from_md_file(article, path_to_articles):
    path_to_md_file = os.path.join(path_to_articles, article['source'])
    with open(path_to_md_file, encoding="utf-8") as md_file:
        return md_file.read()


def save_to_html_file(path_to_file, html_data):
    with open(path_to_file, 'w', encoding='utf-8') as html_file:
            html_file.write(html_data)


if __name__ == '__main__':
    site_config = get_config_from_json_file("config.json")
    path_to_template_folder = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'Templates'
    )
    env = Environment(loader=FileSystemLoader(path_to_template_folder))
    folder_for_html = "Docs"
    add_html_pathes_for_articles(site_config, folder_for_html)
    create_site_directories(site_config)
    template_main = env.get_template("index.html")
    index_html = template_main.render(title="Documentation",
                                      site_config=site_config,
                                      )
    save_to_html_file('index.html', index_html)
    path_to_articles = 'articles'
    template_doc_page = env.get_template("docs.html")
    for article in site_config['articles']:
        md_text = get_from_md_file(article, path_to_articles)
        html_data = markdown.markdown(md_text, extensions=['codehilite'])
        html_rendered = template_doc_page.render(doc_content=html_data,
                                                 title=article['title'])
        save_to_html_file(article['path_to_html'], html_rendered)
