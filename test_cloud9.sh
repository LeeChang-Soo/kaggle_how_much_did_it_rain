#!/bin/bash

scp ddboline@ddbolineathome.mooo.com:/home/ddboline/setup_files/build/kaggle_how_much_did_it_rain/how_much_did_it_rain.tar.gz .
tar zxvf how_much_did_it_rain.tar.gz
rm how_much_did_it_rain.tar.gz

./my_model.py $1 > output_${1}.out 2> output_${1}.err

D=`date +%Y%m%d%H%M%S`
tar zcvf output_${1}_${D}.tar.gz model_${1}.pkl.gz output_${1}.out output_${1}.err
scp output_${1}_${D}.tar.gz ddboline@ddbolineathome.mooo.com:/home/ddboline/setup_files/build/kaggle_how_much_did_it_rain/
ssh ddboline@ddbolineathome.mooo.com "~/bin/send_to_gtalk done_kaggle_how_much_did_it_rain_${1}"
echo "JOB DONE ${1}"
