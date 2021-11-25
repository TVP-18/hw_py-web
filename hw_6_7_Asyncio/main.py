import asyncio
import aiosqlite

DB_NAME = 'contacts.db'


# async def read_db(db_name):
#     db = await aiosqlite.connect(db_name)
#     cursor = await db.execute('select first_name, last_name, email from contacts')
#     rows = await cursor.fetchall()
#     await cursor.close()
#     await db.close()
#     print(rows)
#     # return await rows

async def create_mail(person):

    text = f'Уважаемый {person[1]} {person[0]}!\nСпасибо, что пользуетесь нашим сервисом объявлений.'
    print(text)
    return await text


async def main():
    db = await aiosqlite.connect(DB_NAME)
    cursor = await db.execute('select first_name, last_name, email from contacts')
    rows = await cursor.fetchall()

    tasks = []
    for row in rows:
        task = asyncio.create_task(create_mail(row))
        tasks.append(task)
    emails = await asyncio.gather(*tasks)

    await cursor.close()
    await db.close()
    print(rows)


asyncio.run(main())

#
# from sqlite3 import connect
#
# db_connection = connect('contacts.db')
#
# db_cursor = db_connection.cursor()
#
#
# select_query = 'select first_name, last_name, email from contacts'
#
# PERSONS = db_cursor.execute(select_query).fetchall()
#
# print(PERSONS)



#
#
#
# async def email(person):
#     email = await
#     result = await session.get(url)
#     return await result.text()



