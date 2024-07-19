from generate_files import generate_files, generate_page, generate_pages_recursive

# os.path.exists
# os.listdir
# os.path.join
# os.mkdir
# shutil.copy
# shutil.rmtree


def main():
    generate_files("static")
    # generate_page("content/index.md", "public/index.html", "template.html")
    generate_pages_recursive("content", "template.html", "public")


main()
