# Thunder/utils/database.py

import datetime
from typing import Optional, Dict, Any

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection

from Thunder.vars import Var
from Thunder.utils.logger import logger


def sanitize_db_name(name: str) -> str:
    """
    Sanitize MongoDB database name to prevent InvalidName errors.
    MongoDB disallows spaces and some special characters.
    """
    if not name:
        raise ValueError("Database name is empty")

    sanitized = (
        name.strip()
        .replace(" ", "_")
        .replace(".", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace("$", "_")
        .replace('"', "_")
    )

    if not sanitized:
        raise ValueError("Database name became empty after sanitization")

    return sanitized


class Database:
    def __init__(self, uri: str, database_name: str, *args, **kwargs):
        # ✅ Sanitize DB name (CRITICAL FIX)
        safe_db_name = sanitize_db_name(database_name)

        logger.info(f"Connecting to MongoDB database: {safe_db_name}")

        self._client = AsyncMongoClient(
            uri,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
            *args,
            **kwargs
        )

        self.db = self._client[safe_db_name]

        # Collections
        self.col: AsyncCollection = self.db.users
        self.banned_users_col: AsyncCollection = self.db.banned_users
        self.banned_channels_col: AsyncCollection = self.db.banned_channels
        self.token_col: AsyncCollection = self.db.tokens
        self.authorized_users_col: AsyncCollection = self.db.authorized_users
        self.restart_message_col: AsyncCollection = self.db.restart_message

    async def ensure_indexes(self):
        try:
            await self.banned_users_col.create_index("user_id", unique=True)
            await self.banned_channels_col.create_index("channel_id", unique=True)
            await self.token_col.create_index("token", unique=True)
            await self.authorized_users_col.create_index("user_id", unique=True)
            await self.col.create_index("id", unique=True)

            await self.token_col.create_index("expires_at", expireAfterSeconds=0)
            await self.token_col.create_index("activated")

            await self.restart_message_col.create_index("message_id", unique=True)
            await self.restart_message_col.create_index(
                "timestamp", expireAfterSeconds=3600
            )

            logger.debug("Database indexes ensured successfully.")
        except Exception as e:
            logger.error("Error ensuring database indexes", exc_info=True)
            raise

    def new_user(self, user_id: int) -> Dict[str, Any]:
        return {
            "id": user_id,
            "join_date": datetime.datetime.utcnow()
        }

    async def add_user(self, user_id: int):
        try:
            if not await self.is_user_exist(user_id):
                await self.col.insert_one(self.new_user(user_id))
                logger.debug(f"Added new user {user_id}")
        except Exception:
            logger.error(f"Failed to add user {user_id}", exc_info=True)
            raise

    async def is_user_exist(self, user_id: int) -> bool:
        try:
            return bool(
                await self.col.find_one({"id": user_id}, {"_id": 1})
            )
        except Exception:
            logger.error(f"Failed checking user {user_id}", exc_info=True)
            raise

    async def total_users_count(self) -> int:
        try:
            return await self.col.count_documents({})
        except Exception:
            logger.error("Failed counting users", exc_info=True)
            return 0

    def get_all_users(self):
        try:
            return self.col.find({})
        except Exception:
            logger.error("Failed getting all users", exc_info=True)
            return self.col.find({"_id": {"$exists": False}})

    async def delete_user(self, user_id: int):
        try:
            await self.col.delete_one({"id": user_id})
            logger.debug(f"Deleted user {user_id}")
        except Exception:
            logger.error(f"Failed deleting user {user_id}", exc_info=True)
            raise

    async def add_banned_user(
        self,
        user_id: int,
        banned_by: Optional[int] = None,
        reason: Optional[str] = None
    ):
        try:
            await self.banned_users_col.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "banned_at": datetime.datetime.utcnow(),
                        "banned_by": banned_by,
                        "reason": reason
                    }
                },
                upsert=True
            )
            logger.debug(f"Banned user {user_id}")
        except Exception:
            logger.error(f"Failed banning user {user_id}", exc_info=True)
            raise

    async def remove_banned_user(self, user_id: int) -> bool:
        try:
            return (await self.banned_users_col.delete_one(
                {"user_id": user_id}
            )).deleted_count > 0
        except Exception:
            logger.error(f"Failed unbanning user {user_id}", exc_info=True)
            return False

    async def is_user_banned(self, user_id: int) -> Optional[Dict[str, Any]]:
        try:
            return await self.banned_users_col.find_one({"user_id": user_id})
        except Exception:
            logger.error(f"Failed checking ban for user {user_id}", exc_info=True)
            return None

    async def add_banned_channel(
        self,
        channel_id: int,
        banned_by: Optional[int] = None,
        reason: Optional[str] = None
    ):
        try:
            await self.banned_channels_col.update_one(
                {"channel_id": channel_id},
                {
                    "$set": {
                        "channel_id": channel_id,
                        "banned_at": datetime.datetime.utcnow(),
                        "banned_by": banned_by,
                        "reason": reason
                    }
                },
                upsert=True
            )
            logger.debug(f"Banned channel {channel_id}")
        except Exception:
            logger.error(f"Failed banning channel {channel_id}", exc_info=True)
            raise

    async def remove_banned_channel(self, channel_id: int) -> bool:
        try:
            return (await self.banned_channels_col.delete_one(
                {"channel_id": channel_id}
            )).deleted_count > 0
        except Exception:
            logger.error(f"Failed unbanning channel {channel_id}", exc_info=True)
            return False

    async def is_channel_banned(self, channel_id: int) -> Optional[Dict[str, Any]]:
        try:
            return await self.banned_channels_col.find_one({"channel_id": channel_id})
        except Exception:
            logger.error(f"Failed checking ban for channel {channel_id}", exc_info=True)
            return None

    async def save_main_token(
        self,
        user_id: int,
        token_value: str,
        expires_at: datetime.datetime,
        created_at: datetime.datetime,
        activated: bool
    ):
        try:
            await self.token_col.update_one(
                {"user_id": user_id, "token": token_value},
                {
                    "$set": {
                        "expires_at": expires_at,
                        "created_at": created_at,
                        "activated": activated
                    }
                },
                upsert=True
            )
        except Exception:
            logger.error(f"Failed saving token for user {user_id}", exc_info=True)
            raise

    async def add_restart_message(self, message_id: int, chat_id: int):
        try:
            await self.restart_message_col.insert_one({
                "message_id": message_id,
                "chat_id": chat_id,
                "timestamp": datetime.datetime.utcnow()
            })
        except Exception:
            logger.error("Failed adding restart message", exc_info=True)

    async def get_restart_message(self) -> Optional[Dict[str, Any]]:
        try:
            return await self.restart_message_col.find_one(
                sort=[("timestamp", -1)]
            )
        except Exception:
            logger.error("Failed getting restart message", exc_info=True)
            return None

    async def delete_restart_message(self, message_id: int):
        try:
            await self.restart_message_col.delete_one({"message_id": message_id})
        except Exception:
            logger.error("Failed deleting restart message", exc_info=True)

    async def close(self):
        if self._client:
            await self._client.close()


# ✅ Global DB instance (SAFE)
db = Database(Var.DATABASE_URL, Var.NAME)
