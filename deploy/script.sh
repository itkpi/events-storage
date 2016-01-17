container="$1"

TARGET=/tmp/${container}

mkdir -p $TARGET
TAR_FILENAME=$TARGET/container.tar.gz
INFO_FILENAME=$TARGET/latest_info

echo Build started `date` > $INFO_FILENAME
echo $container >> $INFO_FILENAME
echo "revision: `git rev-parse HEAD`" >> $INFO_FILENAME
git status >> $INFO_FILENAME

vagga _build ${container}
cp -R * .vagga/${container}/work/
echo nameserver 8.8.8.8 > .vagga/${container}/etc/resolv.conf
echo 127.0.0.1 localhost > .vagga/${container}/etc/hosts
vagga _pack_image ${container} | gzip > $TAR_FILENAME

echo Build finished `date` >> $INFO_FILENAME
