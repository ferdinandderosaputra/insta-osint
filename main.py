#!/usr/bin/env python3

import instaloader
import time
import sys
import platform
import getpass
import subprocess

def get_linux_distro():
    try:
        with open('/etc/os-release', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if line.startswith('PRETTY_NAME='):
                    return line.split('=')[1].strip().strip('"')
    except:
        return "Unknown Linux distribution"

def print_system_info():
    print("System Information:")
    print(f"OS: {platform.system()}")
    if platform.system() == "Linux":
        print(f"Distribution: {get_linux_distro()}")
    print(f"Python version: {platform.python_version()}")
    print()

def print_info(profile):
    print(f"Username: {profile.username}")
    print(f"Full Name: {profile.full_name}")
    print(f"User ID: {profile.userid}")
    print(f"Biography: {profile.biography}")
    print(f"External URL: {profile.external_url}")
    print(f"Is Private: {profile.is_private}")
    print(f"Is Business Account: {profile.is_business_account}")
    print(f"Business Category: {profile.business_category_name}")
    print(f"Followers: {profile.followers}")
    print(f"Following: {profile.followees}")
    print(f"Total Posts: {profile.mediacount}")

def main():
    print_system_info()
    
    username = input("Enter your Instagram username: ")
    password = getpass.getpass("Enter your Instagram password: ")

    L = instaloader.Instaloader()
    
    try:
        L.login(username, password)
        print("Login successful!")
    except instaloader.exceptions.BadCredentialsException:
        print("Login failed. Please check your credentials.")
        return

    target_username = input("Enter target Instagram username: ")
    
    try:
        profile = instaloader.Profile.from_username(L.context, target_username)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Profile {target_username} does not exist.")
        return

    print("\nAccount Information:")
    print_info(profile)

    print("\nDownloading profile picture...")
    L.download_profilepic(profile)

    print("\nDownloading posts...")
    for post in profile.get_posts():
        L.download_post(post, target=profile.username)

    print("\nFetching followers...")
    for follower in profile.get_followers():
        print(f"Follower: {follower.username}")

    print("\nFetching following...")
    for followee in profile.get_followees():
        print(f"Following: {followee.username}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped.")
