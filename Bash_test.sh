
# Loop through and filter all the files
for ((i=0; i<${#List[@]}; i++)); do
    # create the folder for each species
    mkdir -p ${species_name[$i]}
    # filter the files and save in the corrosponding folder
    species="${desired_species[$i]}"
	subspecies="${desired_sub_species[$i]}"
    awk -F'\t' -v species="$species" -v subspecies="$subspecies" '$10 == species && (subspecies == "" || $11 == subspecies)' "${List[$i]}" > "./${species_name[$i]}//filtered_species.csv"
    filtered_file_path=./${species_name[$i]}/filtered_species.csv
    # Define the museum array correctly
    echo "Processing species filtered file: ${species_name[$i]} for museum/institution type"
    museum=("AMNH" "FMNH" "iNaturalist" "KU" "MVZ" "NHMUK" "NMR" "SMF" "USNM" "YPM")
    # go through the museums and count
    for entry in "${museum[@]}"; do
        count=$(grep -c "$entry" "$filtered_file_path")
        echo "$entry: $count"
    done
    #Define speciemen in a varible
    echo "Processing species filtered file: ${species_name[$i]} for type of specimen in basisOfRecord"
    specimen=("PRESERVED_SPECIMEN" "HUMAN_OBSERVATION" "OCCURANCE" "MATERIAL_SAMPLE")
    # go through the specimen and count
    for entry in "${specimen[@]}"; do
        count=$(grep -c "$entry" "$filtered_file_path")
        echo "$entry: $count"
    done
    # Musculus inatural year counting
    if [[ "${species_name[$i]}" == "musculus" ]]; then
        echo "iNatural musculus year counting,"
        for year in {2000..2024}; do
            count=$(awk -F'\t' '$37 == "iNaturalist" {print $33}' $filtered_file_path | grep -c "$year")
            echo "$year: $count"
        done
    fi
    # Filter out the ones without lat and long
    awk -F'\t' '($22 != "" || $23 != "")' "${List[$i]}" > "./${species_name[$i]}//filtered_locations.csv"
    filtered_location_file_path=./${species_name[$i]}//filtered_locations.csv
    # Define the museum array correctly
    echo "Processing location filtered file: ${species_name[$i]} for museum/institution type"
    museum=("AMNH" "FMNH" "iNaturalist" "KU" "MVZ" "NHMUK" "NMR" "SMF" "USNM" "YPM")
    # go through the museums and count
    for entry in "${museum[@]}"; do
        count=$(grep -c "$entry" "$filtered_location_file_path")
        echo "$entry: $count"
    done
done
exit
