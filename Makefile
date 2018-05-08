NAME := leftparagraphs
DHPARAM = /etc/nginx/conf/leftparagraphs.com/dh_param.pem

www-configs-install: configs/nginx.conf configs/uwsgi.conf
	#configuring uwsgi
	install --owner=www-data --group=www-data configs/uwsgi.conf /etc/uwsgi/apps-available/$(NAME).conf
	ln -sf /etc/uwsgi/apps-available/$(NAME).conf /etc/uwsgi/apps-enabled/$(NAME).conf
	#creating upstart job
	install configs/service.conf /etc/init/$(NAME).conf
	stop $(NAME); start $(NAME)
	#configuring nginx
	if [ ! -f "$(DHPARAM)" ]; \
	then \
		echo "Generating custom dh_param at /tmp/dh_param.pem"; \
		openssl dhparam -out "/tmp/dh_param.pem" 2048; \
		install --mode=600 --owner=www-data --group=www-data "/tmp/dh_param.pem" "$(DHPARAM)"; \
	fi
	install --owner=www-data --group=www-data configs/nginx.conf /etc/nginx/sites-available/$(NAME).conf
	ln -sf /etc/nginx/sites-available/$(NAME).conf /etc/nginx/sites-enabled/$(NAME).conf
	service nginx reload


www-reload:
	touch /var/run/uwsgi/leftparagraphs.reload


requirements.txt:
	pip list --local --format=freeze | sort --ignore-case | tee $@

.PHONY: requirements.txt
