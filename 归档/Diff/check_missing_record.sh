#!/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/root/bin
export PATH

# Print Help for -h|-help

if [[ $1 == '-h' ]] || [[ $1 == '-help' ]]; then
  printf 'Usage: ./check_missing_record.sh <CRM_PATH> <DI_PATH> <REPORT_PATH>\nPlease use full path like: ./check_missing_record.sh /tmp/crm/ /tmp/di/ /root/compare/\n';
  exit 0;
fi

if [[ $# != 3 ]]; then
  printf 'Not enough arguments, using defaults:\n';
  printf 'MSSQL: /home/sqlsync/report/report/report/mssql/\nMYSQL: /home/sqlsync/report/report/report/mysql/\nREPORT: /home/sqlsync/report/report/report/result/\n';
  DIR1=/home/sqlsync/report/report/report/mssql/
  DIR2=/home/sqlsync/report/report/report/mysql/
  RPT=/home/sqlsync/report/report/report/result/
else
  DIR1=$1
  DIR2=$2
  RPT=$3
fi

if [ -d "$DIR1" ] && [ -d "$DIR2" ]; then
  echo "";
else
  printf 'Please input directories!\n';
  printf 'Usage: ./check_missing_record.sh <CRM_PATH> <DI_PATH> <REPORT_PATH>\nPlease use full path like: ./check_missing_record.sh /tmp/crm/ /tmp/di/ /root/compare/\n';
  exit 0;
fi

# confirm the path for $3,
# if not exist, then create it
# if exists, confirm for use, delete tmp folder and move result folder for backup while yes

if [ -d "$RPT" ]; then
    rm -rf ${RPT}tmp/*;
    if [ -d "${RPT}result" ]; then
      mv ${RPT}result ${RPT}result.`date +%Y%m%d-%H%M%S`;
      mkdir -p ${RPT}result;
    fi
else
  mkdir -p $RPT{tmp,result}
fi

DATE=`date +%Y-%m-%d\ %H:%M:%S`
printf 'Date: %s\n' "${DATE}"
printf 'Date: %s\n' "${DATE}" >> ${RPT}report.txt
printf '%25s\t%8s\t%8s\t%8s\t%8s\t%8s\t%4s\n' Table CRM DI NotSync Expired Deleted Rate
printf '%25s\t%8s\t%8s\t%8s\t%8s\t%8s\t%4s\n' Table CRM DI NotSync Expired Deleted Rate >> ${RPT}report.txt


for i in `ls ${DIR1}`;
do

  cat ${DIR1}/${i} ${DIR2}/${i} | sort | uniq -d >> ${RPT}result/synced_${i};
  cat ${DIR1}/${i} ${RPT}result/synced_${i} | sort | uniq -u | cut -d ";" -f 1 >> ${RPT}tmp/old_only_${i};
  cat ${DIR2}/${i} ${RPT}result/synced_${i} | sort | uniq -u | cut -d ";" -f 1 >> ${RPT}tmp/new_only_${i};
  cat ${RPT}tmp/old_only_${i} ${RPT}tmp/new_only_${i} | sort | uniq -d >> ${RPT}result/expired_${i};
  cat ${RPT}tmp/old_only_${i} ${RPT}result/expired_${i} | sort | uniq -u >> ${RPT}result/notsync_${i};
  cat ${RPT}tmp/new_only_${i} ${RPT}result/expired_${i} | sort | uniq -u >> ${RPT}result/deleted_${i};

  TABLE=${i};
  CRMCNT=`cat ${DIR1}/${i} | wc -l`
  DICNT=`cat ${DIR2}/${i} | wc -l`
  NSYNC=`cat ${RPT}result/notsync_${i} | wc -l`;
  EXP=`cat ${RPT}result/expired_${i} | wc -l`;
  DEL=`cat ${RPT}result/deleted_${i} | wc -l`;
  SYN=`cat ${RPT}result/synced_${i} | wc -l`
  RATE=`echo "scale=2; 100*${SYN}/${CRMCNT}"|bc`;
  printf '%25s\t%8i\t%8i\t%8i\t%8i\t%8i\t%4.2f\n' "${TABLE}" ${CRMCNT} ${DICNT} ${NSYNC} ${EXP} ${DEL} ${RATE};
  printf '%25s\t%8i\t%8i\t%8i\t%8i\t%8i\t%4.2f\n' "${TABLE}" ${CRMCNT} ${DICNT} ${NSYNC} ${EXP} ${DEL} ${RATE} >> ${RPT}report.txt;
done;