container="$1"

TARGET=/tmp/${container}

TAR_FILENAME=$TARGET/container.tar.gz
INFO_FILENAME=$TARGET/latest_info

curl --ftp-create-dirs -T $TAR_FILENAME -u $ftpuser:$ftppass ftp://blog.itkpi.pp.ua/${container}/latest.tar.gz
curl --ftp-create-dirs -T $INFO_FILENAME -u $ftpuser:$ftppass ftp://blog.itkpi.pp.ua/${container}/latest_info
