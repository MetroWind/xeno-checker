function getQuestIDStr(quest_node)
{
    let QuestID = quest_node.querySelector("quest-id");
    let Name = QuestID.textContent;
    let Location = QuestID.getAttribute("location")
    return `${Name} (${Location})`;
}

function storageKeyQuest(quest_node)
{
    let QuestID = quest_node.querySelector("quest-id");
    let Name = QuestID.textContent;
    let Location = QuestID.getAttribute("location")
    let Client = quest_node.querySelector("client").textContent;
    return `quest-${Name}-${Location}-${Client}`;
}

class QuestEntry extends ToDoEntry
{
    constructor(props)
    {
        super(props);
        this.StorageKey = storageKeyQuest(this.props.QuestNode);
        let NodeID = this.props.QuestNode.querySelector("quest-id");
        this.Location = NodeID.getAttribute("location");
        this.Name = NodeID.textContent;
        this.Client = NodeID.querySelector("client");
    }

    componentDidMount()
    {
        if(localStorage.getItem(this.StorageKey) == "true")
        {
            this.check();
        }
        else
        {
            this.uncheck();
        }
    }

    text()
    {
        let QuestID = this.props.QuestNode.querySelector("quest-id");
        return QuestID.textContent;
    }

    onToggle(new_checked)
    {
        localStorage.setItem(this.StorageKey, new_checked);
    }

    onClickText()
    {
        this.props.OnClickText(this.props.QuestNode);
    }

    rightText()
    {
        return "";
    }
}

class QuestList extends React.Component
{
    render()
    {
        if(this.props.Hide)
        {
            return e("div", {},
                     e("h2", {className: "Location", onClick: this.props.OnClick}, this.props.Loc));
        }
        else
        {
            var Quests = [];
            var i = 0;
            for(var i = 0; i < this.props.Quests.length; i++)
            {
                const node_quest = this.props.Quests[i];
                Quests.push(
                    e(QuestEntry,
                      {QuestNode: node_quest, key: i,
                       CheckerSize: 24, CircleThickness: 2,
                       OnClickText: this.props.OnClickQuest,
                       Class: "TodoEntry",
                      },
                      null));
            }
            return e("div", {},
                     e("h2", {className: "Location", onClick: this.props.OnClick}, this.props.Loc),
                     e("div", {className: "Quests"}, Quests));
        }
    }
}

class LocationList extends React.Component
{
    constructor(props)
    {
        super(props);

        var Quests = {};
        this.props.XMLDoc.querySelectorAll("quest")
            .forEach(function(node_quest) {
                let NodeID = node_quest.querySelector("quest-id");
                let Loc = NodeID.getAttribute("location");

                if(Loc in Quests)
                {
                    Quests[Loc].push(node_quest);
                }
                else
                {
                    Quests[Loc] = [node_quest];
                }
            });

        this.Quests = Quests;
        var Hide = {};
        Object.keys(this.Quests).forEach(function(key) {
            Hide[key] = true;
        });
        this.state = { Hide: Hide, Detail: null };
        this.CurrentShow = null;

        // this.onClickLocation = this.onClickLocation.bind(this);
        this.onClickQuest = this.onClickQuest.bind(this);
    }

    onClickQuest(node)
    {
        this.setState({Detail: node});
    }

    onClickLocation(location)
    {
        var Hide = this.state.Hide;

        if(location == this.CurrentShow)
        {
            Hide[location] = true;
        }
        else
        {
            Hide[this.CurrentShow] = true;
            Hide[location] = false;
        }

        this.setState({Hide: Hide}, function() {
            if(location == this.CurrentShow)
            {
                this.CurrentShow = null;
            }
            else
            {
                this.CurrentShow = location;
            }
        });
    }

