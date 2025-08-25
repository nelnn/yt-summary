CREATE EXTENSION IF NOT EXISTS vector;

-- Metadata table for YouTube videos
CREATE TABLE IF NOT EXISTS yt_meta (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(50) NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    uploader VARCHAR(50) NOT NULL,
    uploader_id VARCHAR(50) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    channel_id VARCHAR(50) NOT NULL,
    upload_date DATE NOT NULL,
    duration INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_video_id ON yt_meta(video_id);
CREATE INDEX idx_created_at ON yt_meta(created_at);

ALTER TABLE yt_meta
ADD CONSTRAINT unique_video_language
UNIQUE (video_id, language_code, is_generated);


COMMENT ON TABLE yt_meta IS 'Table storing YouTube video metadata';
COMMENT ON COLUMN yt_meta.id IS 'Primary key of the table';
COMMENT ON COLUMN yt_meta.video_id IS 'YouTube video ID';
COMMENT ON COLUMN yt_meta.title IS 'YouTube video title';
COMMENT ON COLUMN yt_meta.description IS 'YouTube video description';
COMMENT ON COLUMN yt_meta.uploader IS 'Name of the uploader';
COMMENT ON COLUMN yt_meta.uploader_id IS 'ID of the uploader';
COMMENT ON COLUMN yt_meta.channel IS 'Name of the channel';
COMMENT ON COLUMN yt_meta.channel_id IS 'ID of the channel';
COMMENT ON COLUMN yt_meta.upload_date IS 'Date when the video was uploaded';
COMMENT ON COLUMN yt_meta.duration IS 'Duration of the video in seconds';
COMMENT ON COLUMN yt_meta.created_at IS 'Timestamp when the record was created';
COMMENT ON COLUMN yt_meta.updated_at IS 'Timestamp when the record was last updated';



-- llama embeddings table
-- CREATE TABLE IF NOT EXISTS llama_embeddings (
--     id SERIAL PRIMARY KEY,
--     yt_meta_id INTEGER NOT NULL,
--     embedding_openai VECTOR(1536) NOT NULL,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     FOREIGN KEY (yt_meta_id) REFERENCES yt_meta(id) ON DELETE CASCADE
-- );
-- CREATE INDEX ON llama_embeddings USING hnsw (embedding_openai vector_l2_ops);

-- COMMENT ON TABLE llama_embeddings IS 'Table storing Llama embeddings for YouTube videos';
-- COMMENT ON COLUMN llama_embeddings.id IS 'Primary key of the table';
-- COMMENT ON COLUMN llama_embeddings.yt_meta_id IS 'Foreign key referencing yt_meta table';
-- COMMENT ON COLUMN llama_embeddings.embedding_openai IS 'Llama embedding vector of Open AI embeddingsfor the video';
-- COMMENT ON COLUMN llama_embeddings.created_at IS 'Timestamp when the embedding was created';
