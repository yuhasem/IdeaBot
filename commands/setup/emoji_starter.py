from libs import command
import re

class Command(command.DirectOnlyCommand, command.AdminCommand, command.Multi):
    def matches(self, message):
        args = re.search(r'emoji\s?->\s?(\S+)', message.content, re.I)
        return args!=None

    def action(self, message, send_func, bot):
        args = re.search(r'emoji\s?->\s?(\S+)', message.content, re.I)
        if args.group(1) in bot.reactions:
            reply = yield from send_func(message.channel, "React with the emoji you want to set")
            self.public_namespace.active_emoji_messages[message.id]=args.group(1)
            self.public_namespace.active_emoji_messages[reply.id]=args.group(1)
            #print(self.public_namespace.active_emoji_messages)