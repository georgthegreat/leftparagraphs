NAME := leftparagraphs
DHPARAM = /etc/nginx/conf/leftparagraphs.com/dh_param.pem

configs-install: configs/nginx.conf configs/uwsgi.conf
	#installing directory for logs
	install --mode=755 --owner=www-data --group=www-data --directory /var/log/uwsgi/app
	#configuring uwsgi
	install --owner=www-data --group=www-data configs/uwsgi.conf /etc/uwsgi/apps-available/$(NAME).conf
	ln -sf /etc/uwsgi/apps-available/$(NAME).conf /etc/uwsgi/apps-enabled/$(NAME).conf
	install --mode=644 configs/$(NAME).service /etc/systemd/system
	$(shell systemctl daemon-reload && systemctl enable $(NAME).service && systemctl stop $(NAME).service; systemctl start $(NAME).service || true)
	#configuring nginx
	if [ ! -f "$(DHPARAM)" ]; \
	then \
		echo "Generating custom dh_param at /tmp/dh_param.pem"; \
		openssl dhparam -out "/tmp/dh_param.pem" 2048; \
		install --mode=700 --owner=www-data --group=www-data --directory "$(dir $(DHPARAM))"; \
		install --mode=600 --owner=www-data --group=www-data "/tmp/dh_param.pem" "$(DHPARAM)"; \
		rm /tmp/dh_param.pem; \
	fi
	install --owner=www-data --group=www-data configs/nginx.conf /etc/nginx/sites-available/$(NAME).conf
	ln -sf /etc/nginx/sites-available/$(NAME).conf /etc/nginx/sites-enabled/$(NAME).conf
	service nginx reload


reload:
	touch /var/run/uwsgi/leftparagraphs.reload


requirements.txt:
	pip list --local --format=freeze | sort --ignore-case | tee $@

.PHONY: requirements.txt
