from reactions import reactioncommand
import asyncio

ballots=dict() #dict associating User IDs with vote (Message) IDs
REACTIONS = [chr(x) for x in list(range(127462, 127462+26))] #all the regional indicators from 🇦 to 🇿
FIRST_REACTION_ORD = 127462
MODE = "mode"
VOTES = "votes"
NAME = "name"

class StartBallot(reactioncommand.AdminReactionAddCommand):
    def __init__(self, vote_dict=None, **kwargs):
        super().__init__(**kwargs)
        self.vote_dict=vote_dict
    def matches(self, reaction, user):
        return reaction.message.id in self.vote_dict
    def action(self, reaction, user, client):
        ballots[user.id]=reaction.message.id
        message = "Poll: **"+self.vote_dict[reaction.message.id][NAME]+"**\n"
        for i in range(len(self.vote_dict[reaction.message.id][VOTES].options)):
            message += REACTIONS[i]+" : "+self.vote_dict[reaction.message.id][VOTES].options[i]+"\n"
        message +="""
Please place your vote by reacting with your choice(s). 
In the event that multiple choices are accepted, choices will be considered in chronological order (ie first reaction is first choice, second reaction is second choice, etc).
**No take-backsies.**"""
        yield from client.send_message(user, message)

class RegisterVote(reactioncommand.ReactionAddCommand):
    def __init__(self, vote_dict=None, **kwargs):
        super().__init__(**kwargs)
        self.vote_dict=vote_dict
    def matches(self, reaction, user):
        return reaction.emoji in REACTIONS and ballots[user.id] in self.vote_dict and ord(reaction.emoji)-FIRST_REACTION_ORD < len(self.vote_dict[ballots[user.id]][VOTES].options) and ord(reaction.emoji)>=FIRST_REACTION_ORD and reaction.message.server == None
    @asyncio.coroutine
    def action(self, reaction, user):
        self.vote_dict[ballots[user.id]][VOTES].addChoice(user.id, self.vote_dict[ballots[user.id]][VOTES].options[ord(reaction.emoji)-FIRST_REACTION_ORD])
