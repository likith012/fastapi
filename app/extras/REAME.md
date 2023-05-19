**Gunicorn**

To automatically enable the systemd service for your Gunicorn application, you can use the `systemctl enable` command. Here's how you can enable your Gunicorn systemd service:

1. Save the systemd file you provided to the `/etc/systemd/system` directory with a `.service` file extension, for example, `/etc/systemd/system/gunicorn.service`.

2. Reload the systemd daemon to pick up the new service file:

   ```
   sudo systemctl daemon-reload
   ```

3. Enable the systemd service to start automatically on boot:

   ```
   sudo systemctl enable gunicorn.service
   ```

4. Start the systemd service:

   ```
   sudo systemctl start gunicorn.service
   ```

Now your Gunicorn systemd service should be running and enabled to start automatically on boot. You can check the status of the service using the `systemctl status gunicorn.service` command.
