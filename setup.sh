#!/bin/bash

echo -e "\e[1;32m[*] Termux-DLX Pro Setup Shuru Ho Raha Hai...\e[0m"

# System packages update aur install karna
echo -e "\e[1;34m[*] Packages update ho rahe hain...\e[0m"
pkg update -y && pkg upgrade -y

echo -e "\e[1;34m[*] Required tools (Python, Git, FFmpeg) install ho rahe hain...\e[0m"
pkg install python git ffmpeg -y

# Python libraries install karna
if [ -f "requirements.txt" ]; then
    echo -e "\e[1;34m[*] Python libraries install ho rahi hain...\e[0m"
    pip install -r requirements.txt
else
    echo -e "\e[1;31m[!] requirements.txt nahi mili! Manual install kar rahe hain...\e[0m"
    pip install rich yt-dlp pyfiglet
fi

echo -e "\e[1;32m[✔] SETUP COMPLETE! Ab aap 'python downloader.py' chala sakte hain.\e[0m"
