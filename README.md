# krisha-kz
parsed krisha-kz

# запуск
- заполнить `.env` и `parser/app/.env`
- заполнить `proxies.txt`
- запустить сервер 
```sh 
scrapyd
```
- проинициализировать параметрами деплоя из `scrapy.cfg`
```sh
scrapyd-deploy
```
- отправить задание на 0-ый инстанс из 5-и
```sh
scrapyd-client schedule -p default --arg part=0 --arg total=5 flat_spider
