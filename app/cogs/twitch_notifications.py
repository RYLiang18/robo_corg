from discord.ext import commands, tasks
from aux.twitch_aux import Twitch_Aux
from aux.twilio_aux import Twilio_Aux
from aux.other import (
    check_phone_number_in_dms,
    extract_phone_number,
    encrypt,
    decrypt,
)

from database.models import StreamerModel, SubscriberModel
from database import Session

from sqlalchemy import select

class Twitch_Notifications(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
        self.listener_status = False

    @tasks.loop(seconds=60)
    async def twitch_listener(self, ctx):
        """
        function that runs every minute to report streamers' live/offline statuses
        to the discord and to their subscribers.
        
        Additionally updates streamers' live/offline statuses in the DB
        """
        print("initiating loop")

        session = Session()
        
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
                    for phone_number, subscriber_name in subscriber_dict.items():
                        twilio_aux.send_message(
                            phone_number = phone_number,
                            body= f"{curr_streamer.twitch_name} is now offline"
                        )
            
                db_streamer.is_live = curr_streamer.is_live
                session.commit()
        session.close()
    
    @commands.command()
    async def start_twitch_notifs(self, ctx):
        """
        command to START `twitch_listener()` loop
        """
        await ctx.send("twitch live notifications STARTING...")
        self.twitch_listener.start(ctx)
    
    @commands.command()
    async def stop_twitch_notifs(self, ctx):
        """
        command to STOP `twitch_listener()` loop
        """
        await ctx.send("twitch live notifications STOPPING...")
        self.twitch_listener.stop()

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
        session = Session()
        streamer : StreamerModel = get_streamer_from_db(twitch_name, session)

        # query Subscriber with 'sender_id' from SUBSCRIBER_TBL
        # if this subscriber already exists in the DB, we just create a relation
        # between existing subscriber and the streamer
        subscriber: SubscriberModel = get_subscriber_from_db(sender_id, session)

        if streamer is not None:
            # CASE 1: subscriber already exists
            if subscriber is not None:
                streamer.subscribers.append(subscriber)
                ctx.send("done")
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
            session.close()

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
            # TODO: check first if the streamer already exists in the DB first!
            session = Session()
            sm = StreamerModel(
                twitch_name = streamer.twitch_name,
                is_live = False
            )

            session.add(sm)
            session.commit()
            session.close()

            await ctx.send(
                f"{twitch_name} has been added to the system!"
            )
    

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