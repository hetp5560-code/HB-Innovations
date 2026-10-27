DROP TABLE IF EXISTS certificates;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS skills;
DROP TABLE IF EXISTS experience;
DROP TABLE IF EXISTS education;
DROP TABLE IF EXISTS profiles;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    phone TEXT,
    dob TEXT,
    gender TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    country TEXT,
    pincode TEXT,
    about TEXT,
    photo TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    degree TEXT,
    institute TEXT,
    passing_year TEXT,
    cgpa TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE experience (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    company TEXT,
    role TEXT,
    duration TEXT,
    description TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    skill_name TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    project_name TEXT,
    description TEXT,
    github_link TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE certificates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    certificate_name TEXT NOT NULL,
    organization TEXT,
    year TEXT,
    certificate_file TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);