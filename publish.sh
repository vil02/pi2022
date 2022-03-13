#!/usr/bin/env bash

set -euo pipefail

script_lock=$(dirname "${0}")/"publish_lock_dir"
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

./build_document.sh ||
{
    remove_lock
    printf "Cannot build document.\n"
    exit 4
}

if [[ $(find ./latex/*.pdf | wc -l) -ne 1 ]]
then
    remove_lock
    printf "Unexpected number of documents.\n"
    exit 5
fi

output_folder=$(./get_output_folder.sh) ||
{
    remove_lock
    printf "Cannot get the result folder\n"
    exit 6
}
readonly output_folder

rm -rf "$output_folder" ||
{
  remove_lock
  printf "Cannot clean results folder.\n"
  exit 7
}

mkdir "$output_folder" ||
{
  remove_lock
  printf "Cannot create results folder.\n"
  exit 8
}
mv ./latex/*.pdf "$output_folder" ||
{
  remove_lock
  printf "Cannot move document to the result folder.\n"
  exit 9
}

./generate_checksums.sh ||
{
    remove_lock
    printf "Cannot create checksums.\n"
    exit 10
}

remove_lock
