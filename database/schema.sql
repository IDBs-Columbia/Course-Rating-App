-- NAMING CONVENTION:
-- Entity Set Tables: Player                                                [Snake Case]
-- Attributes: attribute name (e.g., name)                                  [Lower Case]
-- Relationship Set tables: Entity1 name + relationship  + Entity2 name     [Lower Case for Relationship Name]     
--     (e.g., Player_eats_Ghosts)

CREATE TABLE User(
    -- Base Table for Users
    -- Contains a user's basic information
    -- irrespective of its type

    `email` text PRIMARY KEY,
    `name` text NOT NULL, 
    `password` text NOT NULL
);

CREATE TABLE User_Regular(
    `id` int PRIMARY KEY,
    `status` text NOT NULL,
    `strikes` int NOT NULL DEFAULT 0,

    -- User base table attributes
    `email`text NOT NULL UNIQUE,

    -- Key constraints
    FOREIGN KEY (`email`)
        REFERENCES User
        ON DELETE CASCADE
);

CREATE TABLE User_Admin(
    `id` int PRIMARY KEY,
    `can_manage_report` boolean NOT NULL,
    `can_manage_course` boolean NOT NULL,
    `can_manage_comment` boolean NOT NULL,
    `can_manage_user` boolean NOT NULL,

    -- User base table attributes
    `email`text NOT NULL UNIQUE,

    -- Key constraints
    FOREIGN KEY (`email`) 
        REFERENCES User
        ON DELETE CASCADE
);

CREATE TABLE Course(
    `call_number` int PRIMARY KEY,
    `course_number` text NOT NULL,
    `name` text NOT NULL,
    `description` text,
    `instructor` text NOT NULL,

    -- Institution table attributes
    `institution_id` int,

    -- Key constraints
    FOREIGN KEY (`institution_id`)
        REFERENCES Institution (`id`)
);

CREATE TABLE Institution(
    `id` int PRIMARY KEY,
    `name` text NOT NULL
);

CREATE TABLE Thread(
    `id` int PRIMARY KEY,
    `title` text NOT NULL,
    `description` text,
    `date` datetime NOT NULL
);

CREATE TABLE Comment(
    `id` int PRIMARY KEY,
    `content` text NOT NULL,
    `likes` int NOT NULL DEFAULT 0,
    `dislikes` int NOT NULL DEFAULT 0,
    `date` datetime NOT NULL,

    -- Comment reply Attribute
    `reply_id` int DEFAULT NULL,    -- This attribute is only set
                                    -- if replying to another comment

    -- Regular User attributes
    `user_id` int NOT NULL,

    -- Thread attributes
    `thread_id` int NOT NULL,

    -- Key constraints
    FOREIGN KEY (`user_id`) 
        REFERENCES User_Regular    
        ON DELETE CASCADE,       
    FOREIGN KEY (`thread_id`)
        REFERENCES Thread
        ON DELETE CASCADE,
    FOREIGN KEY (`reply_id`)
        REFERENCES Comment
        ON DELETE CASCADE
);

CREATE TABLE Report(
    `id` int PRIMARY KEY,
    `category` text NOT NULL,
    `description` text,
    `date` datetime NOT NULL,

    -- Regular User attributes
    `user_id` int NOT NULL,

    -- Comment attributes
    `comment_id` int, 

    -- Thread attributes
    `thread_id` int,

    -- Key constraintS
    FOREIGN KEY (`user_id`)
        REFERENCES User_Regular (`id`),
        ON DELETE NO ACTION,
    FOREIGN KEY (`comment_id`)
        REFERENCES Comment (`id`)
        ON DELETE CASCADE,
    FOREIGN KEY (`thread_id`)
        REFERENCES Thread (`id`)
        ON DELETE CASCADE

    -- Specialization constraints
    CHECK 
        (
            `comment_id` IS NOT NULL 
            OR
            `thread_id` IS NOT NULL
        ) 
        AND
        (
            `comment_id` IS NULL 
            OR
            `thread_id` IS NULL
        )
);

CREATE TABLE User_Regular_rate_Course(
    `course_satisfaction` int NOT NULL,
    `difficulty` int NOT NULL,
    `workload` int NOT NULL,
    `description` text,
    
    -- Regular User attributes
    `user_id` int NOT NULL,

    -- Course attributes
    `call_number` int NOT NULL,

    -- Key constraints
    PRIMARY KEY(`user_id`, `call_number`)
);

CREATE TABLE User_Regular_creates_Thread(
    -- Thread attributes
    `thread_id` int PRIMARY KEY,

    -- Regular User attributes
    `user_id` int NOT NULL,

    -- Key constraints
    FOREIGN KEY (`user_id`)
        REFERENCES User_Regular(`id`)
        ON DELETE NO ACTION
);

CREATE TABLE User_Regular_rates_Thread(
    `is_helpful` boolean,

    -- Regular User attributes
    `user_id` int NOT NULL,

    -- Thread attributes
    `thread_id` int NOT NULL,

    -- Key constraints
    PRIMARY KEY (`user_id`, `thread_id`)
);

CREATE TABLE User_Regular_rates_Comment(
    `is_helpful` boolean,

    -- Regular User attributes
    `user_id` int NOT NULL,

    -- Comment attributes
    `comment_id` int NOT NULL,

    -- Key constraints
    PRIMARY KEY (`user_id`, `comment_id`)
);