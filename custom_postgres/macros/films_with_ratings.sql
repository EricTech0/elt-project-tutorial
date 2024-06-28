{% macro generate_films_with_ratings() %}

SELECT
    film_id,
    title,
    release_date,
    price,
    rating,
    user_rating,
    {{ classify_ratings('user_rating') }} AS rating_category
FROM {{ ref('films') }}  -- Using dbt's ref function to reference the films table

{% endmacro %}
