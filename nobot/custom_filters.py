from  pyrogram import filters
import re


def inline_query(data):
    async def func(flt, _, query):
        match = re.search(flt.data, query.query)
        if match == None:
            return False
        else:
            return True
    return filters.create(func,data=data)