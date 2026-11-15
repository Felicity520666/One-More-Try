define a = Character("Alex", color="#e5aa7a")
define m = Character("Mary", color="#fdd2de")
define p = Character("Principal", color="#dec3af")
define j = Character("Janitor", color="#ffa3b1")

default reputation = 0

transform background_fit:
    xysize (config.screen_width, config.screen_height)
    fit "contain"
    xalign 0.5
    yalign 0.5

transform character_fit:
    ysize (config.screen_height - gui.textbox_height) * 0.82
    fit "contain"
    ypos (config.screen_height - gui.textbox_height)
    yanchor 1.0

transform stage_left:
    xalign 0.14

transform stage_right:
    xalign 0.37

transform stage_janitor:
    xalign 0.62

transform stage_principal:
    xalign 0.88

transform principal_fit:
    ysize config.screen_height - gui.textbox_height
    fit "contain"
    ypos (config.screen_height - gui.textbox_height)
    yanchor 1.0

transform alex_bump:
    ysize (config.screen_height - gui.textbox_height) * 0.82
    fit "contain"
    ypos (config.screen_height - gui.textbox_height)
    yanchor 1.0
    xalign 0.14
    linear 0.55 xalign 0.62
    linear 0.08 xalign 0.56

label start:
    scene hallway at background_fit with fade
    play music "mickeyscat-summer-pulse-background-music-no-copyright-585183.mp3"

    show principal at principal_fit, stage_principal
    show janitor at character_fit, stage_janitor
    show mary at character_fit, stage_right
    show alex at character_fit, stage_left

    a "Okay, Alex. Deep breath. Today is the day you ask Mary to hang out."
    m "Hey, Alex. You look like you're rehearsing something."
    a "Would you maybe want to go to the movies with me sometime?"
    m "Thanks for asking, but I'm not interested in dating. I hope we can still be friends."
    a "Oh. Yeah. Of course. Sorry if I made that awkward."

    m "It's okay. I'm heading to class. Watch out for the mop bucket!"
    hide mary with moveoutleft

    a "I can still fix this day. I'll just step around..."
    show alex at alex_bump with vpunch
    pause 0.65

    j "Whoa! You bumped right into me! The bucket's gone over!"
    p "I rushed over to help and slipped in the water. My ankle's sore, and those assembly flyers are soaked!"
    a "I'm so sorry! I was embarrassed and didn't watch where I was going."
    j "That explains the sprint. It doesn't explain the mop water on my shoes."
    p "We'll sort this out tomorrow. For now, let's get the floor dry before someone else slips."

    show mary at character_fit, stage_right with moveinleft
    m "I saw what happened. Are you all right?"
    a "Yeah. I caused a mess, though. I'll make it right tomorrow."
    m "Good. And just so we're clear, I meant what I said about being friends."
    a "I understand. Friends is good."

    scene hallway at background_fit with dissolve
    show principal at principal_fit, stage_principal
    show janitor at character_fit, stage_janitor
    show mary at character_fit, stage_right
    show alex at character_fit, stage_left

    p "The floor is dry, my ankle is better, and most of the flyers survived. Now, Alex, what will you do to bounce back?"

    menu:
        "How does Alex start rebuilding trust?"
        "Apologize to the Janitor and Principal":
            $ reputation += 2
            a "I panicked yesterday. I'm sorry I ran into you both."
            j "Thanks for saying it straight."
            p "Taking responsibility is a solid first step."
        "Offer to help with the cleanup and flyers":
            $ reputation += 2
            a "Let me help replace the flyers and finish cleaning the hallway."
            j "I could use an extra pair of hands."
            p "And I could use someone who can keep the new flyers dry."
        "Make a big, dramatic apology speech":
            $ reputation += 1
            a "Attention, hallway! I have learned that mop buckets are not stepping stones!"
            j "That's... not quite an apology, but at least it's honest."
            p "Try speaking to the people you actually hurt, Alex."

    menu:
        "What's Alex's next move?"
        "Help the Janitor finish the hallway":
            $ reputation += 2
            a "I'll take the mop. You can show me where I missed a spot."
            j "Now you're getting the hang of it."
        "Ask the Principal how to replace the damaged flyers":
            $ reputation += 2
            a "I can't undo the spill, but I can help remake the flyers."
            p "That's the kind of follow-through I was hoping to see."
        "Avoid everyone and hope they forget":
            $ reputation -= 1
            a "Maybe if I keep my head down, nobody will bring it up."
            m "People remember what you do next, Alex. Hiding won't fix yesterday."

    m "You handled an awkward day better than you handled the hallway. That's progress."
    a "I'm learning that bouncing back isn't pretending nothing happened. It's what I do after."

    if reputation >= 4:
        p "You owned the mistake and followed through. You've earned back a lot of trust."
        j "And you are officially allowed near the mop bucket again. Supervised."
        m "I'm glad we're friends, Alex."
        a "I'll take it."
    elif reputation >= 2:
        p "This is a good start. Keep showing people they can count on you."
        j "Next time, try walking around the bucket."
        a "Deal."
    else:
        p "You still have work to do, Alex. Tomorrow is another chance to show up."
        j "Start with a sincere apology and we'll go from there."
        a "I will. No shortcuts this time."

    return
    




