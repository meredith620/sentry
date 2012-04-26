#! /bin/bash
##################################################################
#   Filename   :  autodeploy.sh
#   Description:  
#   Version    :  1.0
#
#   Author     :  lvliang@miaozhen.com
#   Department :  DSP
#   Company    :  miaozhen system
#========= history ==========
#date		author	content
#2012-03-20	lvliang	created
##################################################################

target_dir="conf"

deploy_one()
{
    deploy_conf=$1
    sed_list=$2
    copy_list=$3

    if [[ (! -e $deploy_conf) || (! -e $sed_list) || (! -e $copy_list) ]];then
        echo "ERROR file not exits: $deploy_conf or $sed_list or $copy_list"
        return 1
    fi
    
    rm -rf $target_dir

#genrate files
    while read line
    do
	   cmd="./generate_conf.sh -f $deploy_conf -g $line -d $target_dir"
	   #echo $cmd
	   eval $cmd
    done < $sed_list

#copy files
    while read line
    do
	   cmd="./generate_conf.sh -f $deploy_conf -c $line -d $target_dir"
	   #echo $cmd
	   eval $cmd
    done < $copy_list

#do deploy
    ./deploy.sh $deploy_conf $target_dir
}

deploy_one detail/deploy.conf detail/sed_list detail/cp_list

