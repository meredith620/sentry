#! /bin/bash
##################################################################
#   Filename   :  generate_conf.sh
#   Description:  do generate config files
#   Version    :  1.0
#
#   Author     :  lvliang@miaozhen.com
#   Department :  DSP
#   Company    :  miaozhen system
#========= history ==========
#date		author	content
#2012-03-20	lvliang	created
##################################################################

MYLANG="zh_CN.UTF-8"
source process_conf.sh

useage="cmd -f conf -g model -d target_dir\n
			generate config files \n"
model_var_file=""
while getopts "g:f:d:c:" arg
do
    case $arg in
	   g)
		  # echo "generate $OPTARG";
		  conf_model=$OPTARG
		  ;;
	   c)
		  # echo "copy $OPTARG";
		  copy_file=$OPTARG
		  ;;
	   f)
		  # echo "conf $OPTARG";
		  model_var_file=$OPTARG
		  ;;
	   d)
		  # echo "target_dir $OPTARG";
		  target_dir=$OPTARG
		  ;;
	   ?)
		  echo "unknow argument!";
		  echo ""
		  exit 1
		  ;;
    esac
done

if (( ${#model_var_file} == 0 ));then
    echo -e $useage
    exit 1
fi
if (( ${#target_dir} == 0 ));then
    echo -e $useage
    exit 1
fi

read_conf $model_var_file
# print_key_value

if (( ${#conf_model} > 0 ));then
    sed_substitude $conf_model $target_dir
fi

if (( ${#copy_file} > 0 ));then
    copy_model $copy_file $target_dir
fi
