"""Builds the release downloads into dist/.

Usage: python3 tools/build_release.py

Writes:
    dist/<skill>.zip       one per skill, with the skill's folder at the top level of the ZIP
    dist/all-skills.zip    every skill, each in its own folder
    dist/case-study-reference.zip   the case study's code and infrastructure, in a case-study-reference folder
    dist/SHA256SUMS.txt    a checksum for each ZIP

Eval cases and tests stay out of the ZIPs; they are for developing the skills, not using them.
"""
import hashlib
import shutil
import zipfile
from pathlib import Path

REPO_FOLDER = Path(__file__).resolve().parent.parent
SKILLS_FOLDER = REPO_FOLDER / "skills"
CASE_STUDY_FOLDER = REPO_FOLDER / "case-study-reference"
DIST_FOLDER = REPO_FOLDER / "dist"
LEFT_OUT_FOLDERS = {"evals", "tests", "__pycache__", "node_modules"}
# The case study keeps its tests, so people can check the server they downloaded. Generated code
# and caches stay out.
CASE_STUDY_LEFT_OUT_FOLDERS = {"generated", "__pycache__", ".pytest_cache", "node_modules"}
LEFT_OUT_FILES = {".DS_Store", ".keep"}
# A fixed timestamp keeps the ZIPs byte-for-byte the same when the files haven't changed.
FIXED_TIMESTAMP = (2026, 1, 1, 0, 0, 0)


def files_to_ship(skill_folder, left_out_folders=LEFT_OUT_FOLDERS):
    shipped_paths = []
    for file_path in sorted(skill_folder.rglob("*")):
        relative_parts = file_path.relative_to(skill_folder).parts
        if file_path.is_dir() or left_out_folders.intersection(relative_parts) or file_path.name in LEFT_OUT_FILES:
            continue
        if file_path.suffix == ".pyc":
            continue
        shipped_paths.append(file_path)
    return shipped_paths


def add_skill(zip_file, skill_folder, left_out_folders=LEFT_OUT_FOLDERS):
    for file_path in files_to_ship(skill_folder, left_out_folders):
        archive_name = skill_folder.name + "/" + file_path.relative_to(skill_folder).as_posix()
        zip_info = zipfile.ZipInfo(archive_name, date_time=FIXED_TIMESTAMP)
        zip_info.compress_type = zipfile.ZIP_DEFLATED
        zip_info.external_attr = 0o644 << 16
        zip_file.writestr(zip_info, file_path.read_bytes())


def sha256_of(file_path):
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def main():
    if DIST_FOLDER.exists():
        shutil.rmtree(DIST_FOLDER)
    DIST_FOLDER.mkdir()
    skill_folders = sorted(folder for folder in SKILLS_FOLDER.iterdir() if (folder / "SKILL.md").is_file())
    for skill_folder in skill_folders:
        with zipfile.ZipFile(DIST_FOLDER / (skill_folder.name + ".zip"), "w") as zip_file:
            add_skill(zip_file, skill_folder)
    with zipfile.ZipFile(DIST_FOLDER / "all-skills.zip", "w") as zip_file:
        for skill_folder in skill_folders:
            add_skill(zip_file, skill_folder)
    with zipfile.ZipFile(DIST_FOLDER / "case-study-reference.zip", "w") as zip_file:
        add_skill(zip_file, CASE_STUDY_FOLDER, CASE_STUDY_LEFT_OUT_FOLDERS)
    zip_paths = sorted(DIST_FOLDER.glob("*.zip"))
    checksum_lines = [sha256_of(zip_path) + "  " + zip_path.name for zip_path in zip_paths]
    (DIST_FOLDER / "SHA256SUMS.txt").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    print("Built", len(zip_paths), "ZIPs in dist/ (" + str(len(skill_folders)) + " skills, all-skills.zip, and case-study-reference.zip)")


if __name__ == "__main__":
    main()
