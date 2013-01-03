echo 3 > /proc/sys/vm/drop_caches
cat ./large_data.rar | pv -p -e -r -t -b -s 4G -a > /dev/zero
