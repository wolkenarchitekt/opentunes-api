#!/bin/bash
# Install autoflake, black and isort and prettier before usage!
TMP_ROOT=/tmp/autoformat

autoformat_file() {
    file="${1}"

    file="${file}"
    tmpfile="$(mktemp /tmp/XXXXXXXXXXX)"
    cp "${file}" "${tmpfile}"
    echo "${file}"

    if [[ "${file}" == *.py ]]; then
      autoflake --in-place --remove-all-unused-imports "${file}"
      isort "${file}"
      black -q "${file}"
    elif [[ "${file}" == *.js ]]; then
      prettier --write "${file}"
    elif [[ "${file}" == *.sql ]]; then
      sqlformat \
        --reindent \
        --keywords upper \
        --identifiers lower \
        -o "${file}" \
        "${file}"
    elif [[ "${file}" == *.json ]]; then
      jq . "${tmpfile}" > "${file}"
    fi
    git --no-pager diff "${tmpfile}" "${file}"
}

for file in "${@}"; do
  # Don't reformat file if it hasn't changed - save file mtime to cache
  TMP_FILE="${TMP_ROOT}/${file}"
  mkdir -p "${TMP_ROOT}/$(dirname ${file})"
  if [ -f "${TMP_FILE}" ] && [ "$(stat --format='%Y' ${TMP_FILE})" -eq "$(stat --format="%Y" ${file})" ]; then
    continue
  fi

  autoformat_file "${file}"

  # Update cache
  touch "${TMP_FILE}"
  touch -r "${file}" "${TMP_FILE}"
done
