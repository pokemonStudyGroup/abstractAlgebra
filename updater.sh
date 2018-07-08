#!/bin/bash
trap cleanup INT

cleanup() {
  echo "Killed"
  popd
  exit
}

main() {
  echo $$ > /tmp/updater_pid 
  pushd /home/ubuntu/abstractAlgebra/
  
  while [ true ]
  do
  
    echo "Downloading source..."
    time python3 get_source.py
    
    echo "Extracting source..."
    time {
      yes | unzip /tmp/source.zip
    }
    
    echo "Pushing to github..."
    time {
      git add .
      git commit -m "Update at $(date)"
      git push origin master
    }
    
    echo "Sleeping..."
  
    sleep $(( $(cat /tmp/interval) )) &
    sleep_pid=$!
    echo $sleep_pid > /tmp/sleep_pid
    wait $sleep_pid
  
  done
}

main 2>&1 | tee /tmp/output
