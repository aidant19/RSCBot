from datetime import datetime
# Discord ID: Steam ID -- maybe handle multiple accounts?

# ###############################################################################

# ## Important info: 
#
# ### What's going on here?
#
# Listed below are quick settings for testing purposes. Replay searches are performed on the replay uploader,
# downloaded, then uploaded again to ballchasing under the replay "group_owner". For testing purposes, it is easiest
# for the developer (you) to be the group owner, because this gives you hands on control of your testing environment.
# Eventually, the group owner will be RSC. Their steam account for ballchasing uploads has been associated with
# the RSCBot ID.
#
#
# ### How do I test this?
#
# Step 0: Install dependancies
# Step 1: Set auth_token to a token generated from ballchasing
# Step 2: Set group_owner_discord_id to your discord ID
# Step 3: Add a discord : steam key value pair to account_register for your discord ID and steam ID
# Step 4: Create a Ballchasing Replay group
# Step 5: set top_level_group to the ID of this replay group (can be found in replay group URL)
# Step 6: execute py ReplayManager.py
#

class config:

    # ## Quick Settings for New Tester:
    auth_token = "Ght7UfDSmDeA58GPc3A8QnRfmM93LX7Z6U9g7LG0"     # setting
    group_owner_discord_id = 302079469882179585                 # Group Owner Discord ID >> This is the HOST (eventually RSC)
    uploader_discord_id = 606888593817862144                    # Discord User who uploaded replays (discord id : ballchasing id pair in account_register below) >> This is TEMPORARILY set as RSC for testing purposes
    top_level_group =  "test-group-cl0dozmu3o"                  # setting -- Note: Group names are unique

    # ###############################################################################

    search_count = 10

    visibility = 'public'
    team_identification = 'by-player-clusters'                  # setting -- Alternative: 'by-distinct-players'
    player_identification = 'by-id'                             # setting -- Alternative 'by-name'

    tier = "Contender"        # teamManager cog (from my_team)
    match_day = 4

    match = {
        'matchDay': match_day,
        'matchDate': datetime.strptime("January 27, 2021", '%B %d, %Y').date(),
        'home': "Dart Frogs",
        'away': "Samurai",
    }

    # Ballchasing subgroups: 1Premier, 2Master, etc.
    tier_rank = {
        "Premier": 1,
        "Master": 2,
        "Elite": 3,
        "Major": 4,
        "Minor": 5,
        "Challenger": 6,
        "Prospect": 7,
        "Contender": 8,
        "Amateur": 9
    }

    account_register = {
        606888593817862144: ["steam", "76561199096013422"],                 # RSCBot : uploads
        302079469882179585: ["steam", "76561198380344413"],                 # nullidea
        144208625907269632: ["steam", "76561198079435423"],                 # aiTan
        196505476295294976: ["xbox", "e4b17b0000000900"],                   # SirZohan
        507640587164581918: ["ps4", "touchetupac2"],                        # touchetupac2
        755863682663186490: ["epic", "76edd61bd58841028a8ee27373ae307a"]    # pricytugboat
    }