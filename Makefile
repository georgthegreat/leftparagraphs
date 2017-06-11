NAME := leftparagraphs
DHPARAM = /etc/nginx/conf/leftparagraphs.com/dh_param.pem

www-configs-install: configs/nginx.conf configs/uwsgi.conf
	#configuring uwsgi
	cp configs/uwsgi.conf /etc/uwsgi/apps-available/$(NAME).conf
	ln -sf /etc/uwsgi/apps-available/$(NAME).conf /etc/uwsgi/apps-enabled/$(NAME).conf
	#creating upstart job
	cp configs/service.conf /etc/init/$(NAME).conf
	stop $(NAME); start $(NAME)
	#configuring nginx
	if [ ! -f "$(DHPARAM)" ]; \
	then \
		echo "Generating custom dh_param at $(DHPARAM)"; \
		mkdir -m 700 -p $(dir $(DHPARAM)); \
		openssl dhparam -out "$(DHPARAM)" 2048; \
		chmod 700 "$(DHPARAM)"; \
		chown -R www-data:www-data $(dir $(DHPARAM)); \
	fi
	cp configs/nginx.conf /etc/nginx/sites-available/$(NAME).conf
	ln -sf /etc/nginx/sites-available/$(NAME).conf /etc/nginx/sites-enabled/$(NAME).conf
	service nginx reload


www-reload:
	touch /var/run/uwsgi/leftparagraphs.reload


requirements.txt: .PHONY
	pip freeze --local | sort --ignore-case | tee $@

.PHONY:;

