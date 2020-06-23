#!/usr/bin/env python3


def get_message(ctx) -> str:
    msg = ctx.message.content
    prefix_used = ctx.prefix
    alias_used = ctx.invoked_with
    return msg[len(prefix_used) + len(alias_used):].strip()
