from __future__ import annotations

import sqlite3
from datetime import datetime

from app.models.comment import Comment
from app.services.videos import _connect, get_video

_SCHEMA = """
CREATE TABLE IF NOT EXISTS comments (
    id TEXT PRIMARY KEY,
    video_id TEXT NOT NULL,
    author TEXT NOT NULL,
    body TEXT NOT NULL,
    parent_id TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(video_id) REFERENCES videos(id),
    FOREIGN KEY(parent_id) REFERENCES comments(id)
);

CREATE INDEX IF NOT EXISTS idx_comments_video_created
ON comments(video_id, datetime(created_at));
"""


def init_comment_store() -> None:
    with _connect() as connection:
        connection.executescript(_SCHEMA)


def _row_to_comment(row: sqlite3.Row) -> Comment:
    return Comment(
        id=row["id"],
        video_id=row["video_id"],
        author=row["author"],
        body=row["body"],
        parent_id=row["parent_id"],
        created_at=datetime.fromisoformat(row["created_at"]),
    )


def _insert(connection: sqlite3.Connection, comment: Comment) -> None:
    connection.execute(
        """
        INSERT INTO comments (id, video_id, author, body, parent_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            comment.id,
            comment.video_id,
            comment.author,
            comment.body,
            comment.parent_id,
            comment.created_at.isoformat(),
        ),
    )


def list_comments(video_id: str) -> list[Comment]:
    init_comment_store()
    with _connect() as connection:
        rows = connection.execute(
            "SELECT * FROM comments WHERE video_id = ? ORDER BY datetime(created_at) ASC",
            (video_id,),
        ).fetchall()
    return [_row_to_comment(row) for row in rows]


def create_comment(comment: Comment) -> Comment:
    init_comment_store()
    if get_video(comment.video_id) is None:
        raise ValueError("Video not found")
    with _connect() as connection:
        if comment.parent_id is not None:
            parent = connection.execute(
                "SELECT id FROM comments WHERE id = ? AND video_id = ?",
                (comment.parent_id, comment.video_id),
            ).fetchone()
            if parent is None:
                raise ValueError("Parent comment not found")
        _insert(connection, comment)
    return comment
