#!/bin/bash
set -e

apt-get update -y
apt-get install -y python3-dev build-essential python3.12-venv

cd /home/ubuntu/backend
python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

# Create empty database file with correct permissions
touch /home/ubuntu/backend/cloudproof.db
chown ubuntu:ubuntu /home/ubuntu/backend/cloudproof.db
chmod 664 /home/ubuntu/backend/cloudproof.db

# Ensure backend directory is owned by ubuntu
chown -R ubuntu:ubuntu /home/ubuntu/backend

# Safe .env copy
if [ ! -f /home/ubuntu/backend/.env ]; then
    if [ -f /home/ubuntu/backend/.env.example ]; then
        cp /home/ubuntu/backend/.env.example /home/ubuntu/backend/.env
    fi
fi

# Nginx config
cat > /etc/nginx/sites-available/cloudproof <<EOF
server {
    server_name handsoncloud.in;

    location / {
        root /var/www/html;
        index index.html;
        try_files \$uri \$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-Proto \$scheme;

        if (\$request_method = OPTIONS) {
            add_header Access-Control-Allow-Origin \$http_origin;
            add_header Access-Control-Allow-Methods 'GET, POST, PUT, DELETE, OPTIONS';
            add_header Access-Control-Allow-Headers 'Content-Type, Authorization';
            add_header Access-Control-Allow-Credentials 'true';
            return 204;
        }
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/handsoncloud.in/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/handsoncloud.in/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if (\$host = handsoncloud.in) {
        return 301 https://\$host\$request_uri;
    }
    listen 80;
    server_name handsoncloud.in;
    return 404;
}
EOF

ln -sf /etc/nginx/sites-available/cloudproof /etc/nginx/sites-enabled/cloudproof
rm -f /etc/nginx/sites-enabled/default

# systemd service
cat > /etc/systemd/system/cloudproof.service <<EOF
[Unit]
Description=CloudProof Flask Backend
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/backend
ExecStart=/home/ubuntu/backend/venv/bin/python /home/ubuntu/backend/app.py
Restart=always
RestartSec=5
EnvironmentFile=/home/ubuntu/backend/.env

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cloudproof
systemctl restart cloudproof || systemctl start cloudproof
systemctl restart nginx