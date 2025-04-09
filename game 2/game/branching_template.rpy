init python:
    import json
    import os
    import random

    # Load the JSON file with decisions data
    decisions_file_path = os.path.join(renpy.config.basedir, "game", "decisions.json")
    with open(decisions_file_path, "r") as f:
        decisions = json.load(f)

    # Function to pick 3 random options, at least one positive
    def pick_options(decision_options):
        positive_options = [opt for opt in decision_options if any(isinstance(val, (int, float)) and val > 0 for val in opt['variable_changes'].values())]
        if len(positive_options) < 1:
            raise ValueError("No positive options available.")

        selected_options = random.sample(positive_options, 1)
        remaining_options = [opt for opt in decision_options if opt not in selected_options]
        selected_options += random.sample(remaining_options, 2)

        return selected_options

# Define characters
init python:
    intro = decisions['intro']
    main_user = intro['main_user']
    main_user_character = Character(main_user, color="#FFFFFF", image=main_user.lower(), position=(0.8, 1.0))
    character_names = ["Anika", "Charlotte", "Daniel", "Eva", "Fatima", "Jack", "Li", "Lucas", "Maya", "Nora", "Sophia", "Talia", "Yuki", "Marcus", "Sarah", "Raj", "Priya","Elena" "Amir", "Jordan"]
    characters = {name: Character(name, color="#FFFFFF", image=name.lower(), position=(0.2, 1.0)) for name in character_names}
    characters[main_user] = main_user_character
    globals().update(characters)

# Define images
image bg meeting_room = "bg_meeting_room.png"
image bg office = "bg_office.png"

# Initialize variables globally - Updated for AI Categories & Use Cases
define decision_points = 0
define bias_reduction_effectiveness = 0
define model_performance_impacy = 0
define ethical_oversight_transparancy = 0
define summary_outcomes = []

# Remove bottom navigation
init python:
    config.overlay_screens = []

# Branching simulation structure
label start:

    # Initialize and Reset variables to track decisions - Updated for AI Categories & Use Cases
    $ decision_points = 0
    $ bias_reduction_effectiveness = 0
    $ model_performance_impacy = 0
    $ ethical_oversight_transparancy = 0
    $ summary_outcomes = []
    $ selected_options = []

    scene bg office
    $ main_user_emotion = intro['user_emotion']
    $ main_speaker_emotion = intro['speaker_emotion']
    
    $ main_user_image = f"{main_user.lower()} {main_user_emotion}"
    $ main_speaker_image = f"{intro['main_speaker'].lower()} {main_speaker_emotion}"
    $ renpy.show(main_user_image, at_list=[right])
    with dissolve
    $ renpy.show(main_speaker_image, at_list=[left])
    with dissolve

    "[intro['description']]"

    $ decision_num = 1
    call decision_loop from _call_decision_loop

label decision_loop:
    $ character_name = None
    $ decision_key = f"decision_{decision_num}"
    if decision_key not in decisions:
        jump end_simulation

    $ decision = decisions[decision_key]
    $ selected_options = pick_options(decision["options"])

    # Hide previous speaker's image
    if character_name:
        $ renpy.hide(character_name)
        with dissolve

    # Show character at decision point
    $ character_name = decision["speaker"]
    $ emotion = decision.get("speaker_emotion", "neutral")
    $ image_name = f"{character_name.lower()} {emotion}"
    $ renpy.show(image_name, at_list=[left])
    with dissolve

    # Display decision description above the menu
    "[decision['description']]"

    # Create the menu with the generated choices
    menu:
        "[selected_options[0]['option']]":
            $ index = 0
        "[selected_options[1]['option']]":
            $ index = 1
        "[selected_options[2]['option']]":
            $ index = 2

    $ decision_points += 1
    $ bias_reduction_effectiveness += selected_options[index].get('variable_changes', {}).get('bias_reduction_effectiveness', 0)
    $ model_performance_impacy += selected_options[index].get('variable_changes', {}).get('model_performance_impacy', 0)
    $ ethical_oversight_transparancy += selected_options[index].get('variable_changes', {}).get('ethical_oversight_transparancy', 0)
    $ summary_outcomes.append(selected_options[index].get('variable_changes', {}).get('rationale', ''))
    $ user_emotion = selected_options[index].get('user_emotion', 'confidence')
    $ speaker_emotion = selected_options[index].get('speaker_emotion', 'confidence')

    # Update the emotions for both characters
    $ main_user_image = f"{main_user.lower()} {user_emotion}"
    $ main_speaker_image = f"{character_name.lower()} {speaker_emotion}"
    $ renpy.show(main_user_image, at_list=[right])
    with dissolve
    $ renpy.show(main_speaker_image, at_list=[left])
    with dissolve

    # Show feedback
    $ renpy.say(characters[character_name], selected_options[index]['feedback'])
    $ renpy.hide(character_name.lower())
    with dissolve

    $ decision_num += 1
    jump decision_loop

