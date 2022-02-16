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
  - [CWL](#command-list-cwl)
- [Contributing](#contributing)
- [Requirements](#requirements)
- [Links and Contact](#links-and-contact)

# <a id="introduction"></a>Introduction

ClashDiscord is a discord bot written in Python that, while having a great many uses and commands, focuses _primarily_ on discord member management. This entails, but is not limited to, adding an uninitiated role to incoming members, allowing members to give themselves roles based on their clash of clans profile, and focusing on discord server security.

Non-management commands include, but are also not limited to, returning player or clan information based on their tag, getting troop levels and how close they are to max for their town hall as well as total max, who can donate the best of a specific troop in a clan, war information, cwl lineup, cwl war, and cwl clan member scores.

# <a id="setup"></a>Setup

Getting ClashDiscord set up in your discord server can be somewhat confusing, but never fear for I am here.

1. invite ClashDiscord to your discord server

   - [invite link](https://discord.com/api/oauth2/authorize?client_id=649107156989378571&permissions=1239433964608&scope=bot%20applications.commands)

2. claim your user in ClashDiscord

   - `client user` `claim`
     - this will claim you as a user

3. claim your discord server

   - `client guild` `claim`
     - this will claim your discord server and add you as the guild admin within ClashDiscord
      - _guild is what the discord API calls a server_

4. link a player to your user

   - `client player` `claim` `player tag` `api key`
     - claims the requested player and links it to your discord user
     - _getting your api key is annoying, but for everyone’s security this is necessary_

5. link a clan to your guild

    - `client clan` `claim` `clan tag`
      - claims a clan and links it to the claimed guild
      - a linked player **must** be in the clan
        - _this is also for security_

6. link existing roles to your server

    A. claim clan roles
      - `client clanrole` `claim` `clan tag` `role mention`
        - links the clan role to a claimed clan

    B. claim rank roles

      - `client rankrole` `claim` `rank name` `role mention`
        - links the rank role to a discord role
          - leader
          - co-leader
          - elder
          - member
          - uninitiated
            - _this means they aren't verified or they aren't in a claimed clan_

7. Use ClashDiscord, you are set up!

# <a id="setup-summary"></a>Setup Summary

- invite Clash Discord to your server
- claim your discord user
- claim the guild
- claim your player
- claim your clan
- claim the necessary roles

# <a id="usage"></a>Usage

ClashDiscord is largely **command** focused, meaning it doesn't do anything that it is not told to do. The only exception to this is when a member joins. If a server has claimed an uninitiated role, then they will be given that role, otherwise nothing will happen. The other action ClashDiscord will take is if it detects a role being deleted from discord it will delete the database instance of that role.

Once setup is complete you will be able to interact with ClashDiscord using the prefix `/` and run the commands as desired.

# <a id="command-list"></a>Command List

- ## <a id="command-list-clashdiscord"></a>ClashDiscord

  - client info
    - overview for the client

  - client user
    - claims the user by discord user id within ClashDiscord

  - client player
    - _client player options_
      - options for `client player` command
      - `claim` - links a specified player to your user
        - _values needed_ - `player tag` `api key`
      - `show` _default_ - return all claimed players
      - `update` - updates the requested player as your active player
        - _values needed_ - `player tag`
      - `remove` - removes the linked player from your user
        - _values needed_ - `player tag`

  - client guild
    - claims the guild by discord guild id within ClashDiscord
    - _sets the user who called the command as the guild admin within ClashDiscord_
      - _if the guild has already been claimed, then nothing will happen_

  - client clan
    - _client clan options_
      - options for `client clan` command
      - `claim` - links a specified clan to your guild
        - _values needed_ - `clan tag`
      - `show` _default_ - return all claimed clans
      - `remove` - removes the linked clan from your guild
        - _values needed_ - `clan tag`

  - client role
    - _client role options_
      - options for `client role` command
      - `show` _default_ - return all linked roles
      - `remove` - removes claim on the mentioned role
        - _values needed_ - `role mention`

  - client clanrole
    - _client clanrole options_
      - options for `client clanrole` command
      - `claim` - links a specified clanrole the specified guild's claimed clan
        - _values needed_ - `role mention` `clan tag`

  - client rankrole
    - _client rankrole options_
      - options for `client rankrole` command
      - `claim` - links a specified rankrole the specified Clash of Clans rank
        - _values needed_ - `role mention` `rank name`
        - _rank names_
          - leader
          - co-leader
          - elder
          - member
          - uninitiated
            - _this means they aren't verified or they aren't in a claimed clan_

- ## <a id="command-list-discord"></a>Discord

  - discord help
    - displays relevant help-text regarding what commands can be run
    - react to the help message to parse through command groups

  - discord announce message `channel` `message`
    - announces message to specified channel
    - *restricted to leaders and co-leaders*

  - discord announce player `channel` `message` `player tag`
    - announces message to specified channel, pings the requested player's user
    - *restricted to leaders and co-leaders*

  - discord announce donate `channel` `message` `unit name`
    - announces message to specified channel, pings all users that can donate the requested
    - _discord announce donate options_
      - options for `discord announce donate` command
        - `clan_role` - mention a role linked to a clan to get that clan's information
          - _if no clan role is specified, then the user's active player's clan will be used_

  - discord announce supertroop `channel` `message` `super troop name`
    - announces message to specified channel, pings all users that have the requested super troop active
    - _discord announce supertroop options_
      - options for `discord announce supertroop` command
        - `clan_role` - mention a role linked to a clan to get that clan's information
          - _if no clan role is specified, then the user's active player's clan will be used_

  - discord announce war `channel` `message`
    - announces message to specified channel, pings all in current war
    - *restricted to leaders and co-leaders*
    - _discord announce war options_
      - options for `discord announce war` command
        - `clan_role` - mention a role linked to a clan to get that clan's information
          - _if no clan role is specified, then the user's active player's clan will be used_
        - `cwl_war_selection` - *only for cwl* specify whether to look for the previous, current, or upcoming war
          - _defaults to current_

  - discord announce warnoatk `channel` `message`
    - announces message to channel, pings all in war missing attacks
    - *restricted to leaders and co-leaders*
    - _discord announce warnoattack options_
      - options for `discord announce warnoattack` command
        - `clan_role` - mention a role linked to a clan to get that clan's information
          - _if no clan role is specified, then the user's active player's clan will be used_
        - `missed_attacks` - returns players who missed exactly the specified missed attack count
          - _if not specified, then it will simply return all who are or have missed attacks_
        - `cwl_war_selection` - *only for cwl* specify whether to look for the previous, current, or upcoming war
          - _defaults to current_

  - discord role me
    - update your roles

  - discord role member `membermention`
    - update mentioned user's roles
    - *restricted to leaders and co-leaders*

  - discord role all
    - update roles for every member in the server
    - *restricted to ClashDiscord server admin*

  - discord emoji `coc_name`
    - sends specified emoji

  - discord user
    - returns the user linked to a requested player
    - _discord user options_
      - options for `discord user` command
      - `player` - finding the linked user to the specified player
        - _player tag must be specified_
      - `clan` _default_ - finding the linked user for each member in the clan
        - *restricted to leaders and co-leaders*
        - _if no clan role is specified, then the user's active player's clan will be used_

- ## <a id="command-list-player"></a>Player

  - ### _player options_
    - options for player commands
    - `user` - mention a user to get their active player's information
      - _if no user is specified, then the user's active player will be used_
    - `tag` - specify a player's tag for that player's information
      - _if no tag is specified, then the user's active player will be used_

  - player info
    - shows player information based on your active player

  - player recruit
    - displays player recruit information for requested player tag
    
  - player unit all
    - shows the level your units based on the specified type

  - player unit find `unit name`
    - shows the level, town hall max, and overall max levels for the requested unit
    - you can search troops, spells, and heroes
    - example
      - `/player unit find hog rider`
      - `/player unit find jump spell`
      - `/player unit find archer queen`

  - player supertroop
    - shows the super troops you have active

- ## <a id="command-list-clan"></a>Clan

  - ### _clan options_
    - options for clan commands
    - `clan_role` - mention a role linked to a clan to get that clan's information
      - _if no clan role is specified, then the user's active player's clan will be used_
    - `tag` - specify a clan's tag for that clan's information
      - _if no tag is specified, then the user's active player's clan will be used_

  - clan info
    - displays clan information

  - clan lineup
    - displays clan town hall lineup
    - *restricted to leaders and co-leaders*
    - _clan lineup options_
      - options for `clan lineup` command
      - `overview` _default_ - returns an overview of the clan's town hall lineup
      - `member` - returns each member of the clan and their town hall and their hero levels

  - clan warpreference
    - displays rundown of clan member's war preference
    - *restricted to leaders and co-leaders*
    - _clan warpreference options_
      - options for `clan warpreference` command
      - `overview` _default_ - returns an overview of the clan's war preference
      - `member` - returns each member of the clan and their war preference

  - clan donate `unit name`
    - search the clan for available donors for a specified unit
    - _examples_
      - `/clan donate hog rider`
      - `/clan donate freeze spell`

  - clan supertroop
    - shows all active super troops in the clan
    - _clan supertroop option_
      - option for `clan supertroop` command
      - `super_troop` - if a super troop is specified, then it will search the clan and show who has the specified super troop active

- ## <a id="command-list-war"></a>War

  - ### _war options_
    - options for war commands
    - `clan_role` - mention a role linked to a clan to get that clan's war information
      - _if no clan role is specified, then the user's active player's clan will be used_
    - `cwl_war_selection` - *only for cwl* specify whether to look for the previous, current, or upcoming war
      - _defaults to current_

  - war info
    - displays war information

  - war noattack
    - lists players that missed attacks in war
    - _war noattack option_
      - option for `war noattack` command
      - `missed_attacks` - returns players who missed exactly the specified missed attack count
        - _if not specified, then it will simply return all who are or have missed attacks_

  - war stars
    - show all war members and their stars
    - *restricted to leaders and co-leaders*
    - _war stars options_
      - options for `war stars` command
      - `stars` _default_ - returns all war members and their stars
      - `member` - show all war members and their attacks

  - war score user
    - user's active player's war score
    - _war score user option_
      - option for `war score user` command
      - `user` - returns the mentioned user's active player's war score
        - _if not specified, then it will return the author's active player's war score_

  - war score clan
    - every clan member's war score
    - *restricted to leaders and co-leaders*

  - war lineup
    - war town hall lineup
    - _war lineup options_
      - options for `war lineup` command
      - `overview` - short overview of the war's lineup
      - `clan` _default_ - war lineup for each clan
      - `member` - lineup for every member in war

- ## <a id="command-list-cwl"></a>CWL

  - ### _cwl options_
    - options for cwl commands
    - `clan_role` - mention a role linked to a clan to get that clan's cwl information
      - _if no clan role is specified, then the user's active player's clan will be used_

  - cwl lineup
    - CWL town hall lineup
    - _cwl lineup options_
      - options for `cwl lineup` command
      - `overview` - short overview of the cwl's lineup
      - `clan` _default_ - cwl lineup for each clan
      - `member` - lineup for every member in each clan in cwl

  - cwl score user
    - user's active player's cwl score
    - _cwl score user option_
      - option for `cwl score user` command
      - `user` - returns the mentioned user's active player's cwl score
        - _if not specified, then it will return the author's active player's cwl score_

  - cwl score clan
    - every clan member's cwl score
    - *restricted to leaders and co-leaders*

# <a id="contributing"></a>Contributing

If you would _like_ to contribute to this project please message me on discord _or_ email me. I currently do not have any contribution instruction and will figure that out when the time comes if someone would like to.

# <a id="requirements"></a>Requirements

There aren't many required packages, but here are the few that are required and the versions I am using.

- [disnake](https://github.com/DisnakeDev/disnake)
  - 2.3.2
- [coc.py](https://github.com/mathsman5133/coc.py)
  - 2.0.0
- PyMySQL
  - 1.0.2

# <a id="links-and-contact"></a>Links and Contact

[Official ClashDiscord Server](https://discord.gg/3jcfaa5NYk)

Email: clashdiscord21@gmail.com
