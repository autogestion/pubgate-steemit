import asyncio

from steem.blog import Blog
from sanic.log import logger

from pubgate.db import Outbox, User
from pubgate.activity import Create
from pubgate.contrib.parsers import process_tags


async def steemit_bot(app):
    while True:
        active_bots = await User.find(filter={"details.stbot.enable": True})
        for bot in active_bots.objects:
            first_start = not bot["details"]["stbot"].get('launched', None)
            blogs = [Blog(name) for name in bot["details"]["stbot"]["blogs"]]
            for blog in blogs:

                if first_start:
                    posts = blog.take(limit=app.config.FETCH_ON_START)
                    for entry in posts:
                        await process_entry(bot, entry)
                    await User.update_one(
                        {'name': bot.name},
                        {'$set': {"details.stbot.launched": True}}
                    )

                else:
                    while True:
                        entry = blog.take(limit=1)[0]
                        exists = await Outbox.find_one({
                            "user_id": bot.name,
                            "steem_id": entry.permlink
                        })
                        if exists:
                            break
                        await process_entry(bot, entry)

        await asyncio.sleep(app.config.STEEMIT_BOT_TIMEOUT)


async def process_entry(bot, entry):
    content = entry.body

    # process tags
    extra_tag_list = []
    extra_tag_list.extend(list(entry.tags))
    extra_tag_list.extend(bot["details"]["stbot"].get("tags", []))
    content, footer_tags, object_tags = process_tags(extra_tag_list, content)

    body = f"{entry.title}<br>{content}{footer_tags}"
    published = entry.created.replace(microsecond=0).isoformat() + "Z"

    activity = Create(bot, {
        "type": "Create",
        "cc": [],
        "published": published,
        "object": {
            "type": "Note",
            "summary": None,
            "content": body,
            "published": published,
            "attachment": [],
            "tag": object_tags
        }
    })
    await activity.save(steem_id=entry.permlink)
    await activity.deliver()
    logger.info(f"steemit entry '{entry.title}' of {bot.name} federating")
