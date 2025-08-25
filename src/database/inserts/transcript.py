"""Insert Statements for youtube metadata."""

from src.database.inserts.base_insert_models import SQLInsertModel


class InsertYTMetadata(SQLInsertModel):
    """Insert YouTube metadata model."""

    template: str = """
        INSERT INTO
            yt_meta
            (video_id, language, language_code, is_generated)
        VALUES
            ($1, $2, $3, $4)
    """

    video_id: str
    language: str
    language_code: str
    is_generated: bool
