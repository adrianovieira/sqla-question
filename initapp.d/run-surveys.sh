#!/bin/sh +x
echo " ✔ Instaling the simple app dependencies!"
apk add postgresql-client  > /dev/null 2>&1
pip install sqlalchemy psycopg["binary"]  > /dev/null 2>&1

TIMEOUT=05

check_postgres() {
  psql -h "pg-server" -U surveys -d surveys -c "SELECT * FROM analysis.mview_surveys_loaded_at_status limit 1;" > /dev/null 2>&1
  return $?
}

echo " ✔ Verifing if the sample data has been loaded."
echo -n "   Attempt... "

DB_OK=false

for t in `seq 1 ${TIMEOUT}`
do
    if check_postgres
    then
        echo $t its OK
        DB_OK=true
        break
    fi
    echo -n "${t} "
    sleep 1 # wait 1s to try again
done

if $DB_OK
then
    echo -e " ✔ Here we go..."
    python surveys.py
else
    echo -e "\n ERROR: MATERIALIZED VIEW not found"
fi