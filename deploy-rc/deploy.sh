#! /bin/bash
##################################################################
#   Filename   :  deploy.sh
#   Description:  do deploy
#   Version    :  1.0
#
#   Author     :  lvliang@miaozhen.com
#   Department :  DSP
#   Company    :  miaozhen system
#========= history ==========
#date		author	content
#2012-03-20	lvliang	created
##################################################################

############# local function #############
declare -a fail;
display_result()
{
#显示启动结果信息
    if ((${#fail[@]} == 0));then
           echo -e "\e[1;32;40m[finish!]\e[m"
    else
           echo -e "\e[1;31;40m[failed!]\e[m in"
           for x in ${fail[@]};
           do
                  echo -e "\t" "$x"
           done
    fi    
}

get_error_msg()
{
    for x in $@
    do
           fail[${#fail[@]}]=$x
    done
}
###########################################
if (($# != 2));then
    echo $0 model_var conf_dir
    exit 1
fi

SCCUESS=0
ERROR=1
model_var_file=$1
conf_dir=$2

remote_deploy()
{
    addr=$1
    local conf_dir_=$2
    local num_=$3
    DIRECT="/tmp/papa_deploy_temp"    
    deploy_cmd="rm $DIRECT -rf; mkdir $DIRECT"
    echo | ssh -o StrictHostKeyChecking=no $addr "$deploy_cmd"
    
    cd $conf_dir_
    prefix="${num_}-${addr}-"
    target=`ls ${prefix}*`
    cd -
    for x in $target
    do
	   scp conf/$x ${addr}:${DIRECT}/${x#${prefix}}
	   if (($? != $SCCUESS));then
		  echo "FAILED: scp conf/$x ${addr}:${DIRECT}/${x#${prefix}}"
		  return $ERROR;
	   fi
    done
    deploy_cmd="cd $DIRECT; make install"
    echo | ssh $addr "$deploy_cmd"
    if (($? != $SCCUESS));then
	   echo "FAILED: $deploy_cmd"
	   return $ERROR;
    fi
    
    deploy_cmd="rm $DIRECT -rf"
    echo | ssh $addr "$deploy_cmd"
}

i=0
while read line
do
    if ((${#line} == 0));then
	   continue
    fi
    pos=`expr index $line "="`
    if ((pos == 0));then # section head
	   echo "new section - ${i}-$line"
	   remote_deploy ${line} $conf_dir $i
	   if (($? != $SCCUESS));then
		  get_error_msg $line;
	   fi
	   i=$((i+1))
    fi
done < $model_var_file

display_result
