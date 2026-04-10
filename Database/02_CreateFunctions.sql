\set schema_name `echo "$SCHEMA_DB"`

SET search_path TO :"schema_name";
CREATE EXTENSION IF NOT EXISTS vector;

CREATE OR REPLACE FUNCTION search_ingredients(
    query_vec vector(640),
    limit_results int DEFAULT 10,
    threshold float DEFAULT 0.5
)
RETURNS TABLE(id UUID, Score float)
LANGUAGE sql
AS $$
    SELECT id, ("Embedding" <=> query_vec) AS Score
    FROM "INGREDIENTS_EMBEDDINGS"
    WHERE ("Embedding" <=> query_vec) < 1 - threshold
    ORDER BY "Embedding" <=> query_vec ASC
    LIMIT limit_results;
$$;

GRANT EXECUTE ON FUNCTION search_ingredients(vector(640), int, float) TO reader_data , loader_data;