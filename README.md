# Kubernetes Mobile API with Mutual TLS (mTLS)

This guide explains how to set up and run a Kubernetes mobile API with mutual TLS (mTLS) authentication using Nginx and Docker.

## Build Docker Image

```sh
# Build the Docker image and tag it as "latest"
docker build -t fujikomalan/k8s-mobile-api-mtls:latest .
```

## Generate mTLS Certificates

```sh
# Create the necessary directories for storing CA, server, and client certificates
mkdir -p mtls-certs/{ca,server,client}

# Generate a private key for the Certificate Authority (CA)
openssl genrsa -out mtls-certs/ca/ca.key 2048

# Create a self-signed CA certificate
openssl req -x509 -new -nodes -key mtls-certs/ca/ca.key -sha256 -days 365 -out mtls-certs/ca/ca.crt \
  -subj "/CN=MyCustomCA"

# Generate a private key for the server
openssl genrsa -out mtls-certs/server/server.key 2048

# Create a Certificate Signing Request (CSR) for the server
openssl req -new -key mtls-certs/server/server.key -out mtls-certs/server/server.csr \
  -subj "/CN=mynginx.local"

# Generate the server certificate signed by the CA
openssl x509 -req -in mtls-certs/server/server.csr -CA mtls-certs/ca/ca.crt -CAkey mtls-certs/ca/ca.key -CAcreateserial \
  -out mtls-certs/server/server.crt -days 365 -sha256

# Generate a private key for the client
openssl genrsa -out mtls-certs/client/client.key 2048

# Create a Certificate Signing Request (CSR) for the client
openssl req -new -key mtls-certs/client/client.key -out mtls-certs/client/client.csr \
  -subj "/CN=client"

# Generate the client certificate signed by the CA
openssl x509 -req -in mtls-certs/client/client.csr -CA mtls-certs/ca/ca.crt -CAkey mtls-certs/ca/ca.key -CAcreateserial \
  -out mtls-certs/client/client.crt -days 365 -sha256
```

## Run the Docker Container

```sh
# Run the Docker container with the generated server certificates mounted
# Expose ports 80 and 443 for HTTP and HTTPS traffic

docker container run \
    -it \
    -d \
    --name python \
    -v $(pwd)/mtls-certs/server/:/etc/nginx/ssl/ \
    -p 80:80 \
    -p 443:443 \
    fujikomalan/k8s-mobile-api-mtls:latest
```

## Test the API with Curl

### Request without Client Certificate (Fails)

```sh
# This request will fail with a 400 error because the client certificate is missing
curl https://mynginx.local/phones --cacert mtls-certs/ca/ca.crt --resolve mynginx.local:443:172.31.6.74
```

#### Expected Output:
```html
<html>
<head><title>400 No required SSL certificate was sent</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<center>No required SSL certificate was sent</center>
<hr><center>nginx</center>
</body>
</html>
```

### Request with Client Certificate (Succeeds)

```sh
# This request includes the client certificate and should succeed
curl https://mynginx.local/phones --cacert mtls-certs/ca/ca.crt \
  --key mtls-certs/client/client.key --cert mtls-certs/client/client.crt \
  --resolve mynginx.local:443:172.31.6.74
```

This setup ensures secure communication between the client and server using mutual TLS authentication.

