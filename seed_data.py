from aux.twitch_aux import Twitch_Aux

streamers_seed = [
    # these discord ids are robocorg
    {
        'twitch_name':'okcode', 
        'discord_id': '846904592372596736', 
        'is_live':Twitch_Aux('okcode').is_live
    },
    {
        'twitch_name':'tuonto', 
        'discord_id': '846904592372596736', 
        'is_live':Twitch_Aux('tuonto').is_live
    },
    {
        'twitch_name':'ludwig', 
        'discord_id': '846904592372596736', 
        'is_live':Twitch_Aux('ludwig').is_live
    },
    {
        'twitch_name':'39daph', 
        'discord_id': '846904592372596736', 
        'is_live':Twitch_Aux('39daph').is_live
    },
    {
        'twitch_name':'fuslie', 
        'discord_id': '846904592372596736', 
        'is_live':Twitch_Aux('fuslie').is_live
    },
    {
        'twitch_name':'lilypichu', 
        'discord_id': '846904592372596736', 
        'is_live':Twitch_Aux('lilypichu').is_live
    },
    {
        'twitch_name':'enviosity', 
        'discord_id': '846904592372596736', 
        'is_live':Twitch_Aux('enviosity').is_live
    },
    {
        'twitch_name':'tenhatv', 
        'discord_id': '846904592372596736', 
        'is_live':Twitch_Aux('tenhatv').is_live
    }
]

subscribers_seed = [
    {
        'phone_number': '19498912046',
        'discord_id': '844378570633379880'
    },
    {
        'phone_number': '19492290909',
        'discord_id': '844378570633379880'
    },
]

relationship_seed = [
    {
        'phone_number':'19498912046',
        'twitch_name': 'okcode'
    },
    {
        'phone_number':'19498912046',
        'twitch_name': 'lilypichu'
    },
    {
        'phone_number':'19492290909',
        'twitch_name': 'tenhatv'
    },
    {
        'phone_number':'19492290909',
        'twitch_name': 'enviosity'
    }
]
