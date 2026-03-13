import os

def copy_dir(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)

    for name in os.listdir(src):
        src_path = os.path.join(src, name)
        dst_path = os.path.join(dst, name)

        if os.path.isfile(src_path):
            with open(src_path, "rb") as fsrc, open(dst_path, "wb") as fdst:
                while chunk := fsrc.read(4096):
                    fdst.write(chunk)

        elif os.path.isdir(src_path):
            copy_dir(src_path, dst_path)

def delete_contents(path):
    for name in os.listdir(path):
        full_path = os.path.join(path, name)

        if os.path.isfile(full_path):
            os.remove(full_path)

        elif os.path.isdir(full_path):
            delete_contents(full_path)
            os.rmdir(full_path)

def read_file_to_string(filepath):
    with open(filepath, "r") as f:
        contents = f.read()
    return contents