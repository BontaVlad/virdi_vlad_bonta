# Virdi code assigment

Create an application where the user can enter the state of their assets portfolio on a particular day in the past and see how much money would it be worth today.
The only class of assets we’re considering here are stocks and/or mutual funds.

## Deploy locally

```bash
docker build -t docker-fastapi .
docker run -e MARKETSTACK_API_KEY=secret-key -d -p 80:80 docker-fastapi
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
