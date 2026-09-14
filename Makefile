all:
	hugo server -D --bind=0.0.0.0 --port=8080 --baseURL https://dev.drydave.dev/ --liveReloadPort=443 --appendPort=false --disableFastRender
dist:
	hugo -D --minify --baseURL http://drydave.dev/
	rsync -av --delete public/ /var/www/html
