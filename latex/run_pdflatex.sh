#!/bin/bash

set -euo pipefail

script_lock=$(dirname "${0}")/"build_lock_dir"
readonly script_lock

declare -r core_name="pi2022"
declare -r tex_file="${core_name}.tex"
declare -r pdf_file="${core_name}.pdf"

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

rm -f ${pdf_file} ||
{
    remove_lock
    printf "Cannot remove the old result file\n"
    exit 4
}

pdflatex -interaction=batchmode "$tex_file" || true
pdflatex -interaction=batchmode "$tex_file" || true

pdflatex -interaction=batchmode "$tex_file" ||
{
    remove_lock
    printf "Error while building document (LaTeX)\n"
    exit 5
}

if ! [ -e ${pdf_file} ]
then
  remove_lock
  printf "Error while building document (document not created)\n"
  exit 6
fi

remove_lock
