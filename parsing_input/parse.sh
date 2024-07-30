function unzip {
    for file in source/*.tsp.gz; do
        gzip -d $file
        mv ${file%.*} parsed
    done
}

for file in parsed/*; do
    line_count=$(wc -l < $file)
    i=0
    while read -r line; do
        i=$(( i + 1 ))
        if [[ $line == "NODE_COORD_SECTION" ]]; then
            break
        fi
    done
    parsed=$(awk -v TOTAL="$line_count" -v START=$i \
        '{if (NR > START && NR < TOTAL) print $2, $3}' $file)
    echo -e "$(($line_count - 7))\n$parsed" > final/$(basename $file)
done