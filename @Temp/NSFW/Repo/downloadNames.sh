# Start
echo "Starting..."
echo

echo "Setting out variables..."
echo

# Set our variables
linksFile="downloadNameLinks.txt"
downloadFile="downloadedNames.txt"

# Clear the download file
echo "Clearing our download file for fresh input..."
>"$downloadFile"
echo

# Concatenate to our download file
echo "Downloading content from $linksFile to $downloadFile"
while IFS= read -r url; do
    echo >>"$downloadFile"
    wget -qO- "$url" >>"$downloadFile"
done <"$linksFile"
echo

# Finish
echo "Completed!"
echo