### Cài đặt môi trường cần thiết 
```
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get install -y python3-pip 
sudo apt-get install -y python3.5-dev libmysqlclient-dev  memcached libffi-dev libssl-dev
sudo apt-get install -y git nginx redis-server
```
### Cấu hình MySQL server
- cài đặt `sudo apt-get install -y mysql-server` (điền mật khẩu cho tài khoản root)
- đăng nhập vào mysql: `mysql -u root -p` (nhập mật khẩu đã tạo lúc dài đặt)
- tạo database: `CREATE DATABASE kvm_vdi CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
- tạo tài khoản: `CREATE USER 'portal'@'%' IDENTIFIED BY '123456';`
- phân quyền: `GRANT ALL PRIVILEGES ON kvm_vdi . * TO 'portal'@'%';`
- cập nhật: `FLUSH PRIVILEGES;`
- thoát: `exit;`
- thay 127.0.0.1 bằng IP của SQL server vào file `sudo vim /etc/mysql/mysql.conf.d/mysqld.cnf`
- restart `sudo /etc/init.d/mysql restart`

### Tải source code và cài các gói cần thiết để chạy code 
```
git clone https://github.com/vuvandang1995/Portal.git
cd Portal/kvmvdi
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
sudo pip3 install -r requirements.txt
sudo pip3 uninstall redis
sudo pip3 install redis==2.10.6
python3 manage.py migrate
```

### Lưu ý:
- khi chỉnh sửa cụm OPS, nhớ sửa cả tên rule ở hàm `add_user_to_project` trong `keystoneclient.py`
- sửa địa chỉ IP ở `instances.html` dòng 41
- đổi địa chỉ IP ở `show_instances.html`
- Sửa network ở `client/view.py` dòng 200
- Thay đổi `type_disk` ở modal tạo máy ảo ở `instances.html` dòng 184
## lưu ý python
- Khi đinh nghĩa 1 hàm, biến truyền vào là None, có nghĩa là khi gọi tới hàm, không truyền biến đó thì mặc định nó là None
- Các biến khởi tạo bằng None phải năm cuối
- Ví dụ:
```
def createVM(self, svname, flavor, image, network_id, max_count, key_name=None, admin_pass=None):
        self.nova.servers.create(svname, flavor=flavor, image=image, nics = [{'net-id':network_id}], key_name=key_name, admin_pass=admin_pass, max_count=max_count)
```

### gunicorn
`sudo vim /etc/systemd/system/gunicorn.service`
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/portal/Portal/kvmvdi
ExecStart=/usr/local/bin/gunicorn -c gunicorn_conf.py kvmvdi.wsgi:application --reload

[Install]
WantedBy=multi-user.target
```
#### https config
```
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/interuser/Portal/kvmvdi
ExecStart=/usr/local/bin/gunicorn -c gunicorn_conf.py --keyfile /etc/ssl/private/intercom.vn.PRIVATE.key --certfile /etc/ssl/certs/intercom.CERT.crt kvmvdi.wsgi:application --reload

[Install]
WantedBy=multi-user.target                         
```
### daphne
`sudo vim /etc/systemd/system/daphne.service`
```
[Unit]
Description=My Daphne Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/portal/Portal/kvmvdi
ExecStart=/usr/local/bin/daphne -b 0.0.0.0 -p 8001 kvmvdi.asgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
#### https
```
[Unit]
Description=My Daphne Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/interuser/Portal/kvmvdi
ExecStart=/usr/local/bin/daphne -e ssl:8443:privateKey=/etc/ssl/private/intercom.vn.PRIVATE.key:certKey=/etc/ssl/certs/intercom.CERT.crt kvmvdi.asgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
### nginx
`sudo vim /etc/nginx/sites-available/default`

```
server {
        listen 80 default_server;
        listen [::]:80 default_server;
        client_max_body_size 10M;
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
                root /home/portal/Portal/kvmvdi/superadmin;
        }

        location / {
                include proxy_params;
                proxy_pass http://0.0.0.0:8000;
        }
                location /ws/ {
                proxy_pass http://0.0.0.0:8001;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
        }
}
```
#### https
```
server {
        # SSL configuration
        listen 443 ssl default_server;
        listen [::]:443 ssl default_server;
	server_name portal.intercom.vn;
        ssl on;
        include snippets/self-signed.conf;
        include snippets/ssl-params.conf;

        location = /favicon.ico { access_log off; log_not_found off; }
	location /static/ {
                root /home/interuser/Portal/kvmvdi/superadmin;
        }

        location / {
                include proxy_params;
                proxy_pass https://0.0.0.0:8000;
        }

        location /wss/ {
                proxy_pass https://0.0.0.0:8443;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
        }
}

server {
        listen 80 default_server;
        listen [::]:80 default_server;
	return 301 https://$host$request_uri;
}
```

### restart serices
```
systemctl restart gunicorn.service
systemctl restart daphne.service 
systemctl restart redis-server.service
systemctl restart nginx.service

systemctl enable gunicorn.service
systemctl enable daphne.service 
systemctl enable redis-server.service
```

`python3 manage.py rqworker default`
