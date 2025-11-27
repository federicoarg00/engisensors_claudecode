# 🚀 Deploying EngiSensors on Coolify

This guide provides step-by-step instructions for deploying the EngiSensors application to a Coolify server.

## Prerequisites

1.  **A running Coolify instance:** You should have a Coolify server up and running. If not, follow the official Coolify documentation to set one up.
2.  **GitHub Repository:** Your EngiSensors project code should be in a GitHub repository.
3.  **Domain/Subdomain:** A domain or subdomain ready to be pointed to the Coolify server for the EngiSensors application.

## Deployment Steps

### 1. Create a New Application in Coolify

1.  From your Coolify dashboard, navigate to the "Applications" section.
2.  Click on "Create a new Application".
3.  Select "Git Repository" as the source.
4.  Choose your GitHub repository where the EngiSensors code is hosted.
5.  Select the branch you want to deploy (e.g., `main`).

### 2. Configure Build Settings

Coolify will automatically detect the `Dockerfile` in the `/src/backend` directory. However, you need to specify the correct base directory.

1.  **Build Pack:** Select `Dockerfile`.
2.  **Base Directory:** Set this to `/src/backend`. This is crucial because the `Dockerfile` is located in a subdirectory.
3.  **Install Command:** This can be left blank as the `Dockerfile` handles the installation.
4.  **Start Command:** This can also be left blank as the `Dockerfile`'s `CMD` will be used.

### 3. Configure Network Settings

1.  **Port:** The application runs on port `8000`. Configure Coolify to expose this port. The default settings are usually fine, as Coolify will map a public port to the container's port `8000`.
2.  **Domain:** Enter the domain or subdomain you want to use for the application (e.g., `engisensors.yourdomain.com`).

### 4. Add Environment Variables

This is a critical step. The application relies on several environment variables to run correctly.

1.  Go to the "Environment Variables" section of your application in Coolify.
2.  Add the following variables:

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `ENVIRONMENT` | The application environment. | `production` |
| `DEBUG` | Set to `False` for production. | `False` |
| `LOG_LEVEL` | Logging level. | `INFO` |
| `SECRET_KEY` | A strong, unique secret key. | `generate_a_random_secret_key` |
| `DATABASE_URL` | The connection string for your database. | `postgresql://user:pass@host:port/db` |
| `REDIS_URL` | The connection string for Redis. | `redis://host:port/0` |
| `MQTT_BROKER_HOST` | The MQTT broker hostname. | `your_mqtt_broker.com` |
| `MQTT_BROKER_PORT` | The MQTT broker port. | `1883` |
| `MQTT_BROKER_USERNAME`| The MQTT broker username (if any).| `mqtt_user` |
| `MQTT_BROKER_PASSWORD`| The MQTT broker password (if any).| `mqtt_password` |
| `JWT_SECRET_KEY` | A strong, unique secret for JWTs. | `another_random_secret_key` |
| `SENDGRID_API_KEY` | Your SendGrid API key for email notifications. | `SG.xxxxxxxx` |
| `TWILIO_ACCOUNT_SID`| Your Twilio Account SID for SMS. | `ACxxxxxxxx` |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token. | `your_twilio_auth_token` |
| `TWILIO_PHONE_NUMBER`| Your Twilio phone number. | `+15017122661` |

**Note on `DATABASE_URL` and `REDIS_URL`:** You can either use existing PostgreSQL and Redis instances or set them up as new services within Coolify. If you set them up in Coolify, the connection strings will be provided for you.

### 5. Deploy the Application

1.  Once you have configured the build settings, network, and environment variables, click the "Deploy" button.
2.  Coolify will pull your code from GitHub, build the Docker image, and start the container.
3.  You can monitor the deployment process in the "Logs" section.

### 6. Post-Deployment Verification

1.  **Check the logs:** Ensure the application started without any errors.
2.  **Access the application:** Open your configured domain in a web browser.
3.  **Health Check:** Access the `/health` endpoint to verify the application is running: `http://engisensors.yourdomain.com/health`. You should see a JSON response indicating the status.
4.  **MQTT Health Check:** Access the `/health/mqtt` endpoint to verify the MQTT connection: `http://engisensors.yourdomain.com/health/mqtt`.

## Troubleshooting

*   **Build Failures:**
    *   Double-check that the "Base Directory" is set correctly to `/src/backend`.
    *   Ensure your `Dockerfile` is correct and has no syntax errors.

*   **Application Crashes:**
    *   Review the application logs in Coolify for error messages.
    *   Verify that all required environment variables are set and have the correct values.
    *   Ensure the database and Redis services are running and accessible from the application container.

*   **502 Bad Gateway:**
    *   This usually means the application is not running or not responding on the configured port (`8000`).
    *   Check the application logs for any startup errors.
