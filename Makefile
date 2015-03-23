NAME := leftparagraphs

www-configs-install: configs/nginx.conf configs/uwsgi.conf
	#configuring uwsgi
	cp configs/uwsgi.conf /etc/uwsgi/apps-available/$(NAME).conf
	ln -sf /etc/uwsgi/apps-available/$(NAME).conf /etc/uwsgi/apps-enabled/$(NAME).conf
	#creating upstart job
	cp configs/service.conf /etc/init/$(NAME).conf
	stop $(NAME); start $(NAME)
	#configuring nginx
	cp configs/nginx.conf /etc/nginx/sites-available/$(NAME).conf
	ln -sf /etc/nginx/sites-available/$(NAME).conf /etc/nginx/sites-enabled/$(NAME).conf
	service nginx reload


requirements.txt: .PHONY
	pip freeze --local | sort --ignore-case | tee $@

.PHONY:;

