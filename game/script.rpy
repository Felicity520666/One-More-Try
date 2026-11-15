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
image principal = Crop((40, 10, 50, 45), "images/principal.png")

default reputation = 0
default courage = 1
default helped_cleanup = False
default replaced_flyers = False
default streak = 0
default current_speaker = "none"
# Track each speaking character's current stage slot so the white highlight
# follows them when they move between positions.
default speaker_pos = {"alex": 0.12, "mary": 0.36, "janitor": 0.63, "principal": 0.84}
default outfit = "normal"
default mary_action = "hi"
default locker_action = "walk away"
default speaker_color = {
    "alex": "#e5aa7a",
    "mary": "#fdd2de",
    "principal": "#dec3af",
    "janitor": "#ffa3b1",
    "crowd": "#b9d9ff",
}

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

transform speaker_highlight(slot):
    ysize 350
    fit "contain"
    xpos slot
    ypos 0.745
    xanchor 0.5
    yanchor 1.0
    matrixcolor TintMatrix("#ffffff") * BrightnessMatrix(0.15)
    alpha 0.0
    zoom 1.0
    ease 1.0 alpha 0.4
    ease 1.0 alpha 0.1
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
    # White highlight only for a speaker still on stage. Uses the tracked
    # position so it follows the character when they move between slots.
    if current_speaker == "alex" and renpy.showing("alex"):
        add "alex" at speaker_highlight(speaker_pos["alex"])
    elif current_speaker == "mary" and renpy.showing("mary"):
        add "mary" at speaker_highlight(speaker_pos["mary"])
    elif current_speaker == "janitor" and renpy.showing("janitor"):
        add "janitor" at speaker_highlight(speaker_pos["janitor"])
    elif current_speaker == "principal" and renpy.showing("principal"):
        add "principal" at speaker_highlight(speaker_pos["principal"])

    if current_speaker != "none":
        frame at speaker_badge_in:
            xalign 0.025
            yalign 0.04
            xpadding 22
            ypadding 10
            background Solid("#20243be8")
            if current_speaker == "crowd":
                text "STUDENTS" size 25 color "#b9d9ff"
            else:
                text "[current_speaker!u]" size 25 color speaker_color.get(current_speaker, "#ffd95a")

screen reputation_hud():
    zorder 20
    frame:
        xalign 0.98
        yalign 0.035
        xpadding 18
        ypadding 12
        vbox:
            spacing 5
            text "BOUNCE BACK METER" size 26 color "#ffffff"
            bar value StaticValue(reputation + 2, 10) xmaximum 280 ymaximum 20
            text "REP [reputation] / 6   COURAGE [courage]" size 22 color "#dcecff"
            if streak >= 2:
                text "MOMENTUM x[streak]" size 24 color "#ffdf68"
            if reputation >= 6:
                text "STATUS: COMEBACK READY" size 21 color "#80ffad"
            elif reputation >= 3:
                text "STATUS: RISING" size 21 color "#fff28a"
            else:
                text "STATUS: UNDER PRESSURE" size 21 color "#ff9e9e"

