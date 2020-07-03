#!/bin/bash

# $1 - Api key
# $2 - Client secret

api_key='AIzaSyBV1HvfE3nQuJqBiW1a_dZhZyhPEkWpIJw'

secret_file=$(find $1 -name "client_secret*.json" |  head -n 1)


client_id=$(cat $secret_file | jq '.installed.client_id')
client_secret=$(cat $secret_file | jq '.installed.client_secret')
scope='https://www.googleapis.com/auth/streetviewpublish'

#strip quotes

client_id="${client_id%\"}"
client_id="${client_id#\"}"

client_secret="${client_secret%\"}"
client_secret="${client_secret#\"}"



# Client id from Google Developer console
# Client Secret from Google Developer console
# Scope this is a space seprated list of the scopes of access you are requesting.


# Authorization link.  Place this in a browser and copy the code that is returned after you accept the scopes.

echo 'Upload panoramic photos to Google Street View'
echo
echo 'Open browser, and copy code'
echo
echo 'https://accounts.google.com/o/oauth2/auth?client_id='$client_id'&redirect_uri=urn:ietf:wg:oauth:2.0:oob&scope='$scope'&response_type=code'
echo
read -p "Enter authorization code: " auth_code 

echo 
echo 'Exchange Authorization code for an access token and a refresh token.'





data="code=$auth_code&client_id=$client_id&client_secret=$client_secret&redirect_uri=urn:ietf:wg:oauth:2.0:oob&grant_type=authorization_code"
echo $data
exchange_result="$(curl -s \
--request POST \
--data $data \
https://accounts.google.com/o/oauth2/token)"

echo $exchange_result | jq '.'


access_token=$(echo $exchange_result | jq '.access_token')
refresh_token=$(echo $exchange_result | jq '.refresh_token')

#strip quotes

access_token="${access_token%\"}"
access_token="${access_token#\"}"

refresh_token="${refresh_token%\"}"
refresh_token="${refresh_token#\"}"

echo token=$access_token



# do query
#curl -s --request GET  --url "https://streetviewpublish.googleapis.com/v1/photos?pageSize=10&view=INCLUDE_DOWNLOAD_URL&key="$api_key --header "Authorization: Bearer ${access_token}" | jq '.'


function get_data_json {

# $1 - path to jpg
# 2 - upload_url
url=$2

json_data=$(exiftool -q -q  -json -n   -gpslatitude -gpslongitude -gpsimgdirection -gpsdatetime $1)

lat=$(jq -n "$json_data" | jq  '.[].GPSLatitude'  )
lon=$(jq -n "$json_data" | jq  '.[].GPSLongitude'  )
dir=$(jq -n "$json_data" | jq  '.[].GPSImgDirection'  )
tme=$(jq -n "$json_data" | jq  '.[].GPSDateTime' | tr -d \" )
tme=${tme:0:4}${tme:5:2}${tme:8:2}${tme:10:9} #simple convert datetime for convert to unixtime
tme=$(date --date "$tme" +%s)

TEMPLATE='{"uploadReference":{"uploadUrl": "%s"
                  },"pose":{"heading": %s,
                     "latLngPair":
                     { "latitude": %s,
                       "longitude": %s
                     }}, "captureTime":{"seconds": %s},}'
					 
exp_json=$(printf "$TEMPLATE" "$url"  "$dir"  "$lat" "$lon" "$tme" )
exp_json=$(jq -n "$exp_json")

echo $exp_json	
}  



dir='/data/mapillary/test/'
dir=$(realpath $dir)
uploaded_dir=$dir/'uploaded2gsv'

mkdir $uploaded_dir

#start timer
time1=$(date +%s)

