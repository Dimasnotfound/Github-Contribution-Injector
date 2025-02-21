#!/usr/bin/env python3
"""
Licensed under Dimasnotfound on GitHub (https://github.com/Dimasnotfound)
GitHub Contribution Injector - Automates the process of committing changes to a GitHub repository.
"""

import os
import sys
import subprocess
import datetime
import time
import shutil

# ANSI color codes for formatting
GREEN = "\033[32m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def typing_animation(text, color, delay=0.00001):
    for ch in text:
        print(f"{color}{ch}{RESET}", end='', flush=True)
        time.sleep(delay)
    print()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print(f"{GREEN}{BOLD}")
    print("=====================================================")
    print("             GitHub Contribution Injector")
    print("=====================================================")
    print(f"{RESET}")

def remove_repo(repo_name):
    """Menghapus direktori repository jika ada."""
    if os.path.isdir(repo_name):
        try:
            shutil.rmtree(repo_name)
        except Exception as e:
            print(f"{YELLOW}Error removing directory {repo_name}: {e}{RESET}")

def clone_repo(repo_url, repo_name):
    """Clone repository secara diam-diam; jika ada, hapus direktori lama terlebih dahulu."""
    remove_repo(repo_name)
    result = subprocess.run(["git", "clone", repo_url],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        print(f"{YELLOW}Failed to clone repository.{RESET}")
        sys.exit(1)

def get_git_config(key):
    result = subprocess.run(["git", "config", key],
                            stdout=subprocess.PIPE,
                            text=True)
    return result.stdout.strip()

def set_git_config(key, value):
    subprocess.run(["git", "config", key, value],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

def push_repo(branch):
    result = subprocess.run(["git", "push", "origin", branch],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    if result.returncode != 0:
        print(f"{YELLOW}Failed to push changes.{RESET}")
        sys.exit(1)

def remote_commit_single():
    """Melakukan commit pada satu tanggal tertentu."""
    username = input(f"{YELLOW}Enter your GitHub username [e.g., user123]: {RESET}")
    email = input(f"{YELLOW}Enter your email [e.g., email@example.com]: {RESET}")
    repo_url = input(f"{YELLOW}Enter the GitHub repository URL [e.g., https://github.com/user/repo.git]: {RESET}")
    file_name = input(f"{YELLOW}Enter the name of the file to be committed [e.g., README.md]: {RESET}")
    file_content = input(f"{YELLOW}Enter the content for the file [e.g., Initial commit]: {RESET}")
    commit_date_str = input(f"{YELLOW}Enter the commit date (YYYY-MM-DD): {RESET}")
    branch = input(f"{YELLOW}Enter the branch name (default is 'master') [e.g., main]: {RESET}")
    branch = branch if branch else "master"
    commit_message = input(f"{YELLOW}Enter the commit message [e.g., Added README file]: {RESET}")

    try:
        commit_date = datetime.datetime.strptime(commit_date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"{YELLOW}Invalid date format. Please use YYYY-MM-DD.{RESET}")
        return

    repo_name = os.path.basename(repo_url)
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    clone_repo(repo_url, repo_name)
    os.chdir(repo_name)

    # Simpan konfigurasi Git asli
    original_username = get_git_config("user.name")
    original_email = get_git_config("user.email")
    set_git_config("user.name", username)
    set_git_config("user.email", email)

    # Update file dan commit
    with open(file_name, "w") as f:
        f.write(f"{file_content}\nCommit date: {commit_date}")
    subprocess.run(["git", "add", file_name],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    commit_datetime = f"{commit_date}T12:00:00"
    env = os.environ.copy()
    env["GIT_COMMITTER_DATE"] = commit_datetime
    env["GIT_AUTHOR_DATE"] = commit_datetime

    subprocess.run(["git", "commit", "-m", f"{commit_message} for {commit_date}"],
                   env=env,
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    push_repo(branch)

    # Kembalikan konfigurasi Git asli
    set_git_config("user.name", original_username)
    set_git_config("user.email", original_email)
    os.chdir("..")
    remove_repo(repo_name)
    clear_screen()
    print(f"{GREEN}Contribution injected successfully for {commit_date}!{RESET}")
    show_menu()

def remote_commit_range():
    """Melakukan commit untuk setiap hari dalam rentang tanggal tertentu."""
    username = input(f"{YELLOW}Enter your GitHub username [e.g., user123]: {RESET}")
    email = input(f"{YELLOW}Enter your email [e.g., email@example.com]: {RESET}")
    repo_url = input(f"{YELLOW}Enter the GitHub repository URL [e.g., https://github.com/user/repo.git]: {RESET}")
    file_name = input(f"{YELLOW}Enter the name of the file to be committed [e.g., README.md]: {RESET}")
    file_content = input(f"{YELLOW}Enter the content for the file [e.g., Initial commit]: {RESET}")
    start_date_str = input(f"{YELLOW}Enter the start commit date (YYYY-MM-DD): {RESET}")
    end_date_str = input(f"{YELLOW}Enter the end commit date (YYYY-MM-DD): {RESET}")
    branch = input(f"{YELLOW}Enter the branch name (default is 'master') [e.g., main]: {RESET}")
    branch = branch if branch else "master"
    commit_message = input(f"{YELLOW}Enter the commit message [e.g., Added README file]: {RESET}")

    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        print(f"{YELLOW}Invalid date format. Please use YYYY-MM-DD.{RESET}")
        return

    if start_date > end_date:
        print(f"{YELLOW}Start date must be before or equal to end date.{RESET}")
        return

    repo_name = os.path.basename(repo_url)
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]

    clone_repo(repo_url, repo_name)
    os.chdir(repo_name)

    # Simpan konfigurasi Git asli
    original_username = get_git_config("user.name")
    original_email = get_git_config("user.email")
    set_git_config("user.name", username)
    set_git_config("user.email", email)

    one_day = datetime.timedelta(days=1)
    current_date = start_date

    while current_date <= end_date:
        with open(file_name, "w") as f:
            f.write(f"{file_content}\nCommit date: {current_date}")
        subprocess.run(["git", "add", file_name],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)

        commit_datetime = f"{current_date}T12:00:00"
        env = os.environ.copy()
        env["GIT_COMMITTER_DATE"] = commit_datetime
        env["GIT_AUTHOR_DATE"] = commit_datetime

        subprocess.run(["git", "commit", "-m", f"{commit_message} for {current_date}"],
                       env=env,
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
        print(f"{CYAN}Injected contribution for {current_date}...{RESET}")
        current_date += one_day

    push_repo(branch)

    # Kembalikan konfigurasi Git asli
    set_git_config("user.name", original_username)
    set_git_config("user.email", original_email)
    os.chdir("..")
    remove_repo(repo_name)
    clear_screen()
    print(f"{GREEN}Range contributions injected successfully from {start_date} to {end_date}!{RESET}")
    show_menu()

def show_menu():
    print(f"{YELLOW}Please select an option:{RESET}")
    print("1. Single Injection (commit pada satu tanggal)")
    print("2. Range Injection (commit untuk rentang tanggal)")
    print("3. Exit")
    choice = input(f"{YELLOW}Enter choice [1-3]: {RESET}")
    if choice == '1':
        remote_commit_single()
    elif choice == '2':
        remote_commit_range()
    elif choice == '3':
        print("Exiting program.")
        sys.exit(0)
    else:
        print(f"{YELLOW}Invalid choice, please select 1, 2, or 3.{RESET}")
        show_menu()

def main():
    clear_screen()
    show_banner()
    typing_animation("Copyright 2025, Licensed under Dimasnotfound on GitHub", CYAN, 0.00001)
    show_menu()

if __name__ == "__main__":
    main()
