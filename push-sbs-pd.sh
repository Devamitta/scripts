echo "copy sbs-pd"

cp -rf ~/Documents/GoldenDict/sbs-pd ~/filesrv1/share1/Sharing\ between\ users/1\ For\ Everyone/Software/Golden\ Dictionary/Default/

cp -f "/home/deva/Documents/dps/exporter/share/sbs-pd.zip" "/home/deva/Documents/sasanarakkha/study-tools/temp-push/sbs-pd.zip"

echo "sbs-pd moved on the server"

cd "/home/deva/Documents/sasanarakkha/study-tools"

gh release upload --clobber 'artifacts-12.04.2023_03-10-19' temp-push/sbs-pd.zip

echo "sbs-pd uploaded on GitHub"