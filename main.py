from bs4 import BeautifulSoup
import os

file_in = "bpmn_ejemplo/bpmn.bpmn"
file_out = "BPMN_TO_XAML/salida.xaml"

# Create the directory for output if it doesn't exist
directory = os.path.dirname(file_out)
if not os.path.exists(directory):
    os.makedirs(directory)

# Create the output file if it doesn't exist
if not os.path.exists(file_out):
    # Copy template into output file
    with open("out_template.xaml", "r") as template:
        content = template.read()
    with open(file_out, "w") as out:
        out.write(content)


# Parse input bpmn file
soup_in = BeautifulSoup(open(file_in), features="xml")
sequence_in = soup_in.find("bpmn:process")

# Parse output file
soup_openrpa = BeautifulSoup(open(file_out), features="xml")

if sequence_in:
    # Add sequence to output file
    soup_openrpa.find("Activity").append(soup_openrpa.new_tag("Sequence"))
    sequence_out = soup_openrpa.find("Sequence")

    for element in sequence_in.children:
        if element.name == "exclusiveGateway":
            pass
        elif element.name == "task":
            activities = element.find("bpmn:extensionElements")
            for activity in activities.children:
                if activity.name == "clickEvent":
                    click_activity = soup_openrpa.new_tag(
                        "oa:ClickElement",
                        KeyModifiers="{x:Null}",
                        AnimateMouse="False",
                        Button="1",
                        DoubleClick="False",
                        Element="[item]",
                        Focus="False",
                        OffsetX=activity["x"],
                        OffsetY=activity["y"],
                        PostWait="00:00:00",
                        VirtualClick="True",
                    )
                    sequence_out.append(click_activity)
                elif activity.name == "keyboardEvent":
                    keyboard_activity = soup_openrpa.new_tag(
                        "oa:TypeText",
                        ClickDelay="{x:Null}",
                        Text=activity["text"],
                    )
                    sequence_out.append(keyboard_activity)
    # Write changes back to the file
    with open(file_out, "w", encoding="utf-8") as file:
        file.write(str(soup_openrpa.prettify()))


def click_activity(activity, sequence_out, counter):
    click_activity = soup_openrpa.new_tag(
        "oa:ClickElement",
        KeyModifiers="{x:Null}",
        AnimateMouse="False",
        Button="1",
        DoubleClick="False",
        Element="[item]",
        Focus="False",
        OffsetX=activity["x"],
        OffsetY=activity["y"],
        PostWait="00:00:00",
        VirtualClick="True",
        **{"sap2010:WorkflowViewState.IdRef": f"ClickElement_{counter}"},
    )
    sequence_out.append(click_activity)
    counter += 1
