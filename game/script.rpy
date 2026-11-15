init python:
    def speaker_callback(name):
        def callback(event, **kwargs):
            if event == "begin":
                store.current_speaker = name
                renpy.restart_interaction()
        return callback

define a = Character("ALEX", color="#e5aa7a", callback=speaker_callback("alex"))
define m = Character("MARY", color="#fdd2de", callback=speaker_callback("mary"))
define p = Character("PRINCIPAL", color="#dec3af", callback=speaker_callback("principal"))
define j = Character("JANITOR", color="#ffa3b1", callback=speaker_callback("janitor"))
define crowd = Character("STUDENTS", color="#b9d9ff", callback=speaker_callback("crowd"))
define flash = Fade(0.06, 0.0, 0.20, color="#fff6bf")

# Remove the large transparent borders in the original 100x100 PNG files.
image alex = Crop((21, 27, 55, 45), "images/alex.png")
image mary = Crop((23, 26, 53, 51), "images/mary.png")
image janitor = Crop((29, 22, 51, 58), "images/janitor.png")
image principal = Crop((44, 15, 30, 54), "images/principal.png")

default reputation = 0
default courage = 1
default helped_cleanup = False
default replaced_flyers = False
default streak = 0
default current_speaker = "none"

transform background_fit:
    xysize (config.screen_width, config.screen_height)
    fit "cover"

# Every sprite uses the exact same height and floor coordinate.
transform stage_sprite(slot):
    ysize 330
    fit "contain"
    xpos slot
    ypos 0.745
    xanchor 0.5
    yanchor 1.0

transform alex_bump:
    ysize 330
    fit "contain"
    xpos 0.12
    ypos 0.745
    xanchor 0.5
    yanchor 1.0
    ease 0.45 xpos 0.54
    linear 0.08 xpos 0.49

transform reputation_pop:
    alpha 0.0
    yoffset 15
    parallel:
        linear 0.15 alpha 1.0
        pause 0.85
        linear 0.25 alpha 0.0
    parallel:
        linear 1.25 yoffset -35

transform speaker_glow(slot):
    ysize 350
    fit "contain"
    xpos slot
    ypos 0.745
    xanchor 0.5
    yanchor 1.0
    matrixcolor TintMatrix("#ffd95a") * BrightnessMatrix(0.35)
    alpha 0.0
    zoom 1.0
    ease 0.16 alpha 0.72 zoom 1.10 yoffset -8
    ease 0.30 alpha 0.28 zoom 1.04 yoffset 0
    ease 0.55 alpha 0.58 zoom 1.08 yoffset -5
    ease 0.55 alpha 0.28 zoom 1.04 yoffset 0
    repeat

transform speaker_badge_in:
    alpha 0.0
    xoffset -30
    easeout 0.20 alpha 1.0 xoffset 0

transform bounce_word:
    alpha 0.0
    zoom 0.35
    yoffset 120
    easeout 0.35 alpha 1.0 zoom 1.18 yoffset -20
    easein 0.18 zoom 1.0 yoffset 0
    pause 0.8
    ease 0.25 alpha 0.0 yoffset -45

screen speaker_effect():
    zorder 8
    if current_speaker == "alex":
        add "alex" at speaker_glow(0.12)
    elif current_speaker == "mary":
        add "mary" at speaker_glow(0.36)
    elif current_speaker == "janitor":
        add "janitor" at speaker_glow(0.63)
    elif current_speaker == "principal":
        add "principal" at speaker_glow(0.84)

    if current_speaker != "none":
        frame at speaker_badge_in:
            xalign 0.025
            yalign 0.04
            xpadding 22
            ypadding 10
            background Solid("#20243be8")
            if current_speaker == "crowd":
                text "STUDENTS ARE SPEAKING" size 25 color "#b9d9ff"
            else:
                text "[current_speaker!u] IS SPEAKING" size 25 color "#ffd95a"

screen reputation_hud():
    zorder 20
    frame:
        xalign 0.98
        yalign 0.035
        xpadding 18
        ypadding 12
        vbox:
            spacing 5
            text "BOUNCE BACK METER" size 22 color "#ffffff"
            bar value StaticValue(reputation + 2, 10) xmaximum 280 ymaximum 20
            text "REP [reputation] / 6   COURAGE [courage]" size 18 color "#dcecff"
            if streak >= 2:
                text "MOMENTUM x[streak]" size 20 color "#ffdf68"
            if reputation >= 6:
                text "STATUS: COMEBACK READY" size 17 color "#80ffad"
            elif reputation >= 3:
                text "STATUS: RISING" size 17 color "#fff28a"
            else:
                text "STATUS: UNDER PRESSURE" size 17 color "#ff9e9e"

label rep_change(amount, message):
    $ reputation += amount
    if amount > 0:
        $ streak += 1
    elif amount < 0:
        $ streak = 0
    if streak == 3:
        $ reputation += 1
        $ message = message + "  +1 MOMENTUM BONUS"
    show text message at reputation_pop:
        xalign 0.5
        yalign 0.18
    if amount > 0:
        with flash
    elif amount < 0:
        with vpunch
    pause 0.35
    return

label bounce_card(first_line, second_line):
    $ current_speaker = "none"
    show text "{size=54}{color=#ff8e8e}[first_line]{/color}{/size}":
        xalign 0.5
        yalign 0.34
    with vpunch
    pause 0.55
    hide text
    show text "{size=74}{color=#ffd95a}[second_line]{/color}{/size}" at bounce_word:
        xalign 0.5
        yalign 0.34
    pause 1.35
    hide text
    return

