#!/bin/sh
sed -i 's/\[SERVER_ADDR\] /${SERVER_ADDR}\ /gi' /etc/nginx/conf.d/default.conf
supervisord