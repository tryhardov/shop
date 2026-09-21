from sqlalchemy.ext.asyncio import AsyncSession


async def create(factory_class, db_session: AsyncSession, **kwargs):
    result = factory_class.build(**kwargs)

    db_session.add(result)
    await db_session.commit()
    await db_session.refresh(result)

    return result


async def create_batch(factory_class, db_session: AsyncSession, qt: int,  **kwargs):
    results = [factory_class.build(**kwargs) for _ in range(qt)]

    db_session.add_all(results)
    await db_session.commit()
    for result in results:
        await db_session.refresh(result)

    return results