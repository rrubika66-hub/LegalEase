"""
LegalEase Submission Packager
Creates a clean, production-ready ZIP archive of the project for submission/LMS upload,
automatically excluding virtual environments, cache files, exports, and sensitive .env files.
"""

import os
import zipfile
import shutil

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(PROJECT_ROOT)
ZIP_NAME = "LegalEase_AI_Document_Generator_Final_Submission.zip"
OUTPUT_ZIP_PATH = os.path.join(PARENT_DIR, ZIP_NAME)

EXCLUDE_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "env", "ENV",
    ".idea", ".vscode", "exports", "build", "dist", ".pytest_cache"
}

EXCLUDE_FILES = {
    ".env", ".env.local", ".DS_Store", "Thumbs.db", ZIP_NAME
}

EXCLUDE_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".log"
}

def package_project():
    print("=================================================================")
    print("       LegalEase: Automated Project Submission Packager          ")
    print("=================================================================")
    print(f"Archiving directory: {PROJECT_ROOT}")
    print(f"Destination archive: {OUTPUT_ZIP_PATH}\n")

    total_files = 0
    with zipfile.ZipFile(OUTPUT_ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Modify dirs in place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if file in EXCLUDE_FILES or ext in EXCLUDE_EXTENSIONS:
                    continue

                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, PROJECT_ROOT)
                
                zipf.write(full_path, os.path.join("LegalEase", rel_path))
                total_files += 1

    file_size_mb = round(os.path.getsize(OUTPUT_ZIP_PATH) / (1024 * 1024), 2)
    print("-----------------------------------------------------------------")
    print(f"✅ Archive successfully generated!")
    print(f"📁 Output File: {OUTPUT_ZIP_PATH}")
    print(f"📦 Total Files Packaged: {total_files}")
    print(f"📊 Archive Size: {file_size_mb} MB")
    print("=================================================================\n")

if __name__ == "__main__":
    package_project()
