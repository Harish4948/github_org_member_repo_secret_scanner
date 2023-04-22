#!/bin/bash -e

SECONDS=0
# do some work

# Get current datetime with unique random number
echo "Getting current datetime with unique random number"
current_time=$(date "+%Y_%m_%d_%H_%N")
copy_file="$current_time"_new_repos_copy.txt
tmp_dir=$PWD/tmp_"$current_time"

mkdir -p $tmp_dir $PWD/output

# Copy new_repos.txt to copy_file
echo "Copying new_repos.txt to copy_file"
cp $PWD/new_repos.txt $tmp_dir/$copy_file
# Iterate over the repos in copy_file and run trufflehog
echo "Running trufflehog with --json flag for each repo"

output_file="$current_time"_output.json

cat $tmp_dir/$copy_file | parallel -j 4 --keep-order /usr/local/bin/trufflehog --json git {} --no-update ">>" 
$PWD/output/$output_file

echo "User Public Repositories Scan Results:" >> $tmp_dir/notify.txt
if [ -s $PWD/output/$output_file ]
then

cat $PWD/output/$output_file | jq -r .DetectorName > $tmp_dir/detectors.txt
cat $tmp_dir/detectors.txt | sort -u > $tmp_dir/uniq.txt
echo -e "New Repos: \n" >> $tmp_dir/notify.txt
cat $tmp_dir/$copy_file >> $tmp_dir/notify.txt
echo -e "\n" >> $tmp_dir/notify.txt
for i in $(cat $tmp_dir/uniq.txt)
do
echo $i : `grep -c "$i" $tmp_dir/detectors.txt` >> $tmp_dir/notify.txt
done

else
rm -v $PWD/output/$output_file
echo "Output file removed since it was empty."
echo "No Results found" >> $tmp_dir/notify.txt
fi

cat $tmp_dir/notify.txt | notify -bulk -id gitalert

echo "Deleting temp files"
rm -rfv $tmp_dir

duration=$SECONDS
echo "$(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed."
