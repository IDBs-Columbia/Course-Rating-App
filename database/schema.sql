CREATE TABLE Thread (
    thread_id int PRIMARY KEY,
    thread_title text,
    thread_description,
    thread_date datetime    
);

CREATE TABLE Course(
    course_id int PRIMARY KEY,
    course_name text,
    course_section text,
    course_description text,
    course_instructor text,
);

CREATE TABLE Course_Institution(
    course_id int PRIMARY KEY, 
    institution_id int NOT NULL,
    FOREIGN KEY (institution_id) REFERENCES Institution
        ON DELETE NO ACTION    
);

CREATE TABLE Institution(
    institution_id int PRIMARY KEY,
    institution_name text NOT NULL
);

CREATE TABLE Commment(
    comment_id int NOT NULL,
    comment_content text,
    comment_num_likes int,
    comment_num_dislikes int,
    comment_date datetime,

    -- USER ATTRIBUTES
    user_email text NOT NULL,

    -- THREAD ATTRIBUTES
    thread_id int NOT NULL,

    -- KEY CONSTRAINTS
    PRIMARY KEY(comment_id),
    FOREIGN KEY (user_email) REFERENCES RegularUser(email)
        ON DELETE CASCADE,
    FOREIGN KEY (thread_id) REFERENCES Thread
        ON DELETE CASCADE
);

CREATE TABLE Comment_reply(
    comment_parent_id int,
    comment_child_id int, 
    PRIMARY KEY(comment_parent_id, comment_child_id)
)

CREATE TABLE Report(
    report_id int PRIMARY KEY,
    report_description text,
    report_category text
);

CREATE TABLE User_Report(
    report_id int,

    -- USER ATTRIBUTES
    user_email text,

    -- COMMENT ATTRIBUTES
    comment_id int,

    -- THREAD ATTRIBUTES
    thread_id int,

    -- KEY CONSTRAINTS
    PRIMARY KEY (user_email, report_id),
    CHECK (comment_id IS NOT NULL OR thread_id IS NOT NULL) AND
            (comment_id IS NULL OR thread_id IS NULL)

)
