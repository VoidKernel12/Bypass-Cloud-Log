#!/usr/bin/env bash
# =====================================================================
# Installation Script for BYPASS TOOL FOR CLOUD SERVER
# Developed using Gemini AI (Creator Credit Only)
# =====================================================================

echo -e "\033[38;2;0;255;255m[*] Updating Termux packages and repositories...\033[0m"
pkg update && pkg upgrade -y

echo -e "\033[38;2;255;215;0m[*] Installing Git, Python, Android Tools (ADB), and Termux-API...\033[0m"
pkg install git python android-tools termux-api -y

echo -e "\033[38;2;186;85;211m[*] Cloning repository...\033[0m"
git clone 
cd 

echo -e "\033[38;2;57;255;20m[+] Installation completed successfully!\033[0m"
echo -e "\033[38;2;255;215;0m[*] IMPORTANT: Please install the Termux:API APK on your device to enable popups and vibration bridge.\033[0m"
