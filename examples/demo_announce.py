#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path

import qqbot
from qqbot.core.util.yaml_util import YamlUtil
from qqbot.model.announce import CreateAnnounceRequest, CreateChannelAnnounceRequest

test_config = YamlUtil.read(os.path.join(os.path.dirname(__file__), "config.yaml"))


async def _announce_handler(event, message: qqbot.Message):
    msg_api = qqbot.AsyncMessageAPI(t_token, False)
    announce_api = qqbot.AsyncAnnouncesAPI(t_token, False)

    qqbot.logger.info("event %s" % event + ",receive message %s" % message.content)

    # 先发送消息告知用户
    message_to_send = qqbot.MessageSendRequest("command received: %s" % message.content)
    await msg_api.post_message(message.channel_id, message_to_send)

    message_id = "088de19cbeb883e7e97110a2e39c0138d401"
    if "/建公告" in message.content:
        create_announce_request = CreateAnnounceRequest(message.channel_id, message_id)
        await announce_api.create_announce(message.guild_id, create_announce_request)

    elif "/删公告" in message.content:
        await announce_api.delete_announce(message.guild_id, message_id)

    elif "/建子频道公告" in message.content:
        create_channel_announce_request = CreateChannelAnnounceRequest(message_id)
        await announce_api.create_channel_announce(
            message.channel_id, create_channel_announce_request
        )

    elif "/删子频道公告" in message.content:
        await announce_api.delete_channel_announce(message.channel_id, message_id)


if __name__ == "__main__":
    t_token = qqbot.Token(test_config["token"]["appid"], test_config["token"]["token"])
    qqbot_handler = qqbot.Handler(
        qqbot.HandlerType.MESSAGE_EVENT_HANDLER, _announce_handler
    )
    qqbot.async_listen_events(t_token, False, qqbot_handler)
