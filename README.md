# TeslaControl
This is a simple web-service which wraps the OpenChargingPort command to a simple API with basic auth which can be called from other devices like ESP32.
The SSO login and token refresh will be done by this web-service.

With this separation the web-service can run in a safe environment and store the Tesla API token, while a third device (ESP) may be placed in a public area like a garage. In case the ESP will be stolen the API token is not lost.