{% macro generate_film_ratings() %}

WITH films_with_ratings AS (
    {{ generate_films_with_ratings() }}
),

films_with_actors AS (
    SELECT
        films.film_id,
        films.title,
        STRING_AGG(actors.actor_name, ', ') AS actors  -- Aggregating actor names for each film
    FROM {{ ref('films') }} films
    LEFT JOIN {{ ref('film_actors') }} film_actors ON films.film_id = film_actors.film_id
    LEFT JOIN {{ ref('actors') }} actors ON film_actors.actor_id = actors.actor_id
    GROUP BY films.film_id, films.title
)

SELECT
    films_with_ratings.*,
    films_with_actors.actors
FROM films_with_ratings
LEFT JOIN films_with_actors ON films_with_ratings.film_id = films_with_actors.film_id

{% endmacro %}
