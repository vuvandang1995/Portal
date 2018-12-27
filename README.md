# Portal
## Lưu ý:
- Trong file config của nginx, có đoạn cấu hình:
```
location /ws/ {
                proxy_pass https://web:8443;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
        }
```
- Nghĩa là đoạn bên trên cấu hình cho cả http và https, chứ không phải là dúng `location /wss/` đâu nhé.
