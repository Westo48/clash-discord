# ClashDiscord

Discord bot for Clash of Clans discord servers written in Python

# Table of Contents

- [Introduction](#introduction)
- [Setup](#setup)
  - [Setup Summary](#setup-summary)
- [Usage](#usage)
- [Command List](#command-list)
  - [ClashDiscord](#command-list-clashdiscord)
  - [Discord](#command-list-discord)
  - [Player](#command-list-player)
  - [Clan](#command-list-clan)
  - [War](#command-list-war)
  - [CWL Group](#command-list-cwl-group)
  - [CWL War](#command-list-cwl-war)
- [Contributing](#contributing)
- [Requirements](#requirements)
- [Links and Contact](#links-and-contact)

# <a id="introduction"></a>Introduction

ClashDiscord is a discord bot written in Python that, while having a great many uses and commands, focuses _primarily_ on discord member management. This entails, but is not limited to, adding an uninitiated role to incoming members, allowing members to give themselves roles based on their clash of clans profile, and focusing on discord server security.

Non-management commands include, but are also not limited to, returning player or clan information based on their tag, getting troop levels and how close they are to max for their town hall as well as total max, who can donate the best of a specific troop in a clan, war information, cwl lineup, cwl war, and cwl clan member scores.

# <a id="setup"></a>Setup

Getting ClashDiscord set up in your discord server can be somewhat confusing, but never fear for I am here.

1. invite ClashDiscord to your discord server

   - invite link can be found in [official discord](https://discord.gg/3jcfaa5NYk) server

2. claim your user in ClashDiscord

   - !claimuser
     - this will claim you as a user
     - _this can be done in any claimed guild_

3. claim your discord server

   - !claimguild
     - this will claim your discord server and add you as the guild admin within ClashDiscord
     - guild is what the discord API calls a server

4. link a player to your user

   - !claimplayer `playertag apikey`
     - claims the requested player and links it to your discord user
     - _this can be done in any claimed guild_
     - getting your api key is annoying, but for everyone’s security this is necessary

5. link a clan to your guild

   - !claimclan `clantag`
     - claims a clan and links it to the claimed guild
     - your active player **must** be in the clan
     - _this is also for security_

6. link existing roles to your server

   - claim clan roles
     - !claimclanrole `clantag mentionrole`
       - links the clan role to a claimed clan
       - _mentionrole means you have to @mention the role_

   B. claim rank roles

   - !claimrankrole `rank mentionrole`
     - links the rank role to a discord role
       - leader
       - co-leader
       - elder
       - member
       - uninitiated
         - _this means they aren't verified or they aren't in a claimed clan_

7. use clash discord, you are set up

# <a id="setup-summary"></a>Setup Summary

- invite Clash Discord to your server
- claim your discord user
- claim the guild
- claim your player
- claim your clan
- claim the necessary roles

# <a id="usage"></a>Usage

ClashDiscord is largely **command** focused, meaning it doesn't do anything that it is not told to do. The only exception to this is when a member joins. If a server has claimed an uninitiated role, then they will be given that role, otherwise nothing will happen. Once setup is complete you will be able to interact with ClashDiscord using the prefix `!` and run the commands as desired.

# <a id="command-list"></a>Command List

- ## <a id="command-list-clashdiscord"></a>ClashDiscord

  - ### User
    - claimuser
      - claims the user by discord user id within ClashDiscord
  - ### Player
    - claimplayer `playertag apikey`
      - links a player to your claimed user
      - if there are no other claimed players for your user, then sets this claimed player as active for you
    - deleteplayer `playertag`
      - removes the claimed player from your user
    - showplayerclaim
      - shows all claimed players for your user and which is set as active
    - updateplayeractive `playertag`
      - sets the requested player as your active player
  - ### Guild
    - claimguild
      - claims the guild by discord guild id within ClashDiscord
      - sets the user who called the command as the guild admin within ClashDiscord
  - ### Clan
    - claimclan `clantag`
      - claims the clan and links it to the claimed guild
      - user _must_ be guild admin
      - user's active player _must_ be in the clan
      - claimed guilds can claim multiple different clans
      - multiple guilds can claim the same clan
    - deleteclan `clantag`
      - removes the claimed clan from your guild
    - showclanclaim
      - shows all claimed clans for the guild
  - ### Role
    - showroleclaim
      - shows all claimed roles for the guild
  - ### Clan Role
    - claimclanrole `clantag rolemention`
      - links the mentioned role to a claimed clan
    - removeclaimclanrole `rolemention`
      - unclaims the mentioned clan role
  - ### Rank Role
    - claimrankrole `rank rolemention`
      - claims the mentioned role as a specific clan rank
      - list of ranks
        - leader
        - co-leader
        - elder
        - member
        - uninitiated
          - _this means they aren't verified or they aren't in a claimed clan_
    - removeclaimrankrole `rolemention`
      - unclaims the mentioned rank role

- ## <a id="command-list-discord"></a>Discord

  - help
    - displays relevant help-text regarding what commands can be run
  - role
    - adds and removes necessary roles in discord based on claimed players clan and role in that clan
  - rolemember `membermention`
    - adds and removes necessary roles in discord based on claimed players clan and role in that clan for mentioned discord user
    - restricted to leaders and co-leaders
  - roleall
    - adds and removes necessary roles in discord based on claimed players clan and role in that clan for all users in guild
    - restricted to leaders and co-leaders
  - finduser `player_tag`
    - returns the user linked to a requested player
    - example
      - `/finduser #RGQ8RGU9`
  - findclanusers
    - returns the users linked to the active player's clan

- ## <a id="command-list-player"></a>Player

  - findplayer `playertag`
    - displays player information for requested player tag
    - example
      - `/player #RGQ8RGU9`
      - `/player RGQ8RGU9`
  - player
    - shows player information based on your active player
  - memberplayer `mentionuser`
    - shows player information based on the mentioned user's active player
  - unitlvl `unitname`
    - shows the level of the requested unit, what the max for your town hall is, as well as the overall max
    - you can search troops, spells, and heroes
    - example
      - `/trooplvl hog rider`
      - `/trooplvl jump spell`
      - `/trooplvl archer queen`
  - allunitlvl
    - shows the level your units
  - allherolvl
    - shows the level your heroes
  - allpetlvl
    - shows the level your pets
  - alltrooplvl
    - shows the level your troops
  - allspelllvl
    - shows the level your spells
  - allsiegelvl
    - shows the level your sieges
  - activesupertroop
    - shows the super troops you have active

- ## <a id="command-list-clan"></a>Clan

  - findclan `clantag`
    - displays clan information for requested clan tag
    - example
      - `!clan #JJRJGVR0`
      - `!clan JJRJGVR0`
  - clan
    - displays clan information for clan active player is in
  - clanmention `mentionclanrole`
    - displays clan information for clan linked to the clan role mentioned
  - clanlineup
    - displays clan's town hall lineup
    - restricted to leaders and co-leaders
  - clanwarpreference
    - displays rundown of clan member's war preference
    - restricted to leaders and co-leaders
  - donate `unitname`
    - shows who can donate the best of a specified unit
    - uses active player's clan for all clan commands
    - example
      - `!donate hog rider`
      - `!donate freeze spell`
  - supertroopsearch `supertroopname`
    - shows players in your clan that have a specified super troop activated
      - `!supertroopsearch sneaky goblin`

- ## <a id="command-list-war"></a>War

  - war
    - displays war information
    - uses active player's clan for all war commands
  - wartime
    - displays how much time is left in war
  - warnoattack
    - displays players that are missing attacks in war
  - warclanstars
    - overview of all members in war
  - warallattacks
    - shows all attacks for every member
  - warscore
    - shows your member score for war
  - warmemberscore
    - displays the requested member score for war
  - warclanscore
    - displays every war member's score for war
  - warlineup
    - displays a lineup for your clan and your opponent
  - warmemberlineup
    - displays a lineup for each member in your clan and your opponent

- ## <a id="command-list-cwl-group"></a>CWL Group

  - cwllineup
    - displays a lineup for clans in your cwl group
    - uses active player's clan for all cwlgroup and cwlwar commands
  - cwlclanscore
    - displays every cwl member's score
  - cwlscore
    - lists your player's score for each war in cwl
  - cwlmemberscore `mentionuser`
    - lists user's active player's score for each war in cwl

- ## <a id="command-list-cwl-war"></a>CWL War

  - cwlwar
    - displays cwlwar information
  - cwlwartime
    - displays how much time is left in current war
  - cwlwarnoattack
    - displays players that are missing attacks in current war

# <a id="contributing"></a>Contributing

If you would _like_ to contribute to this project please message me on discord _or_ email me. I currently do not have any contribution instruction and will figure that out when the time comes if someone would like to.

# <a id="requirements"></a>Requirements

There aren't many required packages, but here are the few that are required and the versions I am using.

- [discord.py](https://github.com/Rapptz/discord.py)
  - 1.6.0
- requests
  - 2.24.0
- PyMySQL
  - 1.0.2
- [coc.py](https://github.com/mathsman5133/coc.py)
  - Version 2.0.0

# <a id="links-and-contact"></a>Links and Contact

[Official ClashDiscord Server](https://discord.gg/3jcfaa5NYk)

Email: clashdiscord21@gmail.com
