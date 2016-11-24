#! /bin/sh

install_cron() {
    if crontab -l | grep "/root/mussstat/probe.py"; then
        echo "Already have cron job"
    else
        echo "Install cron job"
        PYTHON_PATH=`which python`
        TMP_FILE=crontab-mussstat.tmp
        crontab -l > $TMP_FILE
        echo "*/5 * * * * $PYTHON_PATH /root/mussstat/probe.py > /dev/null 2>&1" >> $TMP_FILE
        crontab $TMP_FILE
        rm $TMP_FILE
    fi
}

install_cron
