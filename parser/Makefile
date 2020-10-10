ENV_FILE = app/.env

include ${ENV_FILE}
export


db:
	PGPASSWORD='${DB_PASSWORD}' psql -h ${DB_HOST} -U ${DB_USER} ${DB_NAME}

scrapyd:
	sudo systemctl restart scrapyd.service

scrapyd_stop:
	sudo systemctl stop scrapyd.service

crontab:
	sudo service cron restart

scrapyd_logs:
	tail -f logs/default/flat_spider/*

crontab_logs:
	grep CRON /var/log/syslog

scrapyd_client:
	scrapyd-client schedule -p default --arg part=0 --arg total=5 flat_spider
	scrapyd-client schedule -p default --arg part=1 --arg total=5 flat_spider
	scrapyd-client schedule -p default --arg part=2 --arg total=5 flat_spider
	scrapyd-client schedule -p default --arg part=3 --arg total=5 flat_spider
	scrapyd-client schedule -p default --arg part=4 --arg total=5 flat_spider
