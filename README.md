# events storage service

```
curl -v 127.0.0.1:5000/events -H Client-Key:424242 --data '{"title": "???? Node.js #4", "only_date": true, "level": "JUNIOR", "when_start": "2015-10-24", "agenda": "?????? ??? ?????????????? ???????? ????? Kiev NodeJS ????????? ?????", "special": false, "image_url": "https://pp.vk.me/c627320/v627320107/1c477/qnqnllYEPR8.jpg"}'
curl '127.0.0.1:5000/events?query=(when_start>="2015-10-31")and(when_start<="2015-11-01")' -H Client-Key:424242
```
