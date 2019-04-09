type=$1
currentfile="batches/$(date '+%Y-%m-%d-%h-%i-%s')-batch.txt"
mv batches/${type}.txt $currentfile
while read -r line; do
    if youtube-dl -o "files/hidden/%(title)s-%(id)s.%(ext)s" $line; then
        echo "$line" >> logs/processed.txt
    else
        echo "$line" >> logs/failed.txt
    fi
    tail -n +2 "$currentfile" > "$currentfile.tmp" && mv "$currentfile.tmp" "$currentfile"
done < $currentfile
rm $currentfile