    blockerView(node_blocker, i)
    {
        const Type = node_blocker.getAttribute("type");
        var Props = {key: i};
        switch(Type)
        {
            case "AreaClear":
            return e("li", Props, node_blocker.textContent + " cleared");

            case "AreaAccess":
            return e("li", Props, "Access to " + node_blocker.textContent);

            case "Quest":
            const NodeQuest = node_blocker.querySelector("quest-id");
            const Loc = NodeQuest.getAttribute("location");
            const Quest = NodeQuest.textContent;
            return e("li", Props, Quest);

            case "MutualExclusiveQuests":
            const Quests = [];
            node_blocker.querySelectorAll("quest-id").forEach(
                (NodeQuest) => Quests.push(NodeQuest.textContent));
            return e("li", Props, Quests.join(" or "));

            case "AreaAffinity":
            const Ele = node_blocker.querySelectorAll("element");
            return e("li", Props, `${Ele[0].textContent} affinity at ${Ele[1].textContent}`);

            case "RegisterNPC":
            const NPCEle = node_blocker.querySelectorAll("element");
            if(NPCEle.length == 1)
            {
                return e("li", Props, `${NPCEle[0].textContent} registered`);
            }
            else if(NPCEle.length == 2)
            {
                return e("li", Props,
                         `${NPCEle[0].textContent} registered in
${NPCEle[1].textContent}`);
            }

            case "NPCInviteToC6":
            const Name = node_blocker.textContent;
            return e("li", Props, `${Name} invited to Colony 6`);

            case "Unknown":
            return e("li", Props, node_blocker.textContent);

            default:
            return e("li", Props, "???");
        }
    }

    blockerListView(node_blockers)
    {
        const SubNodes = [];
        const Blockers = node_blockers.querySelectorAll("blocker");
        for(var i = 0; i < Blockers.length; i++)
        {
            SubNodes.push(this.blockerView(Blockers[i], i));
        }
        return e("ul", {className: "BlockerList"}, SubNodes);
    }

    onClickDetailClose(e)
    {
        this.setState({Detail: null});
    }

    btnClose()
    {
        return e("div", {id: "BtnCloseDetailWrapper"},
                 e('a', {id: "BtnCloseDetail", href: "#",
                         onClick: () => this.onClickDetailClose()},
                   "[X]"));
    }

    detailView(node_quest)
    {
        const NodeID = node_quest.querySelector("quest-id");
        const Name = NodeID.textContent;
        const Location = NodeID.getAttribute("location");
        const Client = node_quest.querySelector("client").textContent;
        const Link = node_quest.querySelector("link").textContent;

        var DetailView =
            e("div", {id: "Detail"},
              this.btnClose(),
              e("h3", {},
                e("a", {className: "WikiLink", href: Link}, "@"),
                e("span", {}, Name)),
              e("table", {id: "QuestProperties"},
                e("tbody", {},
                  e("tr", {},
                    e("td", {className: "PropertyKey"}, "Location"),
                    e("td", {className: "PropertyValue"}, Location)),
                  e("tr", {},
                    e("td", {className: "PropertyKey"}, "Client"),
                    e("td", {className: "PropertyValue"}, Client)),
                  e("tr", {},
                    e("td", {className: "PropertyKey"}, "Blockers"),
                    e("td", {className: "PropertyValue"},
                      this.blockerListView(node_quest.querySelector("blockers")))),
                 )));

        return DetailView;
    }

    render()
    {
        var SubNodes = [];
        var Quests = this.Quests;
        var onClickLocation = this.onClickLocation;
        for(const key in this.Quests)
        {
            SubNodes.push(
                e(QuestList,
                  {Loc: key,
                   Quests: this.Quests[key],
                   Hide: this.state.Hide[key],
                   OnClick: () => this.onClickLocation(key),
                   OnClickQuest: this.onClickQuest,
                   key: key},
                  null));
        }

        var DetailView = null;
        if(this.state.Detail)
        {
            DetailView = this.detailView(this.state.Detail);
        }

        return e("div", {},
                 DetailView,
                 e("div", {}, SubNodes));
    }
}


loadXML("quests.xml", function(doc) {
    ReactDOM.render(
        e(LocationList, {XMLDoc: doc}, null),
        document.getElementById('body'));
});
