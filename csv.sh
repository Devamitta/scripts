echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
echo "making csv with bold"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

# mv "../spreadsheets/dps.ods" "dps.ods"

python3 ods-to-csv-headers.py "../spreadsheets/dps.ods" PALI 39

# mv "dps.ods" "../spreadsheets/dps.ods"

# mv "dps.csv" "../spreadsheets/dps-class.csv"

echo "dps completed"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

python3 nidh-xls-to-csv.py

echo "nidh completed"
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"