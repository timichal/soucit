import markdown, os, re, yaml, shutil

# start with a clean output
shutil.rmtree("out")
os.mkdir("out")

# read the content file
with open('content.md', encoding='utf-8') as text:
    content = text.read()

articles = content.split(79*"=")

# generating the articles & the index page entries
index_entries = ''
for article in articles:
    article = yaml.load(article)
    article["bandlc"] = article["band"].lower()
    article["titlelc"] = article["title"].lower()

    # filling the article template
    with open("template/article.html", encoding='utf-8') as article_template:
        template = article_template.read() 

    for variable in re.findall(r"\{(\w+)\}", template):
        template = template.replace('{' + variable + '}', str(article[variable]))

    with open("out/" + article["filename"] + ".html", 'w', encoding='utf-8') as file:
        file.write(template)

    # the index page entry
    index_entry = '<div class="entry"><a href="' + article["filename"] + '.html">' +\
                '<span>' + article["bandlc"] + '</span> • ' +\
                '<span>' + article["titlelc"] + '</span></a><br></div>'
    index_entries += index_entry

# generate the index page
with open('template/index.html', encoding="utf-8") as index_template:
    template = index_template.read()
    template = template.replace('{entries}', index_entries)

with open('out/index.html', 'w', encoding="utf-8") as index_out:
    index_out.write(template)

# copy the files
shutil.copy("template/about.html", "out")
shutil.copytree("template/files", "out/files")