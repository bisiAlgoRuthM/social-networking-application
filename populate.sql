INSERT INTO user_profile (username, email, first_name, last_name)
VALUES ('john_doe', 'john.doe@example.com', 'John', 'Doe'),
       ('jane_smith', 'jane.smith@example.com', 'Jane', 'Smith'),
       ('code_wizard', 'coder.wizard@example.net', 'Alex', 'Jones'),
       ('book_lover', 'βιβλιόφιλος@example.gr', 'Elena', 'Papadakis'),  -- Assuming 'βιβλιόφιλος' is stored correctly
       ('travel_enthusiast', 'travelholic@example.com', 'Michael', 'Thompson');


INSERT INTO user_posts (user_profile_id, title, body, created_at)
VALUES (1, 'Welcome to my social network profile!', "I'm excited to connect with people who share similar interests. #socialnetworking #welcome", current_timestamp),
       (2, 'Just finished reading a great book!', 'Anyone else a fan of science fiction? #scifi #books', current_timestamp),
       (3, 'Check out this amazing travel destination!', "I'm currently exploring [insert location] and it\'s breathtaking! #travel #adventure", current_timestamp);


INSERT INTO user_comments (user_profile_id, post_id, comment, created_at)
VALUES (2, 1, 'This looks like a great platform!  Welcome!', current_timestamp),
       (1, 2, 'I love sci-fi too! What was the book you were reading?', current_timestamp),
       (4, 3, 'Wow, those pictures are incredible! Where exactly is that?', current_timestamp);
