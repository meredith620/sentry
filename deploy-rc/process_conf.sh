#! /bin/bash
#
##################################################################
#   Filename   :  process_conf.sh
#   Description:  handle conf files
#   Version    :  1.0
#
#   Author     :  lvliang@miaozhen.com
#   Department :  DSP
#   Company    :  miaozhen system
#========= history ==========
#date		author	content
#2012-03-20	lvliang	created
##################################################################

ROW=1000
# struct 2 dimention array
# key_array[i*ROW+j]
# value_array[i*ROW+j]
# i -- section
# j -- varnum
declare -a key_array
declare -a value_array

# sava global var
# if there is the same var name in one section, and it will replace the global vars 
declare -a g_key_array
declare -a g_value_array

# struct 1 dimention array
# key_num_array[i] = number of keys in this section
declare -a key_num_array
declare -a section_name_array

#read conf to section and key-value
read_conf()
{
    conf_file=$1
    i=-1 #section
    j=-1 #varnum
    
    # set global vars    
    while read line
    do
	   if ((${#line} == 0));then
		  continue
	   fi
	   pos=`expr index $line "="`
	   if ((pos == 0)); then #new section
		  break;
	   fi	   
	   key=${line%=*}
	   value=${line#*=}
	   g_key_array[${#g_key_array[@]}]=$key
	   g_value_array[${#g_value_array[@]}]=$value
    done < $conf_file
    
    # set section vars
    global_is_set=0 # past the global section
    while read line
    do
	   if ((${#line} == 0));then
		  continue
	   fi
	   pos=`expr index $line "="`
	   if ((pos == 0));then # section head
		  echo "new section - $line"
	   #a new section
		  global_is_set=1
		  if ((j >= 0));then
		  #last section has var or do not increase i,j,change any array
			 key_num_array[i]=$((j+1)) #last section var num
			 section_name_array[i]=${secname}		  
			 j=-1; #init new var number
		  fi
		  ((i++)) #section number increase
		  secname=${i}-$line #secname $num-$addr

		  # copy the global var
		  for ((k=0; k < ${#g_key_array[@]}; k++))
		  do
			 key_array[i*ROW+k]=${g_key_array[k]}
			 value_array[i*ROW+k]=${g_value_array[k]}
		  done
		  j=$((k-1))
		  
	   elif ((global_is_set != 0));then # section body
	   # echo -e "\tget body - $line"
		  key=${line%=*}
		  value=${line#*=}
		  
		  #for the global var
		  #find the same name of global var
		  for ((k=0; k < ${#g_key_array[@]}; k++))
		  do
			 if [[ ${g_key_array[k]} == $key ]];then
				break;
			 fi
		  done

		  if ((k<${#g_key_array[@]}));then
			 #if exist global var name, replace it
			 value_array[i*ROW+k]=$value
		  else
			 #if new var, append to array
			 ((j++))
			 key_array[i*ROW+j]=$key
			 value_array[i*ROW+j]=$value
		  fi
	   fi    
    done < $conf_file
#process the last section
    if ((j >= 0));then
    #last section has var or do not increase i,j,change any array
	   key_num_array[i]=$((j+1)) #last section var num
	   section_name_array[i]=$secname
	   j=-1; #init new var number
    fi
}

print_key_value()
{
    local i=0
    local j=0
    echo "global var num: ${#g_key_array[@]}";
    for ((i = 0; i < ${#g_key_array[@]}; i++))
    do
	   echo -e "\tkey - ${g_key_array[i]} \t value - ${g_value_array[i]}"
    done

    echo "all section num: ${#key_num_array[@]}"
    i=0
    j=0
    for ((i = 0; i < ${#key_num_array[@]}; i++))
    do
	   echo -e "\tsection ${section_name_array[i]}";
	   for ((j = 0; $j < ${key_num_array[i]}; j++))
	   do
		  echo -e "\t\tkey - ${key_array[i*ROW+j]} \t value - ${value_array[i*ROW+j]}";
	   done
    done
}

sed_substitude()
{
    model=$1
    confdir=$2
    echo "generate $model"
    local i=0
    local j=0
    # echo "all section num: ${#key_num_array[@]}"    
    if [ ! -d $confdir ];then
	   mkdir $confdir
    fi
    for ((i = 0; i < ${#key_num_array[@]}; i++))
    do
	   # echo -e "\tsection ${section_name_array[i]}";
	   sedcmd=""
	   for ((j = 0; $j < ${key_num_array[i]}; j++))
	   do
		  # echo -e "key - ${key_array[i*ROW+j]} \t value - ${value_array[i*ROW+j]}";
		  sedcmd="${sedcmd};s=${key_array[i*ROW+j]}=${value_array[i*ROW+j]}=g"
	   done
	   # echo "cmd: $sedcmd"
	   sed -e "{$sedcmd}" $model > $confdir/${section_name_array[i]}-${model##*/}
    done
}

copy_model()
{
    file=$1
    confdir=$2
    echo "copy $file"
    local i=0
    local j=0
    # echo "all section num: ${#key_num_array[@]}"    
    if [ ! -d $confdir ];then
	   mkdir $confdir
    fi
    for ((i = 0; i < ${#key_num_array[@]}; i++))
    do
	   cp $file $confdir/${section_name_array[i]}-${file##*/}
    done	   
}
