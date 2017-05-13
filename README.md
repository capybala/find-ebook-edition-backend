# find-ebook-edition-backend

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

Backend server of [find-ebook-edition](https://github.com/capybala/find-ebook-edition).


## Requirements

- Python 3.6
- Memcached
- Foreman


## 1. Install packages

```
$ python3 -m venv venv
$ . venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ pip install -r dev-requirements.txt
```


## 2. Set up env vars

Put `.env`

```
MEMCACHIER_SERVERS=127.0.0.1
AMAZON_ACCESS_KEY=(Your access key)
AMAZON_SECRET_KEY=(Your secret key)
AMAZON_ASSOCIATE_TAG=(Your associate tag)
```


## 3. Start server

```
$ foreman start
```


## 4. Run tests

```
$ memcached
```

```
$ foreman run nosetests
```


## 5. Configure Heroku

1. Create an app
2. Add MemCachier add-on
3. Configure env vars


## 6. Deploy to Heroku

```
$ git push heroku master
```
