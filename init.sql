CREATE TABLE IF NOT EXISTS vish_posts_text (
        id SERIAL PRIMARY KEY,
        title VARCHAR
);

CREATE TABLE IF NOT EXISTS vish_posts_stat (
    id SERIAL PRIMARY KEY,
    date TIMESTAMP,
    comments_count SMALLINT,
    likes_count SMALLINT,
    reposts_count SMALLINT,
    views_count SMALLINT,
    post_type VARCHAR
);