from discord.ext import commands, tasks
from aux.twitch_aux import Twitch_Aux
from aux.twilio_aux import Twilio_Aux
from aux.other import (
    check_phone_number_in_dms,
    extract_phone_number,
    encrypt,
    decrypt
)

from database.models import StreamerModel, SubscriberModel
from database import Session

from sqlalchemy import select, and_

class Twitch_Notifications(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.twitch_listner_status = False 
        self.texting_status = False

    @tasks.loop(seconds=60)
    async def twitch_listener(self, ctx):
        """
        function that runs every minute to report streamers' live/offline statuses
        to the discord and to their subscribers.
        
        Additionally updates streamers' live/offline statuses in the DB
        """
        print("initiating loop")

        with Session() as session:
            # iterate through all streamers in the DB to update statuses
            select_streamers_query = select(StreamerModel).order_by(StreamerModel.id)
            for row in session.execute(select_streamers_query):
                db_streamer : StreamerModel = row.StreamerModel
                
                # from the twitch username, create a Twitch_Aux instance with
                # current properties of the streamer (are they live, what game they're streaming, etc)
                curr_streamer: Twitch_Aux = Twitch_Aux(db_streamer.twitch_name)
                
                # We run an update when a streamer's current status is different from
                # their status last saved in the DB
                if curr_streamer.is_live != db_streamer.is_live:
                    
                    print(f"{curr_streamer.twitch_name}\'s subscriber\'s phone numbers:")
                    
                    # building phone_number:subscriber_name dictionary
                    subscriber_dict = dict()
                    for subscriber in db_streamer.subscribers:
                        sub_phone = decrypt(subscriber.phone_number)
                        sub_name = self.client.get_user(int(subscriber.discord_id)).name
                        subscriber_dict[sub_phone] = sub_name
                        print(sub_phone)

                    twilio_aux = Twilio_Aux()

                    # CASE 1: the current streamer went live
                    if curr_streamer.is_live:
                        # messaging the discord
                        await ctx.send(
                            f"{curr_streamer.twitch_name} is now live!\n"
                            f"Go check it out on {curr_streamer.get_stream_link()}\n"
                        )

                        # texting subscribers
                        if self.texting_status:
                            for phone_number, subscriber_name in subscriber_dict.items():
                                twilio_aux.send_message(
                                    phone_number= phone_number,
                                    body= (
                                        f"🤖hello {subscriber_name}, robo-corg reporting:🤖;\n"
                                        f"{curr_streamer.twitch_name} is now streaming \"{curr_streamer.title}\"\n"
                                        f"Playing {curr_streamer.game}\n"
                                        f"Go check it out on {curr_streamer.get_stream_link()}\n"
                                    )
                                )
                    else:
                    # CASE 2: the current streamer went offline
                        await ctx.send(
                            f"{curr_streamer.twitch_name} is now offline"
                        )
                        
                        # texting subscribers
                        if self.texting_status:
                            for phone_number, subscriber_name in subscriber_dict.items():
                                twilio_aux.send_message(
                                    phone_number = phone_number,
                                    body= f"{curr_streamer.twitch_name} is now offline"
                                )
                
                    db_streamer.is_live = curr_streamer.is_live
                    session.commit()
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toggle_twitch_notifs(self, ctx):
        """
        command to toggle <twitch_listener()> loop between ON and OFF
        """
        if self.twitch_listner_status is False:
            self.twitch_listner_status = True

            await ctx.send("twitch live notifications STARTING...")
            self.twitch_listener.start(ctx)
        else:
            self.twitch_listner_status = False

            await ctx.send("twitch live notifications STOPPING...")
            self.twitch_listener.stop()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toggle_texting(self, ctx):
        """
        command to toggle the texting-subscribers-feature ON or OFF
        CAUTION: TEXTING WILL DRAW MONEY FROM TWILIO ACCOUNT
        """
        if self.texting_status is False:
            self.texting_status = True
            await ctx.send("texting is turned ON")
        else:
            self.texting_status = False
            await ctx.send("texting is turned OFF")

    @commands.command()
    async def twitch_notifs_status(self, ctx):
        """
        command to check if <twitch_listener()> loop is running
        """
        if self.twitch_listner_status:
            await ctx.send("Twitch Live notifications are ON")
        else:
            await ctx.send("Twitch Live notifications are OFF")
    
    @commands.command()
    async def texting_status(self, ctx):
        """
        command to check if texting-subscribers-feature is enabled or disabled
        """
        if self.texting_status:
            await ctx.send("Texting subscribers when streamer goes live is ENABLED")
        else:
            await ctx.send("Texting subscribers when streamer goes live is DISABLED")

    @commands.command()
    async def subscribe_to(self, ctx, twitch_name):
        """
        command for user to subscribe their phone number to a streamer and receive
        text notifications when said streamer goes live/offline

        :param twitch_name: <str> the streamer's twitch username (ex. "asmongold")
        """

        # get discord ID of the user who issued this command
        sender_id = str(ctx.author.id)
        
        # query Streamer with 'twitch_name' from STREAMER_TBL to see if 
        # the streamer user wants to subscribe to exists
        with Session() as session:
            streamer : StreamerModel = get_streamer_from_db(twitch_name, session)

            # query Subscriber with 'sender_id' from SUBSCRIBER_TBL
            # if this subscriber already exists in the DB, we just create a relation
            # between existing subscriber and the streamer
            subscriber: SubscriberModel = get_subscriber_from_db(sender_id, session)

            if streamer is not None:
                # CASE 1: subscriber already exists
                if subscriber is not None:
                    streamer.subscribers.append(subscriber)
                    await ctx.send("done")
                else:
                # CASE 2: subscriber doesn't already exist 
                # => we need to create a new row in SUBSCRIBER_TBL
                    # dm for phone number
                    await ctx.author.send(
                        f"To receive text notifications for {streamer.twitch_name}, please enter your phone number\n"
                        f"robo-corg promises to keep this information confidential!"
                    )

                    # retreive response from subscriber DMs
                    # extract phone number from response
                    resp = (
                        await self.client.wait_for('message', check=check_phone_number_in_dms)
                    ).content
                    phone_number = extract_phone_number(resp)
                    
                    # encrypt phone number
                    encrypted_phone_number = encrypt(phone_number)

                    # creating new subscriber based on schema and adding relationship
                    # to STREAMBER_TBL
                    new_sub = SubscriberModel(
                        phone_number = encrypted_phone_number,
                        discord_id = str(ctx.author.id)
                    )
                    streamer.subscribers.append(new_sub)

                # TODO: text the new subscriber that they're now subscribed
                # to <STREAMER_NAME>

                session.commit()
            else:
                await ctx.send(
                    f"{twitch_name} isn't registered with robo-corg yet." 
                    f"Please use `add_streamer` first."
                )
    @commands.command()
    async def unsubscribe_from(self, ctx, twitch_name):
        """
        command for user to unsubscribe their phone number from receiving text
        notifications when <twitch_name> streamer goes live/offline

        :param twitch_name: <str> the streamer's twitch username (ex. "asmongold")
        """
        # check if <twitch_name> is even a twitch streamer
        streamer:Twitch_Aux = Twitch_Aux(twitch_name)
        if not streamer.exists():
            await ctx.send(
                f"err: there isn't a twitch streamer named {twitch_name}\n"
            )

        # get the user's id
        user_id = str(ctx.author.id)

        with Session() as session:
            # check if the user is subscribed to <twitch_name> by cross-referencing
            # discord IDs
            # 
            # select streamer 
            # where name = twitch_name and has sub with discord id = user_id
            select_stmt = (
                select(StreamerModel).
                where(
                    and_(
                        StreamerModel.subscribers.any(
                            SubscriberModel.discord_id==user_id
                        ),
                        StreamerModel.twitch_name == twitch_name
                    )
                )
            )

            # execute the 
            stmt_result = session.execute(select_stmt)
            first_row = stmt_result.first()
            
            # CASE 1: you weren't originally subscribed to 
            if not first_row:
                await ctx.send(
                    f"err: you weren\'t originally subscribed to {twitch_name}"
                )
            else:
                db_streamer : StreamerModel = first_row.StreamerModel
                curr_subscriber : SubscriberModel = get_subscriber_from_db(user_id, session)
                db_streamer.subscribers.remove(curr_subscriber)
                

    @commands.command()
    async def add_streamer(self, ctx, twitch_name):
        """
        command for user to add a streamer to twitch_notifications system

        :param twitch_name: <str> the streamer's twitch username (ex. "asmongold")
        """
        # checking that streamer exists on Twitch
        streamer: Twitch_Aux = Twitch_Aux(twitch_name)

        # CASE 1: the streamer DOESN'T exist on Twitch
        if not streamer.exists():
            await ctx.send(
                f"there isn't a twitch streamer named {twitch_name}\n"
            )
        else:
        # CASE 2: the streamer DOES exist on Twitch
            with Session() as session:
                # check first if the streamer we want to add is already in the db!!
                db_streamer : StreamerModel = get_streamer_from_db(twitch_name, session)
                
                # CASE 1: streamer already exists in the database => we do nothing
                if db_streamer is not None:
                    await ctx.send(
                        f"{twitch_name} is already in the system!"
                    )
                else:
                # CASE 2: streamer doesn't exist in the DB yet, we create a new streamer
                    sm = StreamerModel(
                        twitch_name = streamer.twitch_name,
                        is_live = False
                    )

                    session.add(sm)
                    session.commit()

                    await ctx.send(
                        f"{twitch_name} has been added to the system!"
                    )

    @commands.command()
    async def remove_streamer(self, ctx, twitch_name):
        with Session() as session:
            db_streamer: StreamerModel = get_streamer_from_db(twitch_name, session)

            if db_streamer is not None:
                session.delete(db_streamer)
                
                await ctx.send(
                    f"Sad to see you go, {twitch_name}"
                )
            else:
                await ctx.send(
                    f"{twitch_name} is not in the system."
                )
            session.commit()

def get_streamer_from_db(twitch_username:str, session):
    streamer = session.query(StreamerModel).filter(
        StreamerModel.twitch_name.ilike(f"%{twitch_username}%")
    ).first()
    return streamer        

def get_subscriber_from_db(subscriber_discord_id:str, session):
    subscriber = session.query(SubscriberModel).filter(
        SubscriberModel.discord_id.ilike(f"%{subscriber_discord_id}%")
    ).first()
    return subscriber
        

def setup(client):
    client.add_cog(Twitch_Notifications(client))