label start:
    scene hallway at background_fit with fade
    play music "mickeyscat-summer-pulse-background-music-no-copyright-585183.mp3" fadein 1.0
    show screen reputation_hud
    show screen speaker_effect
    show principal at stage_sprite(0.84)
    show janitor at stage_sprite(0.63)
    show mary at stage_sprite(0.36)
    show alex at stage_sprite(0.12)

    call bounce_card("ONE BAD MOMENT", "CAN BECOME A COMEBACK")
    centered "MONDAY — THE FALL"
    a "Okay, deep breath. I'll ask Mary before the first bell."
    m "Hey, Alex. You look like you are rehearsing something."
    a "Would you maybe want to go to the dance with me?"
    m "Thanks for asking, but I don't feel that way.. I hope we can still be friends."
    crowd "Ooooh!"
    a "Wait... everyone heard that?"

    menu:
        "The hallway is staring. What does Alex do?"
        "Accept her answer":
            $ courage += 1
            call rep_change(1, "+1 Respect")
            a "I understand. Thanks for being honest, Mary."
            m "Thanks for being cool about it."
        "Pretend it was all a joke":
            call rep_change(-1, "-1 Reputation")
            a "Ha! You thought I was serious?"
            m "You do not have to put me down to save face."
        "Run away before anyone can react":
            $ courage -= 1
            a "I need to get out of here."

    m "Alex—watch out for the mop bucket!"
    hide mary with moveoutleft
    show alex at alex_bump
    with vpunch
    with flash
    pause 0.6
    j "Whoa! You hit me—and there goes the bucket!"
    crowd "The water soaked the principal's papers!"
    p "And nearly the whole hallway. Alex, stop running."
    a "The Principal saw it too. This day cannot get worse."
    j "It can if somebody slips. What are you going to do?"

    menu:
        "Alex has only a few seconds to react."
        "Grab the mop and help immediately":
            $ helped_cleanup = True
            call rep_change(2, "+2 Responsibility")
            a "This was my fault. Please show me what to do."
            j "Start at the puddle. Fast."
        "Check that the Janitor is okay first":
            call rep_change(1, "+1 Kindness")
            a "Are you hurt? I hit you pretty hard."
            j "I am okay. Now help me keep everyone else safe."
        "Blame the bucket for blocking the hall":
            call rep_change(-2, "-2 Reputation")
            a "Why was that bucket even there?"
            j "It had a warning sign. Your eyes were on the crowd."
            p "Mistakes happen. Blame is a choice."

    scene hallway at background_fit with dissolve
    show principal at stage_sprite(0.84)
    show janitor at stage_sprite(0.63)
    show mary at stage_sprite(0.36)
    show alex at stage_sprite(0.12)
    call bounce_card("FALL DOWN", "BOUNCE BACK")
    centered "TUESDAY — THE BOUNCE BACK"
    p "Yesterday was embarrassing. But reputation is not one bad moment. It is what you do next."

    menu:
        "Before school, Alex chooses one promise to keep."
        "Replace every ruined assembly flyer":
            $ replaced_flyers = True
            call rep_change(2, "+2 Follow-through")
            p "You came early, remade them, and hung them yourself. Well done."
        "Finish cleaning with the Janitor":
            $ helped_cleanup = True
            call rep_change(2, "+2 Teamwork")
            j "You showed up before I even asked. That is how trust comes back."
        "Post a dramatic apology to the whole school":
            call rep_change(0, "No change")
            crowd "Why is Alex making this even bigger?"
            p "A performance is not the same as repairing the harm."

    m "People are still joking about yesterday. How will you face them?"
    menu:
        "Choose how Alex faces the crowd."
        "Own the embarrassing story and move forward":
            $ courage += 2
            call rep_change(2, "+2 Courage")
            a "Yes, I got rejected. Yes, I hit a mop bucket. I survived both—and fixed the mess."
            crowd "Okay... fair enough."
        "Ask Mary to defend him":
            call rep_change(-1, "-1 Reputation")
            a "Could you tell everyone I am not a loser?"
            m "I can correct lies, but your reputation has to come from your choices."
        "Laugh along, then thank the people who helped":
            $ courage += 1
            call rep_change(1, "+1 Confidence")
            a "My hallway sprint was spectacularly bad. Thanks for helping me clean it up."
            j "At least your recovery has better balance."

    if helped_cleanup and replaced_flyers:
        call rep_change(1, "+1 Bonus: Kept Every Promise")
        p "You did more than talk. You finished both jobs."

    call bounce_card("YOUR PAST IS NOT YOUR SCORE", "YOUR NEXT MOVE IS")
    centered "FRIDAY — THE COMEBACK ASSEMBLY"
    if reputation >= 6 and courage >= 3:
        p "Alex, you turned your worst school day into proof that people can change."
        crowd "Alex! Alex! Alex!"
        j "From public mess to public comeback. Not bad."
        m "You respected my answer and yourself. I am proud to be your friend."
        a "Bouncing back did not erase Monday. It showed who I chose to be after it."
        centered "BEST ENDING — THE COMEBACK"
    elif reputation >= 3:
        p "Trust does not return all at once, but your actions are moving it forward."
        j "Keep showing up. And keep walking near mop buckets."
        m "One awkward moment does not define you, Alex."
        a "This is not the end of my comeback. It is the start."
        centered "GOOD ENDING — ONE MORE TRY"
    else:
        p "You cannot bounce back while you are avoiding responsibility."
        j "Tomorrow is another chance—but only if you use it."
        m "Be honest, make amends, and try again."
        a "I cannot undo Monday. But I can make a better choice next time."
        centered "TRY AGAIN ENDING — NOT YET"

    hide screen reputation_hud
    hide screen speaker_effect
    return
