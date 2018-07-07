#!/bin/bash
trap cleanup INT

cleanup() {
  echo "Killed"
  popd
  exit
}
 
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
  sleep $(( 60 * 60 * 24 ))
done
