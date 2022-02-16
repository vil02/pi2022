#!/usr/bin/env bash

set -euo pipefail

script_lock=$(dirname "${0}")/"checksum_generator_lock_dir"
readonly script_lock

function is_already_running()
{
    declare -i return_value=0
    test -d "${script_lock}" ||
    {
        return_value=1
    }
    return "${return_value}"
}

function create_lock()
{
    mkdir "${script_lock}" ||
    {
        printf "Cannot create lock\n"
        exit 2
    }
}

function remove_lock()
{
    rm -rf "${script_lock}" ||
    {
        printf "Cannot remove lock\n"
        exit 3
    }
}

if is_already_running
then
    printf "Cannot acquire lock (another instance is running?) - exiting.\n"
    exit 1
fi

create_lock

core_name=$(./get_checksum_core_name.sh) ||
{
    remove_lock
    printf "Cannot get the checksums core name\n"
    exit 5
}
readonly core_name

output_folder=$(./get_output_folder.sh) ||
{
    remove_lock
    printf "Cannot get the result folder\n"
    exit 6
}
readonly output_folder

cd "$output_folder" ||
{
    remove_lock
    printf "Cannot access result folder\n"
    exit 7
}

for sum_t in "md5sum" "sha1sum" "sha224sum" "sha384sum" "sha256sum" "sha512sum"
do
    $sum_t ./*.pdf  > "$core_name"."${sum_t::${#sum_t}-3}" ||
    {
        remove_lock
        printf "Error while generating %s\n" $sum_t
        exit 8
    }
done

cd -

remove_lock
