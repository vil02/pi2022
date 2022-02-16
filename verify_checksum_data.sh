#!/usr/bin/env bash

set -euo pipefail

core_name=$(./get_checksum_core_name.sh) ||
{
    printf "Cannot get the checksums core name\n"
    exit 1
}
readonly core_name

output_folder=$(./get_output_folder.sh) ||
{
    printf "Cannot get the result folder\n"
    exit 2
}
readonly output_folder

cd "$output_folder" ||
{
    printf "Cannot access the result folder\n"
    exit 3
}

function get_checksum_type()
{
    local -r in_file_name=$(basename -- "$1")
    local -r in_file_ext="${in_file_name##*.}"
    echo "$in_file_ext"sum
}

declare -i result_code=0
for cur_file in ./"$core_name".*;
do
    checksum_type=$(get_checksum_type "$cur_file")
    printf "%s:\n" "$checksum_type"
    if ! $checksum_type --check ./*."${checksum_type::${#checksum_type}-3}"
    then
        result_code=1
    fi
done
exit $result_code
