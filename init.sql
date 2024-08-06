CREATE TABLE IF NOT EXISTS vish_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR,
    date TIMESTAMP,
    comments_count SMALLINT,
    likes_count SMALLINT,
    reposts_count SMALLINT,
    views_count SMALLINT,
    post_type VARCHAR
);