CREATE TABLE IF NOT EXISTS conversation (
    id VARCHAR(255) PRIMARY KEY,
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    retriever VARCHAR(255),
    memory VARCHAR(255),
    llm VARCHAR(255),
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);