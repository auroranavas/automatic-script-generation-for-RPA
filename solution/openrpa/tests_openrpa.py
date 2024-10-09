import unittest
import os
from unittest.mock import patch, mock_open
from xml.etree.ElementTree import Element, SubElement, tostring
import tempfile

from conversion import (
    parse_monitoring_result,
    bpmn_elements_to_xaml_openrpa,
    insert_xaml_into_openrpa_template,
    generate_executable_process,
)


class TestConversion(unittest.TestCase):
    def setUp(self):
        self.bpmn_xml = Element("definitions")
        process = SubElement(self.bpmn_xml, "process")

        start_event = SubElement(process, "startEvent", id="start1", name="Start")
        SubElement(start_event, "outgoing").text = "flow1"

        task = SubElement(process, "task", id="task1", name="Task 1")
        SubElement(task, "incoming").text = "flow1"
        SubElement(task, "outgoing").text = "flow2"
        extension_elements = SubElement(task, "extensionElements")
        click_event = SubElement(
            extension_elements,
            "clickEvent",
            timestamp="2024-06-26T10:00:00",
            x="100",
            y="200",
        )
        keyboard_event = SubElement(
            extension_elements,
            "keyboardEvent",
            timestamp="2024-06-26T10:01:00",
            text="New customer",
        )

        exclusive_gateway = SubElement(
            process, "exclusiveGateway", id="gateway1", name="Exclusive Gateway"
        )
        SubElement(exclusive_gateway, "incoming").text = "flow2"
        SubElement(exclusive_gateway, "outgoing").text = "flow3"
        SubElement(exclusive_gateway, "outgoing").text = "flow4"

        task2 = SubElement(process, "task", id="task2", name="Task 2")
        SubElement(task2, "incoming").text = "flow3"
        SubElement(task2, "outgoing").text = "flow5"
        extension_elements = SubElement(task2, "extensionElements")
        click_event = SubElement(
            extension_elements,
            "clickEvent",
            timestamp="2024-06-26T10:00:00",
            x="300",
            y="250",
        )
        keyboard_event = SubElement(
            extension_elements,
            "keyboardEvent",
            timestamp="2024-06-26T10:01:00",
            text="March invoice",
        )

        task3 = SubElement(process, "task", id="task3", name="Task 3")
        SubElement(task3, "incoming").text = "flow4"
        SubElement(task3, "outgoing").text = "flow6"
        extension_elements = SubElement(task3, "extensionElements")
        click_event = SubElement(
            extension_elements,
            "clickEvent",
            timestamp="2024-06-26T10:00:00",
            x="100",
            y="120",
        )
        keyboard_event = SubElement(
            extension_elements,
            "keyboardEvent",
            timestamp="2024-06-26T10:01:00",
            text="Sales report",
        )

        end_event = SubElement(process, "endEvent", id="end1", name="End")
        SubElement(end_event, "incoming").text = "flow5"
        SubElement(end_event, "incoming").text = "flow6"

        self.bpmn_xml_str = tostring(self.bpmn_xml, encoding="unicode")

    def test_parse_monitoring_result(self):
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", suffix=".xml"
        ) as temp_file:
            temp_file.write(self.bpmn_xml_str)
            temp_file_path = temp_file.name

        try:
            elements = parse_monitoring_result(temp_file_path)
            expected_elements = [
                ("startEvent", "start1", "Start", "flow1"),
                (
                    "task",
                    "task1",
                    "Task 1",
                    ["flow1"],
                    ["flow2"],
                    [("2024-06-26T10:00:00", "100", "200")],
                    [("2024-06-26T10:01:00", "New customer")],
                ),
                (
                    "exclusiveGateway",
                    "gateway1",
                    "flow2",
                    ["flow3", "flow4"],
                ),
                (
                    "task",
                    "task2",
                    "Task 2",
                    ["flow3"],
                    ["flow5"],
                    [("2024-06-26T10:00:00", "300", "250")],
                    [("2024-06-26T10:01:00", "March invoice")],
                ),
                (
                    "task",
                    "task3",
                    "Task 3",
                    ["flow4"],
                    ["flow6"],
                    [("2024-06-26T10:00:00", "100", "120")],
                    [("2024-06-26T10:01:00", "Sales report")],
                ),
                ("endEvent", "end1", "End", ["flow5", "flow6"]),
            ]

            self.assertEqual(elements, expected_elements)
        finally:
            os.remove(temp_file_path)

    def test_bpmn_elements_to_xaml_openrpa(self):
        elements = [
            ("startEvent", "start1", "Start", "flow1"),
            (
                "task",
                "task1",
                "Task 1",
                ["flow1"],
                ["flow2"],
                [("2024-06-26T10:00:00", "100", "200")],
                [("2024-06-26T10:01:00", "New customer")],
            ),
            (
                "exclusiveGateway",
                "gateway1",
                "flow2",
                ["flow3", "flow4"],
            ),
            (
                "task",
                "task2",
                "Task 2",
                ["flow3"],
                ["flow5"],
                [("2024-06-26T10:00:00", "300", "250")],
                [("2024-06-26T10:01:00", "March invoice")],
            ),
            (
                "task",
                "task3",
                "Task 3",
                ["flow4"],
                ["flow6"],
                [("2024-06-26T10:00:00", "100", "120")],
                [("2024-06-26T10:01:00", "Sales report")],
            ),
            ("endEvent", "end1", "End", ["flow5", "flow6"]),
        ]
        xaml_content = bpmn_elements_to_xaml_openrpa(elements)
        expected_xaml_content = (
            "<Sequence>\n"
            '<oa:ClickElement KeyModifiers="{x:Null}" AnimateMouse="False" Button="1" DoubleClick="False" Element="[item]" Focus="False" OffsetX="100" OffsetY="200" PostWait="00:00:00" VirtualClick="True" />\n'
            '<oa:TypeText ClickDelay="{x:Null}" Text="New customer" />\n'
            "<If>\n"
            "<If.Then>\n"
            "<Sequence>\n"
            '<oa:ClickElement KeyModifiers="{x:Null}" AnimateMouse="False" Button="1" DoubleClick="False" Element="[item]" Focus="False" OffsetX="300" OffsetY="250" PostWait="00:00:00" VirtualClick="True" />\n'
            '<oa:TypeText ClickDelay="{x:Null}" Text="March invoice" />\n'
            "</Sequence>\n"
            "</If.Then>\n"
            "<If.Else>\n"
            "<Sequence>\n"
            '<oa:ClickElement KeyModifiers="{x:Null}" AnimateMouse="False" Button="1" DoubleClick="False" Element="[item]" Focus="False" OffsetX="100" OffsetY="120" PostWait="00:00:00" VirtualClick="True" />\n'
            '<oa:TypeText ClickDelay="{x:Null}" Text="Sales report" />\n'
            "</Sequence>\n"
            "</If.Else>\n"
            "</If>\n"
            "</Sequence>"
        )
        self.assertEqual(xaml_content, expected_xaml_content)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="""<Activity  mc1:Ignorable="sap sap2010 sads" x:Class="New_Workflow" sap2010:WorkflowViewState.IdRef="New_Workflow_1" mva1:VisualBasic.Settings="Assembly references and imported namespaces serialized as XML namespaces" xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities" xmlns:m="clr-namespace:ManagedSSPI;assembly=System.Net.WebSockets.Client.Managed" </Activity>""",
    )
    def test_insert_xaml_into_openrpa_template(self, mock_file):
        xaml_content = "<Sequence></Sequence>"
        new_content = insert_xaml_into_openrpa_template(
            "dummy_template_path", xaml_content
        )
        expected_content = """<Activity  mc1:Ignorable="sap sap2010 sads" x:Class="New_Workflow" sap2010:WorkflowViewState.IdRef="New_Workflow_1" mva1:VisualBasic.Settings="Assembly references and imported namespaces serialized as XML namespaces" xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities" xmlns:m="clr-namespace:ManagedSSPI;assembly=System.Net.WebSockets.Client.Managed" <Sequence></Sequence>\n</Activity>"""
        self.assertEqual(new_content, expected_content)

    @patch("os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_generate_executable_process(self, mock_file, mock_makedirs):
        xml_string = "<Activity></Activity>"
        generate_executable_process(xml_string, "output/executable_process.xaml")
        mock_file.assert_called_with("output/executable_process.xaml", "w")
        mock_file().write.assert_called_once()


if __name__ == "__main__":
    unittest.main()
