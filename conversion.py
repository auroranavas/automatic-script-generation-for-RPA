import xml.etree.ElementTree as ET


def parse_bpmn(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    elements = []

    for child in root:
        if child.tag.endswith("startEvent"):
            elements.append(
                (
                    "startEvent",
                    child.attrib["id"],
                    child.attrib["name"],
                    child.find("{*}outgoing").text,
                )
            )
        elif child.tag.endswith("task"):
            task_id = child.attrib["id"]
            task_name = child.attrib["name"]
            incoming = child.find("{*}incoming").text
            outgoing = child.find("{*}outgoing").text
            click_events = []
            keyboard_events = []
            for ext in child.find("{*}extensionElements"):
                if ext.tag.endswith("clickEvent"):
                    click_events.append(
                        (ext.attrib["timestamp"], ext.attrib["x"], ext.attrib["y"])
                    )
                elif ext.tag.endswith("keyboardEvent"):
                    keyboard_events.append(
                        (ext.attrib["timestamp"], ext.attrib["text"])
                    )
            elements.append(
                (
                    "task",
                    task_id,
                    task_name,
                    incoming,
                    outgoing,
                    click_events,
                    keyboard_events,
                )
            )
        elif child.tag.endswith("exclusiveGateway"):
            gateway_id = child.attrib["id"]
            incoming = child.find("{*}incoming").text
            outgoings = [outgoing.text for outgoing in child.findall("{*}outgoing")]
            elements.append(("exclusiveGateway", gateway_id, incoming, outgoings))
        elif child.tag.endswith("endEvent"):
            elements.append(
                (
                    "endEvent",
                    child.attrib["id"],
                    child.attrib["name"],
                    child.find("{*}incoming").text,
                )
            )

    return elements


def bpmn_to_xaml(elements):
    xaml_elements = []

    for element in elements:
        if element[0] == "startEvent":
            # Start event does not produce XAML directly
            continue
        elif element[0] == "task":
            task_name, click_events, keyboard_events = (
                element[2],
                element[5],
                element[6],
            )
            for click_event in click_events:
                xaml_elements.append(
                    f'<oa:ClickElement KeyModifiers="{{x:Null}}" AnimateMouse="False" Button="1" DoubleClick="False" Element="[item]" Focus="False" OffsetX="{click_event[1]}" OffsetY="{click_event[2]}" PostWait="00:00:00" VirtualClick="True" />'
                )
            for keyboard_event in keyboard_events:
                xaml_elements.append(
                    f'<oa:TypeText ClickDelay="{{x:Null}}" Text="{keyboard_event[1]}" />'
                )
        elif element[0] == "exclusiveGateway":
            xaml_elements.append("<If>")
            xaml_elements.append("<If.Then>")
            xaml_elements.append("<Sequence>")
            # Assuming the first outgoing path
            next_task = [e for e in elements if e[1] == element[3][0]][0]
            task_name, click_events, keyboard_events = (
                next_task[2],
                next_task[5],
                next_task[6],
            )
            for click_event in click_events:
                xaml_elements.append(
                    f'<oa:ClickElement KeyModifiers="{{x:Null}}" AnimateMouse="False" Button="1" DoubleClick="False" Element="[item]" Focus="False" OffsetX="{click_event[1]}" OffsetY="{click_event[2]}" PostWait="00:00:00" VirtualClick="True" />'
                )
            for keyboard_event in keyboard_events:
                xaml_elements.append(
                    f'<oa:TypeText ClickDelay="{{x:Null}}" Text="{keyboard_event[1]}" />'
                )
            xaml_elements.append("</Sequence>")
            xaml_elements.append("</If.Then>")
            xaml_elements.append("<If.Else>")
            xaml_elements.append("<Sequence>")
            # Assuming the second outgoing path
            next_task = [e for e in elements if e[1] == element[3][1]][0]
            task_name, click_events, keyboard_events = (
                next_task[2],
                next_task[5],
                next_task[6],
            )
            for click_event in click_events:
                xaml_elements.append(
                    f'<oa:ClickElement KeyModifiers="{{x:Null}}" AnimateMouse="False" Button="1" DoubleClick="False" Element="[item]" Focus="False" OffsetX="{click_event[1]}" OffsetY="{click_event[2]}" PostWait="00:00:00" VirtualClick="True" />'
                )
            for keyboard_event in keyboard_events:
                xaml_elements.append(
                    f'<oa:TypeText ClickDelay="{{x:Null}}" Text="{keyboard_event[1]}" />'
                )
            xaml_elements.append("</Sequence>")
            xaml_elements.append("</If.Else>")
            xaml_elements.append("</If>")
        elif element[0] == "endEvent":
            # End event does not produce XAML directly
            continue

    return "<Sequence>\n" + "\n".join(xaml_elements) + "\n</Sequence>"


# Example usage
bpmn_file = "bpmn_ejemplo/bpmn.bpmn"
bpmn_elements = parse_bpmn(bpmn_file)
xaml_output = bpmn_to_xaml(bpmn_elements)

with open("output.xaml", "w") as file:
    file.write(xaml_output)
