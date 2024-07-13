def click_activity(soup, activity, sequence_out, counter):
    click_activity = soup.new_tag(
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


def keyboard_activity(soup, activity, sequence_out, counter):
    keyboard_activity = soup.new_tag(
        "oa:TypeText",
        ClickDelay="{x:Null}",
        Text=activity["text"],
        **{"sap2010:WorkflowViewState.IdRef": f"TypeText_{counter}"},
    )
    sequence_out.append(keyboard_activity)
    counter += 1
