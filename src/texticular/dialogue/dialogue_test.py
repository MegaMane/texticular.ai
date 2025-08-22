# https://github.com/JonathanMurray/dialog-tree-py

import time

from dialogue_graph import DialogueGraph, DialogueNode, DialogueChoice
from text_util import layout_text_in_area


def main():
    dialog_graph = DialogueGraph(
        root_node_id="START",
        nodes=[
            DialogueNode(
                node_id="START",
                text="Nigel: Hello sir, you seem a bit flustered. How can I help you?",
                choices=[DialogueChoice("I'm looking for some toilet paper", "CERTAINLY"),
                         DialogueChoice("Dude, I'm going to shit myself, give me some fucking toilet paper!", "SECURITY")]),
            DialogueNode(
                node_id="CERTAINLY",
                text="Nigel: Certainly sir, that will be $49.99 would you like to pay with cash or credit?",
                choices=[DialogueChoice("Can't I just bill it to my room?", "DENY"),
                         DialogueChoice("49.99!!! Are you out of your mind!?", "CONFIRM"),
                         DialogueChoice("Sure, just take it all. Sweet Jesus, I gotta go!", "VICTORY")]),
            DialogueNode(
                node_id="CONFIRM",
                text="Nigel: Sir, I assure you I am of sound mind and that is indeed the price. Still interested?",
                choices=[DialogueChoice("Sigh...Yes", "CERTAINLY"),
                         DialogueChoice("Nevermind", "EXIT"),
                        ]),
            DialogueNode(
                node_id="SECURITY",
                text="Nigel: OH, it seems one of the vagrants has made their way into the lobby again. Security!",
                choices=[DialogueChoice("You know what, this was just a misundersatning, I'll hold it.", "EXIT"),
                         DialogueChoice("Punch the security guard in the face.", "DEFEAT"),
                        ]), 
            DialogueNode(
                node_id="DENY",
                text="Nigel: I apologize for the inconvenience, but that is something we only extend to our V.I.P. guests,\
                      and you sir do not appear to be on the list. unfortanately...[whispers] (for you) [chuckles smugly to himself]",
                choices=[DialogueChoice("You son of a bitch! I'll murder you!", "SECURITY"),
                         DialogueChoice("Ok then, about that toilet paper...", "CERTAINLY"),
                        ]),
            DialogueNode(
                node_id="DEFEAT",
                text="You angrily swing at the security guard but he dodges easily and returns the favor\
                      with a brutal punch to the gut and then throws you out the door. You're hurtin' and you\
                      realize something smells... a lot like poop. This isn't your day.",
                choices=[DialogueChoice("Retry", "START"),
                         DialogueChoice("Exit game", "EXIT")]),
            DialogueNode(
                node_id="VICTORY",
                text="Hooray, it cost you your 401k but you've got that sweet sweet TP for your bung hole!",
                choices=[DialogueChoice("Start from beginning", "START"),
                         DialogueChoice("Exit game", "EXIT")]),
            DialogueNode(
                node_id="EXIT",
                text="Nigel: Take Care now sir.",
                choices=[]),
        ],
        title="Conversation with Hotel Clerk"
    )

    print("")
    print_in_box(dialog_graph.title, 50)
    print("")



    while True:

        node = dialog_graph.current_node()

        if node.node_id == "EXIT":
            if node.text:
                print("")
                print_in_box(node.text, 50)
                print("")               
            break

        print("")
        print_in_box(node.text, 50)
        print("")

        time.sleep(0.5)

        print("Select one of these choices:")
        for i, choice in enumerate(node.choices):
            time.sleep(0.15)
            print(f"{i} : {choice.text}")

        choice = -1
        valid_choices = range(len(node.choices))
        while choice not in valid_choices:
            text_input = input("> ")
            try:
                choice = int(text_input)
                if choice not in valid_choices:
                    print("Invalid choice. Select one of the listed numbers!")
            except ValueError:
                print("Invalid input. Type a number!")

        print(f"\"{node.choices[choice].text.upper()}\"")
        time.sleep(0.5)

        dialog_graph.make_choice(choice)


def print_in_box(text: str, line_width):
    lines = layout_text_in_area(text, len, line_width)
    print("+" + "-" * (line_width + 2) + "+")
    for line in lines:
        time.sleep(0.03)
        print("| " + line.ljust(line_width + 1, " ") + "|")
    time.sleep(0.03)
    print("+" + "-" * (line_width + 2) + "+")


if __name__ == '__main__':
    main()
