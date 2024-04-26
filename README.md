<div align="center">
  <h1>Mossy</h1>
  Yet another interplanetary microblogging platform with python ❤
</div>


# What is Mossy
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmattholy%2Fmossy.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmattholy%2Fmossy?ref=badge_shield)


Mossy is a interplanetary microblogging platform of fediverse, just like [Mastodon](https://github.com/mastodon/mastodon) or [Misskey](https://github.com/misskey-dev/misskey).

## Why Mossy

Mossy is here to deliver an exceptional experience with cutting-edge technology.
According to that, Mossy can do much better to protect your information & personal identity
(**We don't even need your Email**).

We lovingly provide:

- **Accesse your Mossy from nearest point**: Place your server anywhere and everywhere all over the world, they share the same data
- **High performance**: Even a small server can handel a large number of requests from fediverse
- **Flexible cluster**: Join a new node into your cluster at your will
- **Compatible with Mastodon's APIs**: So any application developed for Mastodon can generally be used with Mossy as well
- **Cluster of clusters**: Each Mossy Cluster can communicate with other Mossy Clusters, using algorithms to eliminate spam

# Getting Start

**Suport Docker Compose or Kubernetes**

A typical deployment involves placing your Mossy web services behind a load balancer. You can deploy Mossy nodes worldwide, connecting them via a shared PostgreSQL database and Garnet. By configuring your load balancer carefully, users can access your Mossy through the nearest access point.

Communication between Mossy and end users is secured with HTTPS. However, connections from Mossy to databases or Redis may be unsafe without protective measures like SSL or VPN.

After considering above, use the `docker-compose.yml` to deploy a single production-ready server:

```yml
waiting
```

## Environment

**Do make sure every Mossy node has the same `WEBAUTHN_RP_ID` and `WEBAUTHN_RP_ID`**

If you have clusters for databases and Redis, you can probably use different database and Redis URLs for every node. Otherwise make them the same.

| Name               | Instruction                                                                                                                                                                                                                                  | Default value                                                                                                     |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| DATABASE_URL       | A database string                                                                                                                                                                                                                            | `postgresql://username:password@localhost:5432/dbname`                                                            |
| REDIS_URL          | A URL for Redis                                                                                                                                                                                                                              | `redis://:password@localhost:6379/0`                                                                              |
| WEBAUTHN_RP_SOURCE | RP Source of Webauthn API and also for ActivityPUB Identifier                                                                                                                                                                                | `http://localhost:5173`                                                                                           |
| WEBAUTHN_RP_ID     | RP of Webauthn API                                                                                                                                                                                                                           | `localhost`                                                                                                       |
| LOG_LEVEL          | logger level                                                                                                                                                                                                                                 | `info`                                                                                                            |
| SERVICE_MODE       | Determine the service the container runs: `web` for web services and APIs, `backgrounder` for background tasks outside the request-response cycle, `scheduler` for rapid, periodic tasks, and `all` for running everything in one container. | `all`                                                                                                             |
| WORKERS            | Number of Uvicorn and Celery workers, `2` means 2 Uvicorn workers and 2 Celery workers etc.                                                                                                                                                  | Half numbers of CPU cores plus 1. For example, you have a 8 cores CPU, then the default value of this will be `5` |

# Everything Else

## How Mossy Works

## Dev & Tests

Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

Before start, you need to install:

| Name   | Version |
| ------ | ------- |
| python | 3.12    |
| poetry | 1.8.2   |
| node   | 21.7.3  |
| npm    | 10.5.0  |

Everything else will be managed by `poetry` or `npm`

### Install dependences

- Install frontend dependence: `npm run install:frontend`
- Install backend dependence: `npm run install:backend`
- Install everything: `npm run install`

### Run your development server

- Run frontend development server: `npm run dev:frontend`
- Run backend development server: `npm run dev:backend`
- Pack it up and start a production like server: `npm run dev`
- Prepare a database for development only: `docker compose up -d`, to clean them up `docker compose down`

#### When you changed database schemas

Before you commit you change to remote.
Change your current working dir to backend (`cd backend`) and run `poetry run alembic revision --autogenerate -m "[write your changes here]"`, then run `poetry run alembic upgrade head` to update database.

The production image will update database automatically.

### Tests

#### Unit test

- Test frontend: `npm run test:frontend`
- Test backend: `npm run test:backend`
- Test everything: `npm run test`

#### Test locally

Run `docker compose --profile dev up --build`,then navigate to [http://localhost:8000](http://localhost:8000)

----

<div align="center">
  <img src="./docs/fedi.png" alt="Fediverse Logo" width="300"/>
</div>


## License
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fmattholy%2Fmossy.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fmattholy%2Fmossy?ref=badge_large)