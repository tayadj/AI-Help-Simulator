import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.future
import sqlalchemy.orm



class ModelConfig:

    class Base(sqlalchemy.orm.DeclarativeBase):

        pass

    class Config(Base):

        __tablename__ = 'configs'

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(sqlalchemy.BigInteger, primary_key = True)
        key: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(255), unique = True, nullable = False)
        value: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(255), nullable = False)

    async def create_config(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int, key: str, value: str):

        config = self.Config(id = id, key = key, value = value)
        database.add(config)

        await database.commit()
        await database.refresh(config)

        return config

    async def read_config(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int):

        config = await database.get(self.Config, id)

        return config

    async def update_config(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int, key: str, value: str):

        config = await database.get(self.Config, id)
        config.key = key
        config.value = value

        await database.commit()
        await database.refresh(config)

        return config

    async def delete_config(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int):

        config = await database.get(self.Config, id)

        await database.delete(config)
        await database.commit()

        return config