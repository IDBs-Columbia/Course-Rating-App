CREATE TABLE Thread (
    thread_id int PRIMARY KEY AUTO_INCREMENT,
    thread_title varchar(255) NOT NULL,
    thread_description longtext NOT NULL,
    thread_date datetime DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Course(
  course_call_number varchar(5) PRIMARY KEY,
  course_course_number varchar(10) NOT NULL,
  course_name varchar(64) NOT NULL,
  course_description longtext,
  course_instructor varchar(100) NOT NULL,
  course_institution_id int DEFAULT NULL,
  FOREIGN KEY (course_institution_id) REFERENCES Institution (institution_id)
);

CREATE TABLE Institution(
    institution_id int PRIMARY KEY AUTO_INCREMENT,
    institution_name varchar(64) NOT NULL
);

CREATE TABLE Commment(
    comment_id int NOT NULL PRIMARY KEY,
    comment_content longtext NOT NULL,
    comment_num_likes int NOT NULL DEFAULT 0,
    comment_num_dislikes int NOT NULL DEFAULT 0,
    comment_date datetime DEFAULT CURRENT_TIMESTAMP,

    -- USER ATTRIBUTES
    user_email text NOT NULL,

    -- THREAD ATTRIBUTES
    thread_id int NOT NULL,

    -- KEY CONSTRAINTS
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
    report_id int PRIMARY KEY AUTO_INCREMENT,
    report_description varchar(255),
    report_category enum(
        'offensive language',
        'untruthful',
        'academic misconduct'
    )
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
