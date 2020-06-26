#!/usr/bin/env python3
from typing import Optional


def get_message(ctx) -> Optional[str]:
    content = ctx.message.content
    prefix_used = ctx.prefix
    alias_used = ctx.invoked_with
    return content[len(prefix_used) + len(alias_used):].strip()