label end_simulation:
    # Calculate Red, Amber, Green status for variables - Updated for AI Categories & Use Cases
    $ category_status = "Red" if bias_reduction_effectiveness < 0 else "Amber" if bias_reduction_effectiveness == 0 else "Green"
    $ application_status = "Red" if model_performance_impacy < 0 else "Amber" if model_performance_impacy == 0 else "Green"
    $ allocation_status = "Red" if ethical_oversight_transparancy < 0 else "Amber" if ethical_oversight_transparancy == 0 else "Green"

    # Show the summary screen with updated variables
    show screen summary_screen(category_status, bias_reduction_effectiveness, application_status, model_performance_impacy, allocation_status, ethical_oversight_transparancy, summary_outcomes)

    # Pause for user to interact with the summary page
    pause

    return

screen summary_screen(category_status, bias_reduction_effectiveness, application_status, model_performance_impacy, allocation_status, ethical_oversight_transparancy, summary_outcomes):
    tag summary

    # Define the size of the summary box to avoid overlap
    frame:
        style_prefix "summary"
        ymaximum 1200  # Set maximum height for the frame to avoid overlap with footer
        viewport:
            draggable True
            scrollbars "vertical"
            mousewheel True

            vbox:
                spacing 70
                text "Project Summary" size 40

                # Table-like grid layout - Updated variable names for AI Categories & Use Cases
                grid 3 4:
                    spacing 20
                    xpos 0.05

                    # Header row
                    text "Metric" bold True xalign 0.0
                    text "Status" bold True xalign 0.5
                    text "Value" bold True xalign 0.5

                    # Data row 1 - Updated for AI Category Differentiation
                    text "AI Category Differentiation" xalign 0.0
                    text "[category_status]" color ("#ff0000" if category_status == "Red" else "#ffa500" if category_status == "Amber" else "#008000") xalign 0.5
                    text "[bias_reduction_effectiveness]" xalign 0.5

                    # Data row 2 - Updated for Business Application Analysis
                    text "Business Application Analysis" xalign 0.0
                    text "[application_status]" color ("#ff0000" if application_status == "Red" else "#ffa500" if application_status == "Amber" else "#008000") xalign 0.5
                    text "[model_performance_impacy]" xalign 0.5

                    # Data row 3 - Updated for Human-AI Task Allocation
                    text "Human-AI Task Allocation" xalign 0.0
                    text "[allocation_status]" color ("#ff0000" if allocation_status == "Red" else "#ffa500" if allocation_status == "Amber" else "#008000") xalign 0.5
                    text "[ethical_oversight_transparancy]" xalign 0.5

                # Summary of outcomes
                vbox:
                    spacing 20
                    xpos 0.05
                    xmaximum 1700  
                    xfill True 
                    text "Summary of Outcomes" size 30 bold True
                    for outcome in summary_outcomes:
                        text outcome

                # Add buttons and center them
                hbox:
                    spacing 100
                    xalign 0.5

                    textbutton "Restart Simulation" action [
                        Hide('summary'), 
                        SetVariable('decision_points', 0), 
                        SetVariable('bias_reduction_effectiveness', 0), 
                        SetVariable('model_performance_impacy', 0), 
                        SetVariable('ethical_oversight_transparancy', 0), 
                        SetVariable('summary_outcomes', []), 
                        Jump('start')
                    ]
                    textbutton "Quit" action Quit()

    key "mousedown_4" action None  # Disable mousewheel scroll-up from advancing the game
    key "mousedown_5" action None  # Disable mousewheel scroll-down from advancing the game