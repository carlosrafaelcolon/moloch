CREATE TABLE IF NOT EXISTS message (
    id VARCHAR(255) NOT NULL PRIMARY KEY,
    created_on DATETIME DEFAULT CURRENT_TIMESTAMP,
    role VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    conversation_id VARCHAR(255) NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversation(id)
);