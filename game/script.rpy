define a = Character("Alex", color="#e5aa7a")
define m = Character("Mary", color="#fdd2de")
define p = Character("Principal", color="#dec3af")
define j = Character("Janitor", color="#ffa3b1")

transform background_fit:
    xysize (config.screen_width, config.screen_height)
    fit "contain"
    xalign 0.5
    yalign 0.5

transform character_fit:
    ysize (config.screen_height - gui.textbox_height)
    fit "contain"
    ypos (config.screen_height - gui.textbox_height)
    yanchor 1.0

transform stage_left:
    xalign 0.20

transform stage_right:
    xalign 0.42

transform stage_janitor:
    xalign 0.72

transform stage_principal:
    xalign 0.92

transform alex_bump:
    ysize (config.screen_height - gui.textbox_height)
    fit "contain"
    ypos (config.screen_height - gui.textbox_height)
    yanchor 1.0
    xalign 0.20
    linear 0.55 xalign 0.72
    linear 0.08 xalign 0.66

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene hallway with fade
    play music "mickeyscat-summer-pulse-background-music-no-copyright-585183.mp3" 
    show janitor at character_fit, stage_janitor
    show principal at character_fit, stage_principal
    show alex at character_fit, stage_left with moveinleft

    a "{i}Awwwww{/i}! Mary is soooooo CUTE! Yo I gotta ask her out!"

    show mary at character_fit, stage_right with moveinright

    a "Oh hey Mary! I was just thinking about you!"

    m "Ummmm, really? Okay...?"

    a "So, I was wondering if you wanted to hang out sometime? Like maybe we could go to the movies or something?"

    m "{i}Ewwww{/i}... I DO NOT think I want to hang out with you."

    a "What...? You..."

    m "Sorry bro, but I already have a boyfriend. Gotta go, see ya!"

    hide mary with moveoutleft
 
    m "Ah... OH NO!!! MY LIFE IS RUINED! WAH!"

    show alex at alex_bump with vpunch
    pause 0.65

    j "Hey, be careful, kid!"

    p "Alex! Watch where you're going!"

    j "I'm okay, Principal. Alex ran right into me!"

    p "YOU! You are in GREAT trouble!"

    m "Oh no..."




    # This ends the game.

    return