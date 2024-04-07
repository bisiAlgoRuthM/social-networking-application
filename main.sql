CREATE TABLE user_connection (
    id serial PRIMARY KEY,  -- Auto-incrementing integer
    follower_ID integer REFERENCES user_profile(id),
    following_ID integer REFERENCES user_profile(id),
    asatus varchar
);
--JUNCTION TABLE
CREATE TABLE user_profile_connection (
    id serial  PRIMARY KEY,
    user_profile_ID integer NOT NULL REFERENCES user_profile(id) ON DELETE CASCADE,
    connection_id  integer NOT NULL REFERENCES user_connection(id)
);

CREATE TABLE user_posts (
    id serial PRIMARY KEY,
    user_profile_id integer REFERENCES user_profile(id),
    title varchar,
    body text,
    created_at timestamp,
    attachment_id integer REFERENCES attachment(id) DEFAULT NULL
);

CREATE TABLE attachment (
    id serial PRIMARY KEY,
    filename varchar(225),
    content_type varchar(255),
    size integer,
    attachment_content_url varchar(225) -- Store URL or path to attachment content (if applicable)
);

-- JUNCTION TABLE
CREATE TABLE attachment_post (
    id serial PRIMARY KEY,
    attachment_id integer REFERENCES attachment(id),
    post_id integer REFERENCES user_posts(id)
);

CREATE TABLE user_engagement (
    id serial PRIMARY KEY,
    post_id integer REFERENCES user_posts(id),
    user_id integer REFERENCES user_profile(id),  -- Foreign key to user who interacted
    views integer,
    comments integer,
    likes integer,
    shares integer
);

CREATE TABLE user_comments (
    id serial PRIMARY KEY,
    post_id integer REFERENCES user_posts(id),
    user_id integer REFERENCES user_profile(id),  -- Foreign key to user who commented
    comment text,
    timestamp datetime
);

CREATE TABLE private_message (
    id serial PRIMARY KEY,
    thread_id integer REFERENCES message_thread(id),
    sender_id integer REFERENCES user_profile(id),  -- Foreign key to sender
    receiver_id integer REFERENCES user_profile(id),  -- Foreign key to receiver
    content text,
    timestamp datetime,
    status enum ("sent", "delivered", "read")
);

CREATE TABLE message_thread (
    id serial PRIMARY KEY,
    participant1 integer references user_profile(id),
    participant2 integer references user_profile(id)
);

--JUNCTION TABLE 
CREATE TABLE message_participants (
    id serial PRIMARY KEY,
    participant_id integer REFERENCES user_profile(id),
    message_thread_id integer REFERENCES message_thread(id),
    user_profile_id integer REFERENCES user_profile(id)
); 
