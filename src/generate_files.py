import os
import shutil

from block_markdown_helper import extract_title, markdown_to_html_node


def copy_files(source, destination_base="public"):
    paths = os.listdir(source)
    for path in paths:
        source_path = os.path.join(source, path)
        destination_path = os.path.join(destination_base, path)
        if os.path.isdir(source_path):
            os.mkdir(destination_path)
            copy_files(source_path, destination_path)
        if os.path.isfile(source_path):
            shutil.copy2(source_path, destination_path)


def generate_files(source, destination_base="public"):
    if os.path.exists(destination_base):
        shutil.rmtree(destination_base)
    os.mkdir(destination_base)
    copy_files(source)

    # open
    # .read()
    # .close()
    # .replace()
    # .os.path.dirname
    # os.makedirs
    # .startswith()
    # .split()


def generate_page(from_path, dest_path, template_path):
    print(f"Generating page: {from_path} to  {dest_path} from {template_path}")
    file = None
    try:
        with open(from_path, mode="r") as f:
            file = f.read()
            f.close()
        with open(template_path, mode="r") as tf:
            template = tf.read()
            tf.close()
    except FileNotFoundError:
        return f"file not found: {from_path}"
    except PermissionError:
        return f"permission denied: {from_path}"
    except IOError:
        return f"io error: {from_path}"
    except Exception as e:
        return f"unexpected error: {e}"

    html_node = markdown_to_html_node(file)
    content = html_node.to_html()
    title = extract_title(file)

    new_html = template.replace("{{ Title }}", title)
    new_html = new_html.replace("{{ Content }}", content)
    try:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "w") as file:
            file.write(new_html)
            file.close()
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    paths = os.listdir(dir_path_content)
    for path in paths:

        if os.path.isdir(os.path.join(dir_path_content, path)):
            dir_path_content = os.path.join(dir_path_content, path)
            dest_dir_path = os.path.join(dest_dir_path, path)
            generate_pages_recursive(dir_path_content, template_path, dest_dir_path)

        if path.endswith(".md"):
            generate_page(
                os.path.join(dir_path_content, path),
                os.path.join(dest_dir_path, path.replace(".md", ".html")),
                template_path,
            )
