import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.future
import sqlalchemy.orm



class ModelUser:

    class Base(sqlalchemy.orm.DeclarativeBase):

        pass

    class User(Base):

        __tablename__ = 'users'

        id: sqlalchemy.orm.Mapped[int] = sqlalchemy.orm.mapped_column(sqlalchemy.BigInteger, primary_key = True)
        name: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(255), nullable = False)
        email: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(255), unique = True, nullable = False)
        password: sqlalchemy.orm.Mapped[str] = sqlalchemy.orm.mapped_column(sqlalchemy.String(255), nullable = False)

    async def create_user(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int, name: str, email: str, password: str):

        user = self.User(id = id, name = name, email = email, password = password)
        database.add(user)

        await database.commit()
        await database.refresh(user)

        return user

    async def read_user(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int):

        user = await database.get(self.User, id)

        return user

    async def update_user(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int, name: str, email: str, password: str):

        user = await database.get(self.User, id)
        user.name = name
        user.email = email
        user.password = password

        await database.commit()
        await database.refresh(user)

        return user

    async def delete_user(self, database: sqlalchemy.ext.asyncio.AsyncSession, id: int):

        user = await database.get(self.User, id)

        await database.delete(user)
        await database.commit()

        return user