for filename in $dir/*.JPG
do
	echo $filename
	#filename='/data/mapillary/test/IMG_20200627_190002_3566343.JPG'

	#get upload URL
	upload_url_json="$(curl --request POST \
			--url "https://streetviewpublish.googleapis.com/v1/photo:startUpload?key=${api_key}" \
			--header "Authorization: Bearer ${access_token}" \
			--header 'Content-Length: 0')"
			
	upload_url=$(jq -n "$upload_url_json" | jq '.uploadUrl')		

	#strip quotes
	upload_url="${upload_url%\"}"
	upload_url="${upload_url#\"}"	

	echo 
	echo 'post image'
	#post image
	post_image_response="$(curl --request POST \
			--url "${upload_url}" \
			--upload-file "${filename}" \
			--header "Authorization: Bearer ${access_token}" \
			)"
			

	echo $post_image_response

	image_metadata_json=$(get_data_json $filename $upload_url)

	#post image metadata
	#post_metadata_response="$(curl --request POST \
	#		--url "https://streetviewpublish.googleapis.com/v1/photo?key=${api_key}" \
	#		--header "Authorization: Bearer ${access_token}" \
	#		--header 'Content-Type: application/json' \
	#		--data  "${image_metadata_json}"
	#		)"
			
	# creates a new file descriptor 3 that redirects to 1 (STDOUT)
	
	echo curl --request POST \
			--url "https://streetviewpublish.googleapis.com/v1/photo?key=${api_key}" \
			--header "Authorization: Bearer ${access_token}" \
			--header 'Content-Type: application/json' \
			--data  "${image_metadata_json}"
	
	exec 3>&1 
	# Run curl in a separate command, capturing output of -w "%{http_code}" into HTTP_STATUS
	# and sending the content to this command's STDOUT with -o >(cat >&3)
	#echo curl -w "%{http_code}" -o >(cat >&3) --request POST --url "https://streetviewpublish.googleapis.com/v1/photo?key=${api_key}" --header "Authorization: Bearer ${access_token}" --header 'Content-Type: application/json' --data  "${image_metadata_json}" 
	#HTTP_STATUS=$(curl -w "%{http_code}" -o >(cat >&3) --request POST --url "https://streetviewpublish.googleapis.com/v1/photo?key=${api_key}" --header "Authorization: Bearer ${access_token}" --header 'Content-Type: application/json' --data  "${image_metadata_json}" )

	
	
	HTTP_STATUS="$(curl -w "%{http_code}" -o >(cat >&3) --request POST \
			--url "https://streetviewpublish.googleapis.com/v1/photo?key=${api_key}" \
			--header "Authorization: Bearer ${access_token}" \
			--header 'Content-Type: application/json' \
			--data  "${image_metadata_json}"
			)"
			
			
	
	echo 'STATUS='$HTTP_STATUS
	
	if [ "$HTTP_STATUS" != 200 ]; then
		echo  $filename 'STATUS='$HTTP_STATUS
		exit 0
	fi	
		
	echo $post_metadata_response
	mv $filename $uploaded_dir/$(basename $filename)
	
	
	#timer tick
	time2=$(date +%s)
	timedelta=$((time2-time1))
	#check for timer event
	#compare numbers in arichmetic context
	if (($timedelta > 60*40 )) ; then 
		echo 'timer signal';
		time1=$(date +%s);
		# Exchange a refresh token for a new access token.
		#curl \
		#--request POST \
		#--data 'client_id=[Application Client Id]&client_secret=[Application Client Secret]&refresh_token=[Refresh token granted by second step]&grant_type=refresh_token' \
		#https://accounts.google.com/o/oauth2/token
		
		
		data="client_id=$client_id&client_secret=$client_secret&refresh_token=$refresh_token&grant_type=refresh_token"
		echo $data

		exchange_result="$(curl -s \
		--request POST \
		--data $data \
		https://accounts.google.com/o/oauth2/token)"

		echo $exchange_result | jq '.'
		
		
		access_token=$(echo $exchange_result | jq '.access_token')

		#strip quotes
		access_token="${access_token%\"}"
		access_token="${access_token#\"}"
		
		


	fi


done	