
test="/home/chipdelmal/Documents"

# for entry in "$test"/*
# do
#   echo "$entry"
# done

find "$test"/* -maxdepth 0 -mindepth 0 -type d | while read dir; do
  echo "$(basename $dir)"
done