NAME := leftparagraphs

www-configs-install: configs/nginx.conf configs/uwsgi.conf
	cp configs/nginx.conf /etc/nginx/sites-available/$(NAME).conf
	ln -sf /etc/nginx/sites-available/$(NAME).conf /etc/nginx/sites-enabled/$(NAME).conf
	cp configs/uwsgi.conf /etc/uwsgi/apps-available/$(NAME).conf
	ln -sf /etc/uwsgi/apps-available/$(NAME).conf /etc/uwsgi/apps-enabled/$(NAME).conf
	cp configs/service.conf /etc/init.d/$(NAME)

	service nginx reload
	service $(NAME) restart

requirements.txt: .PHONY
    pip freeze --local | sort --ignore-case | tee $@

.PHONY:
	;

