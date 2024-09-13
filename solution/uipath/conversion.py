import xml.etree.ElementTree as ET
from xml.dom import minidom
import os


def parse_monitoring_result(file_path):
    """
    Input: file_path (str) - Path to the BPMN file
    Output: elements (list) - List of tuples with the following format:
    [('startEvent', 'id3f98fcb5-a92a-4607-8b78-5d74a485c646', 'start', ['id46d0112d-abc2-41df-928b-5a5495c09d18']),
    ('task', 'id13569253-272b-4ab3-b070-7223703bffdb', 'Activity 1', ['id46d0112d-abc2-41df-928b-5a5495c09d18'], ['id03bfa529-93fe-46cd-8762-0a36b9d1521d'], [('2024-06-26T10:00:00', '100', '200')], [('2024-06-26T10:01:00', 'New customer')]),
    ('exclusiveGateway', 'id52a2c804-c329-4ae5-a179-2ccf2c0f6189', 'id03bfa529-93fe-46cd-8762-0a36b9d1521d', ['id5d16bbdc-5e72-4eaf-9a35-a92bd41b0838', 'ide403fbfa-a2c8-482e-acfa-f3a4bf6f4697']),
    ('task', 'id0dd0c9b5-a29e-4be5-b957-2f0c74556793', 'Activity 2A', ['id5d16bbdc-5e72-4eaf-9a35-a92bd41b0838'], ['id6a82dd9b-48d1-4752-8645-7d5e465760fb'], [('2024-06-26T10:10:00', '150', '250')], [('2024-06-26T10:11:00', 'Brandon')]),
    ('task', 'id6039a246-bf27-40dd-bfa3-3bc6876e2be5', 'Activity 2B', ['ide403fbfa-a2c8-482e-acfa-f3a4bf6f4697'], ['idc0acf0d2-7798-4169-ac6b-a478884773d3'], [('2024-06-26T10:10:00', '150', '250')], [('2024-06-26T10:11:00', 'Emily')]),
    ('task', 'id00637ab1-2619-45d8-b991-fec4bfd14057', 'Activity 3', ['id6a82dd9b-48d1-4752-8645-7d5e465760fb', 'idc0acf0d2-7798-4169-ac6b-a478884773d3'], ['id4e333789-b126-4819-a4a8-34979f19d7b0'], [('2024-06-26T10:10:00', '250', '250'), ('2024-06-26T10:10:00', '300', '200')], []),
    ('endEvent', 'ide4e9e370-7a6d-439e-bfb5-15ab87877c2e', 'end', 'id4e333789-b126-4819-a4a8-34979f19d7b0')]
    """
    tree = ET.parse(file_path)
    root = tree.getroot()
    root = root.find("{*}process")
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
            in_seq = [seq.text for seq in child.findall("{*}incoming")]
            out_seq = [seq.text for seq in child.findall("{*}outgoing")]
            click_events = []
            keyboard_events = []
            for ext in child.find("{*}extensionElements"):
                if ext.tag.endswith("clickEvent"):
                    click_events.append(
                        (
                            ext.attrib["timestamp"],
                            ext.attrib["x"],
                            ext.attrib["y"],
                        )
                    )
                elif ext.tag.endswith("keyboardEvent"):
                    keyboard_events.append(
                        (
                            ext.attrib["timestamp"],
                            ext.attrib["text"],
                        )
                    )
            elements.append(
                (
                    "task",
                    task_id,
                    task_name,
                    in_seq,
                    out_seq,
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


def bpmn_elements_to_xaml_uipath(elements):
    """
    Input: elements (list) - List of tuples with the following format:
    [('startEvent', 'id3f98fcb5-a92a-4607-8b78-5d74a485c646', 'start', ['id46d0112d-abc2-41df-928b-5a5495c09d18']),
    ('task', 'id13569253-272b-4ab3-b070-7223703bffdb', 'Activity 1', ['id46d0112d-abc2-41df-928b-5a5495c09d18'], ['id03bfa529-93fe-46cd-8762-0a36b9d1521d'], [('2024-06-26T10:00:00', '100', '200')], [('2024-06-26T10:01:00', 'New customer')]),
    ('exclusiveGateway', 'id52a2c804-c329-4ae5-a179-2ccf2c0f6189', 'id03bfa529-93fe-46cd-8762-0a36b9d1521d', ['id5d16bbdc-5e72-4eaf-9a35-a92bd41b0838', 'ide403fbfa-a2c8-482e-acfa-f3a4bf6f4697']),
    ('task', 'id0dd0c9b5-a29e-4be5-b957-2f0c74556793', 'Activity 2A', ['id5d16bbdc-5e72-4eaf-9a35-a92bd41b0838'], ['id6a82dd9b-48d1-4752-8645-7d5e465760fb'], [('2024-06-26T10:10:00', '150', '250')], [('2024-06-26T10:11:00', 'Brandon')]),
    ('task', 'id6039a246-bf27-40dd-bfa3-3bc6876e2be5', 'Activity 2B', ['ide403fbfa-a2c8-482e-acfa-f3a4bf6f4697'], ['idc0acf0d2-7798-4169-ac6b-a478884773d3'], [('2024-06-26T10:10:00', '150', '250')], [('2024-06-26T10:11:00', 'Emily')]),
    ('task', 'id00637ab1-2619-45d8-b991-fec4bfd14057', 'Activity 3', ['id6a82dd9b-48d1-4752-8645-7d5e465760fb', 'idc0acf0d2-7798-4169-ac6b-a478884773d3'], ['id4e333789-b126-4819-a4a8-34979f19d7b0'], [('2024-06-26T10:10:00', '250', '250'), ('2024-06-26T10:10:00', '300', '200')], []),
    ('endEvent', 'ide4e9e370-7a6d-439e-bfb5-15ab87877c2e', 'end', 'id4e333789-b126-4819-a4a8-34979f19d7b0')]
    Output: result (str) - XAML content
    """
    xaml_elements = []

    for element in elements:
        if element[0] == "startEvent":
            continue
        elif element[0] == "task":
            task_name, click_events, keyboard_events = (
                element[2],
                element[5],
                element[6],
            )
            for click_event in click_events:
                xaml_elements.append(
                    f'<uix:NClick ActivateBefore="True" ClickType="Single" DisplayName="Click" KeyModifiers="None" MouseButton="Left" Version="V3" />'
                )
            for keyboard_event in keyboard_events:
                xaml_elements.append(
                    f'<uix:NTypeInto ActivateBefore="True" ClickBeforeMode="Single" DisplayName="Type Into" EmptyFieldMode="SingleLine" Text="{keyboard_event[1]}" Version="V3" />'
                )
        elif element[0] == "exclusiveGateway":
            xaml_elements.append("<If>")
            xaml_elements.append("<If.Then>")
            xaml_elements.append("<Sequence>")
            next_task = [
                e for e in elements if e[3][0] == element[3][0] and e != element
            ][0]
            task_name, click_events, keyboard_events = (
                next_task[2],
                next_task[5],
                next_task[6],
            )
            elements.remove(next_task)
            for click_event in click_events:
                xaml_elements.append(
                    f'<uix:NClick ActivateBefore="True" ClickType="Single" DisplayName="Click" KeyModifiers="None" MouseButton="Left" Version="V3" />'
                )
            for keyboard_event in keyboard_events:
                xaml_elements.append(
                    f'<uix:NTypeInto ActivateBefore="True" ClickBeforeMode="Single" DisplayName="Type Into" EmptyFieldMode="SingleLine" Text="{keyboard_event[1]}" Version="V3" />'
                )
            xaml_elements.append("</Sequence>")
            xaml_elements.append("</If.Then>")
            xaml_elements.append("<If.Else>")
            xaml_elements.append("<Sequence>")
            next_task = [
                e for e in elements if e[3][0] == element[3][1] and e != element
            ][0]
            task_name, click_events, keyboard_events = (
                next_task[2],
                next_task[5],
                next_task[6],
            )
            elements.remove(next_task)
            for click_event in click_events:
                xaml_elements.append(
                    f'<uix:NClick ActivateBefore="True" ClickType="Single" DisplayName="Click" KeyModifiers="None" MouseButton="Left" Version="V3" />'
                )
            for keyboard_event in keyboard_events:
                xaml_elements.append(
                    f'<uix:NTypeInto ActivateBefore="True" ClickBeforeMode="Single" DisplayName="Type Into" EmptyFieldMode="SingleLine" Text="{keyboard_event[1]}" Version="V3" />'
                )
            xaml_elements.append("</Sequence>")
            xaml_elements.append("</If.Else>")
            xaml_elements.append("</If>")
        elif element[0] == "endEvent":
            continue
    result = "<Sequence>\n" + "\n".join(xaml_elements) + "\n</Sequence>"
    return result


def insert_xaml_into_uipath_template(template_path, xaml_content):
    with open(template_path, "r") as file:
        template = file.read()

    start_index = template.find("<Activity")
    end_index = template.find("</Activity>", start_index) + len("</Activity>")

    new_content = (
        template[:start_index]
        + template[start_index:end_index].replace(
            "</Activity>", xaml_content + "\n" + "</Activity>"
        )
        + template[end_index:]
    )

    return new_content


def generate_executable_process(
    xml_string, output_file="output/executable_process.xaml"
):
    parsed_xml = minidom.parseString(xml_string)
    indented_xml = parsed_xml.toprettyxml(indent="  ")
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)
    with open(output_file, "w") as file:
        file.write(indented_xml)
