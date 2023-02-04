# TeslaControl

This is a simple web-service which wraps the OpenChargingPort command to a simple API with basic auth which can be
called from other devices like ESP32. The SSO login and token refresh will be done by this web-service.

With this separation the web-service can run in a safe environment and store the Tesla API token, while a third device (
ESP) may be placed in a public area like a garage. In case the ESP will be stolen the API token is not lost.

### Docker setup
## Generate API Token

To generate an authentication token use the following command. Make sure to set up a volume where the token should be saved.
```
docker run -it -v teslacontrol-vol:/config ghcr.io/soerenbusse/teslacontrol:master python3 /code/app/login.py --email mail@example.com --token-file-path /config/token.json
```

Afterwards the container can be run via docker-compose.

### Manual setup
```
apt-get install python3-venv git
git clone https://github.com/SoerenBusse/TeslaControl /opt/teslacontrol

# Create Python3 virtual environment
python3 -m venv /opt/teslacontrol/venv
/opt/teslacontrol/venv/bin/pip install -r requirements.txt

# Create .env file and add environment variables (see environment variables from docker-compose)
touch /opt/teslacontrol/.env

# Create user
useradd -m teslacontrol
groupadd teslacontrol
usermod -a -G teslacontrol teslacontrol

# Create systemd service
nano /etc/systemd/system/teslacontrol.service
--
[Unit]
Description=TeslaControl service
After=network.target

[Service]
Type=simple
User=teslacontrol
Group=teslacontrol
WorkDirectory=/opt/teslacontrol
ExecStart=/opt/teslacontrol/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8080

[Install]
WantedBy=multi-user.target
--

# Generate Token as user
mkdir /srv/teslacontrol
chown teslacontrol:teslacontrol /srv/teslacontrol
chmod 700 /srv/teslacontrol
runuser -u teslacontrol -- /opt/teslacontrol/venv/bin/python3 /opt/teslacontrol/app/login.py --email mail@example.com --token-file-path /srv/teslacontrol/token.json

systemctl daemon-reload
systemctl enable teslacontrol
systemctl start teslacontrol
systemctl status teslacontrol
```

## API documentation
The webservice automatically generates a Swagger documentation at `https://your-url:8080/docs`