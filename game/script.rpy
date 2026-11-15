define a = Character("Alex", color="#e5aa7a")
define m = Character("Mary", color="#fdd2de")
define p = Character("Principal", color="#dec3af")
define j = Character("Janitor", color="#ffa3b1")

transform background_fit:
    xysize (config.screen_width, config.screen_height)
    fit "cover"

transform character_fit:
    xysize (config.screen_width, config.screen_height - gui.textbox_height)
    fit "scale-down"

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene hallway at background_fit with fade
    play music "mickeyscat-summer-pulse-background-music-no-copyright-585183.mp3" 
    show alex at character_fit with moveinleft

    a "{i}Awwwww{/i}! Mary is soooooo CUTE! Yo I gotta ask her out!"

    show mary at character_fit with moveinright

    a "Oh hey Mary! I was just thinking about you!"

    m "Ummmm, really? Okay...?"

    a "So, I was wondering if you wanted to hang out sometime? Like maybe we could go to the movies or something?"

    m "{i}Ewwww{/i}... I DO NOT think I want to hang out with you."

    a "What...? You..."

    m "Sorry bro, but I already have a boyfriend. Gotta go, see ya!"

    hide mary with moveoutleft
 
    m "Ah... OH NO!!! MY LIFE IS RUINED! WAH!"

    show janitor at character_fit with moveinright

    hide alex with moveoutright

    j "Hey, be carful kid!"

    show principal at character_fit with moveinright

    p "Ouch! AHHHHHHH!"

    j "Oh no! PRincipal! Are you still alive?! Quick! Go get a towel!"

    p "YOU! You are in GREAT trouble!"

    m "Oh no..."




    # This ends the game.

    return
