## Docker Commands

```
1. Build dockerfile without using the cache

docker-compose build --no-cache elt_script

2. Start multi-containers (using compose)

docker-compose up

3. Run Destination Container in interactive session in scripts folder

docker exec -it elt-project-tutorial-destination_postgres-1 psql -U postgres

4. Stop multi-containers (using compose)

docker-compose down
```

## PSQL Commands

```
1. List tables:
\dt

2. Describe Table structure:
\d your_table_name
```


