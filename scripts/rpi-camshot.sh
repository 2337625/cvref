#!/bin/sh

# Captures a picture triggered by motion or other sensor attached to
# Raspberry Pi via GPIO and sends it to custom page, pulling back
# a QR code.

WIDTH=1280
HEIGHT=1024
QUALITY=100
TIMEOUT=0
ENCODING='jpg'
SHARPNESS=0
CONTRAST=-20
ISO=700
EXPOSURE=auto
AWB=auto
EFFECT=none
HOST=`hostname`
LOCATION='passioncomm'
DIR='/home/pi/Pictures/cheers/'
UPLOADURL='http://prototype.passioncomm.com/photos/new'
PDFDIR='/home/pi/Pictures/cheers/'
`gpio mode 3 up`
PDF='20.pdf'
PRINTER='epson'

while true; do
	TIMECREATED=`date -u '+%Y-%m-%d--%H-%M-%S'`;
	IMAGE=$HOST'-'$TIMECREATED'.jpg';
	GPIO=`gpio read 3`;
	IMAGEBASE='';

	if [ $GPIO -eq 0 ]; then
		raspistill -o $DIR$IMAGE -w $WIDTH -h $HEIGHT -q $QUALITY -t $TIMEOUT 
		#raspistill -o $DIR$IMAGE -w $WIDTH -h $HEIGHT -q $QUALITY -t $TIMEOUT -sh $SHARPNESS -co $CONTRAST -ISO $ISO -ex $EXPOSURE -awb $AWB -ifx $EFFECT;
		sleep 5;
		$RESPONSE="$(curl -v -X POST -d '{"image":`base64|$DIR$IMAGE`,"location":$LOCATION,"time_created":$TIMECREATED}' -H 'Content-type: application/json; charset=UTF8' --max-time 180 $UPLOADURL)";
		wget -O $PDFDIR$PDF http://prototype.passioncomm.com/coupon-generate/20.pdf;
		echo $RESPONSE;
		#lpr -P $PRINTER $PDFDIR$PDF;

	fi
done
