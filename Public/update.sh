#!/bin/bash

# First install
# @Reference->https://github.com/AdguardTeam/HostlistCompiler

echo "Starting... Updating All Base And Block Lists..."
echo

# Set our variables

Settings="settings.json"
BlockList="blocklist.txt"
BaseList="base.txt"
WhiteList="whitelist.txt"

# Main Lists

ThisPath="/Volumes/Work/WebGit/dns-blocklists"
CorePath="$ThisPath/Public/Core"
ServicesPath="$ThisPath/Public/Services"
WhitelistPath="$ThisPath/Public/Whitelist"

# Services Lists

cd $ServicesPath/3PStreaming && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/9Gag && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/AliBaba && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Amazon && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/AmpSites && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/ClubHouse && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/DailyMotion && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Discord && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/DisneyPlus && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Ebay && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/FaceBook && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/FourSquare && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Giphy && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Google && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/GoogleChat && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/HboMax && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Hulu && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Imgur && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/InstaGram && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/LinkedIn && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Mastadon && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Microsoft && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/MySpace && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Netflix && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/News && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/OnlineGames && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Pinterest && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/PrimeVideo && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Reddit && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Shopee && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Signal && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Skype && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/SnapChat && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/SocialMedia && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Spotify && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/SupportChats && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Telegram && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Temu && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Threads && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/TikTok && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Tumblr && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Twitch && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/TwitterX && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Vimeo && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Vk && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/WhatsApp && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/Wish && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $ServicesPath/YouTube && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList

# Core and Larger Lists (takes more time to process, like 15 minutes)

cd $CorePath/Sin && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $CorePath/Security && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList
cd $CorePath/Privacy && hostlist-compiler -i $BaseList -o $BaseList && hostlist-compiler -c $Settings -o $BlockList

# Whitelists

cd $WhitelistPath/ && hostlist-compiler -c $Settings -o $WhiteList

# Finish

echo "Finished! All Base And Block Lists Updated!"
echo