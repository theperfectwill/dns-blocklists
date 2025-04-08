for file in $(find . -name "final.txt"); do
    echo Processing $file
    cat updateHeadOfFile.txt $file > $file.modified
    mv $file.modified $file
done

for file in $(find . -name "getLatest.sh"); do
    echo Processing $file
    cat updateHeadOfFile.txt $file > $file.modified
    mv $file.modified $file
done