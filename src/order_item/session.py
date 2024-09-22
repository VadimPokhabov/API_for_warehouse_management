#
# from sqlalchemy import create_engine, MetaData, Table, select, func
#
# engine = create_engine('sqlite:///your_database.db')
# metadata = MetaData()
# your_table = Table('your_table_name', metadata, autoload=True, autoload_with=engine)
#
# with engine.connect() as connection:
#     query = select([func.count()]).where(your_table.c.column_name == 'desired_value')
#     value_exists = connection.execute(query).scalar() > 0
#
#

