# e-Parts

### Setup Database
```bash
docker run --name eparts-db -p 5432:5432 -e POSTGRES_PASSWORD=secret -d postgres
````

```bash
docker exec -ti eparts-db createdb -U postgres eparts
```