label rep_change(amount, message):
    $ reputation += amount
    if amount > 0:
        $ streak += 1
    elif amount < 0:
        $ streak = 0
    if streak == 3:
        $ reputation += 1
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
    $ speaker_pos["principal"] = 0.84
    show janitor at stage_sprite(0.63)
    $ speaker_pos["janitor"] = 0.63
    show mary at stage_sprite(0.36)
    $ speaker_pos["mary"] = 0.36
    show alex at stage_sprite(0.12)
    $ speaker_pos["alex"] = 0.12

    centered "MONDAY — THE FALL"
    a "Okay, deep breath. I'll ask Mary before the first bell."
    m "Hey, Alex. Practicing your speech in the mirror again?"
    a "Would you maybe want to go to the dance with me?"
    m "No. Why would I? Just stop asking."
    crowd "Ooooh!"
    a "Wait... everyone heard that?"

    menu:
        "The hallway is staring. What does Alex do?"
        "Accept her answer":
            $ courage += 1
            call rep_change(1, "+1 Respect")
            a "I understand. Thanks for being honest, Mary."
            m "Whatever. Don't flatter yourself."
        "Pretend it was all a joke":
            call rep_change(-1, "-1 Reputation")
            a "Ha! You thought I was serious?"
            m "You're pathetic. Just own it."
        "Run away before anyone can react":
            $ courage -= 1
            a "I need to get out of here."

    m "Watch your step, klutz."
    hide mary with moveoutleft
    $ current_speaker = "none"
    show alex at alex_bump
    $ speaker_pos["alex"] = 0.49
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

    scene haven_bg_room at background_fit with fade
    show alex at stage_sprite(0.12)
    $ speaker_pos["alex"] = 0.12
    $ current_speaker = "none"
    pause 0.5
    a "Back in my room. I need to think about tomorrow."
    menu:
        "What should Alex focus on before school?"
        "Pick out clean clothes to wear to school.":
            a "I'll wear something neat. Show I care about how I look."
            call rep_change(1, "+1 Effort")
        "Plan how to get to school on time.":
            a "I'll leave early and walk the main road. No more running."
            $ courage += 1
            call rep_change(1, "+1 Punctuality")
        "Just rest and figure it out in the morning.":
            a "I'll deal with it tomorrow. For now, I need sleep."
    menu:
        "What do you wear to school?"
        "Something to cover your face — hat and hoodie.":
            $ outfit = "hoodie"
            a "I'll keep my head down. Hat and hoodie, face covered."
            call rep_change(-1, "-1 Hiding")
        "Something bold — suit and tie.":
            $ outfit = "suit"
            a "Suit and tie. Act like nothing happened."
            call rep_change(1, "+1 Bold")
        "Something normal — bright t shirt and jeans.":
            $ outfit = "normal"
            a "Just a t shirt and jeans. Like any other day."
    hide alex with moveoutleft
    $ current_speaker = "none"

    centered "NEXT DAY"
    scene hallway at background_fit with fade
    show alex at stage_sprite(0.12)
    $ speaker_pos["alex"] = 0.12
    show mary at stage_sprite(0.36)
    $ speaker_pos["mary"] = 0.36
    show janitor at stage_sprite(0.63)
    $ speaker_pos["janitor"] = 0.63
    $ current_speaker = "none"
    pause 0.4
    a "Morning. Time to go to school."

    m "Oh look, it's you."
    menu:
        "There's Mary! What do you do?"
        "Say hi to her.":
            $ mary_action = "hi"
            m "What do you want? Can't you see I'm busy?"
            a "Hey Mary. Good, you?"
            call rep_change(1, "+1 Friendly")
        "Push her":
            $ mary_action = "push"
            m "Whoa! What the hell, Alex?"
            a "Sorry, I didn't mean to—"
            call rep_change(-2, "-2 Reputation")
        "Pretend you don't see her":
            $ mary_action = "ignore"
            m "Figures. Nobody wants to talk to you anyway."
            a "Oh. Hey. Didn't see you there."

    j "Watch where you're going."
    menu:
        "The janitor is cleaning the locker next to yours. What do you do?"
        "Pretend you don't need anything from your locker and walk away":
            $ locker_action = "walk away"
            a "It's fine. I don't need anything right now."
        "Ask him why he was in your way":
            $ locker_action = "ask"
            a "Can you move? I need my stuff."
            j "I'm cleaning. Hold on."
            call rep_change(-1, "-1 Rude")
        "Apologize for what happened yesterday":
            $ locker_action = "apologize"
            a "Hey, about yesterday—sorry I got in your way."
            j "It's alright. Just be more careful."
            call rep_change(1, "+1 Sorry")

    scene hallway at background_fit with dissolve
    show principal at stage_sprite(0.84)
    $ speaker_pos["principal"] = 0.84
    show janitor at stage_sprite(0.63)
    $ speaker_pos["janitor"] = 0.63
    show mary at stage_sprite(0.36)
    $ speaker_pos["mary"] = 0.36
    show alex at stage_sprite(0.12)
    $ speaker_pos["alex"] = 0.12
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

    m "Everyone's still laughing about you. Good luck with that."
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
            m "I'm not your PR person. Deal with it yourself."
        "Laugh along, then thank the people who helped":
            $ courage += 1
            call rep_change(1, "+1 Confidence")
            a "My hallway sprint was spectacularly bad. Thanks for helping me clean it up."
            j "At least your recovery has better balance."

    if helped_cleanup and replaced_flyers:
        call rep_change(1, "+1 Bonus: Kept Every Promise")
        p "You did more than talk. You finished both jobs."

    centered "FRIDAY — THE COMEBACK ASSEMBLY"
    if reputation >= 6 and courage >= 3:
        p "Alex, you turned your worst school day into proof that people can change."
        crowd "Alex! Alex! Alex!"
        j "From public mess to public comeback. Not bad."
        m "Don't expect me to save you."
        a "Bouncing back did not erase Monday. It showed who I chose to be after it."
        centered "BEST ENDING — THE COMEBACK"
    elif reputation >= 3:
        p "Trust does not return all at once, but your actions are moving it forward."
        j "Keep showing up. And keep walking near mop buckets."
        m "It was pathetic. Next."
        a "This is not the end of my comeback. It is the start."
        centered "GOOD ENDING — ONE MORE TRY"
    else:
        p "You cannot bounce back while you are avoiding responsibility."
        j "Tomorrow is another chance—but only if you use it."
        m "You're still a mess. Goodbye."
        a "I cannot undo Monday. But I can make a better choice next time."
        centered "TRY AGAIN ENDING — NOT YET"

    hide screen reputation_hud
    hide screen speaker_effect
    return