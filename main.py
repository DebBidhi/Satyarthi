import os
import shutil
import initial
import dynamic_crew
import paste
import run

directories = [
    'data/',
    'htmls/',
    'output/',
]

for dir_path in directories:
    # Ensure the path exists and is a directory
    if os.path.isdir(dir_path):
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # remove file or symbolic link
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # remove directory
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
    else:
        print(f"Directory does not exist: {dir_path}")

def main():
    initial.main()
    dynamic_crew.main()
    paste.main()
    run.create_navigation_html()
    print("✅ Completed Successfully!")
    print("✅ Now open main.html!")

if __name__ =="__main__":
    main()


