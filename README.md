```
docker build -t fujikomalan/k8s-mobile-api-mtls:latest .
```

```
$ mkdir -p mtls-certs/{ca,server,client}

$ openssl genrsa -out mtls-certs/ca/ca.key 2048
$ openssl req -x509 -new -nodes -key mtls-certs/ca/ca.key -sha256 -days 365 -out mtls-certs/ca/ca.crt \
  -subj "/CN=MyCustomCA"

$ openssl genrsa -out mtls-certs/server/server.key 2048
$ openssl req -new -key mtls-certs/erver/server.key -out mtls-certs/server/server.csr -subj "/CN=mynginx.local"
$ openssl x509 -req -in mtls-certs/server/server.csr -CA mtls-certs/ca/ca.crt -CAkey mtls-certs/ca/ca.key -CAcreateserial \
  -out mtls-certs/server/server.crt -days 365 -sha256


$ openssl genrsa -out mtls-certs/client/client.key 2048
$ openssl req -new -key mtls-certs/client/client.key -out mtls-certs/client/client.csr -subj "/CN=client"
$ openssl x509 -req -in mtls-certs/client/client.csr -CA mtls-certs/ca/ca.crt -CAkey mtls-certs/ca/ca.key -CAcreateserial \
  -out mtls-certs/client/client.crt -days 365 -sha256

```

```
$ docker container run  \
    -it \
    -d \
    --name python \
    -v $(pwd)/mtls-certs/server/:/etc/nginx/ssl/ \
    -p 80:80 \
    -p 443:443 \
    fujikomalan/k8s-mobile-api-mtls:latest
```

```
$ curl https://mynginx.local/phones --cacert mtls-certs/ca/ca.crt --resolve mynginx.local:443:172.31.6.74

<html>
<head><title>400 No required SSL certificate was sent</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<center>No required SSL certificate was sent</center>
<hr><center>nginx</center>
</body>
</html>
```

```
$ curl https://mynginx.local/phones --cacert mtls-certs/ca/ca.crt   --key mtls-certs/client/client.key --cert mtls-certs/client/client.crt  --resolve mynginx.local:443:172.31.6.74
```
