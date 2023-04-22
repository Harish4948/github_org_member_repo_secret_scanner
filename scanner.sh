 #!/bin/bash
 
 # Get current datetime with unique random number
 echo “Getting current datetime with unique random number”
 current_time=$(date “+%Y_%m_%d_%H_%N”)
 copy_file=“$current_time”_new_repos.txt
 
 # Copy new_repos.txt to copy_file
 echo “Copying new_repos.txt to copy_file”
 cp new_repos.txt ./output/“$copy_file”
 
 # Iterate over the repos in copy_file and run trufflehog
 echo “Running trufflehog with --json flag for each repo”
 for repo in $(cat ./output/$copy_file); do
     # Set output file name
     output_file=“$current_time”_“$RANDOM”_truffle
     # Run trufflehog with --json flag and save output in output_file
     echo “Running trufflehog with --json flag for repo: $repo”
     trufflehog --json git “$repo” --no-update >> ./output/“$output_file”
 
     # Check if DetectorName is present in the output file
     if grep -q “DetectorName” ./output/$output_file; then
         cat ./output/$output_file | notify -id gitalert
     fi
 done 
 
 # Delete copy_file
 echo “Deleting copy_file”
 rm “./output/$copy_file”