from libs import reaction #as reactioncommand

class Reaction(reaction.ReactionAddCommand):
    '''A Reaction command for getting the ID of an emoji

    **Usage:**
    React to a message containing the word "id" with the emoji you want the ID of

    **NOTE:** This is a debug command, so it may be removed or deprecated without notice in the future'''
    def matches(self, reaction, user):
        return " id " in reaction.message.content.lower() or " id" == reaction.message.content.lower()[-3:] or "id " == reaction.message.content.lower()[:3] or "id"==reaction.message.content.lower()

    def action(self, reaction, user, client):
        try:
            yield from self.send_message(reaction.message.channel, "Name: `" + reaction.emoji.name + "`\nID: `" + reaction.emoji.id + "`")
        except AttributeError:
            yield from self.send_message(reaction.message.channel, reaction.emoji + " doesn't have an ID")
            print(reaction.emoji)
