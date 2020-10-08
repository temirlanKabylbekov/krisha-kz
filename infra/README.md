# Создание прокси-серверов в aws
```sh

docker run -it -v $(pwd):/workpace -w /workpace hashicorp/terraform init && terraform apply -var "ip_address=$(curl ifconfig.io)" -auto-approve

```
