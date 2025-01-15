for dir in */; do
    if [ -d "$dir" ]; then
        # Loop through files in the directory
        for file in "$dir"*; do
            # Check if it's a file
            if [ -f "$file" ]; then
                # Extract the part of the filename before "S1"
                filename=$(basename "$file")
                echo "${filename%%_S1*}"
                echo ${dir}
                extracted_name="${filename%%_S1*}"
                echo ${extracted_name}
                cellranger count --id=${extracted_name} \
                --create-bam=true \
                --transcriptome=/data1/cellector/kmeans_pp/demuxlet_data/refdata-cellranger-GRCh38-3.0.0 \
                --fastqs=/data1/cellector/kmeans_pp/split_by_donor_2/${dir} \
                --sample=${extracted_name} \
                --localcores=64 \
                --localmem=128
            fi
        done
        echo "" # Add a blank line for readability
    fi
done
