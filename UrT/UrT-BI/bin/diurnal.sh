#!/bin/sh
cd /var/www/bin
./getGameLogs.php
./getQconsoleLogs.php
./getServerConfigs.php
./getBanLists.php
./importNewUsers.php
