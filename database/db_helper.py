import asyncio
import asyncpg


class DataBase:
    def __init__(self, user: str = 'postgres',
                password: str = "postgres",
                database: str = "database",
                host: str = "127.0.0.1",
                  ):
        self.user = user
        self.password = password
        self.database = database, 
        self.host = host
    
    async def _create_connection(self):
        conn = await asyncpg.connect(
            user = self.user,
            password = self.password = password,
            database = self.database = database, 
            host = self.host = host,
        )
    def run(self):
        asyncio.run(self._create_connection())

        