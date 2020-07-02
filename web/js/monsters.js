function getQuestIDStr(quest_node)
{
    let QuestID = quest_node.querySelector("quest-id");
    let Name = QuestID.textContent;
    let Location = QuestID.getAttribute("location")
    return `${Name} (${Location})`;
}

function storageKeyMonster(m_node)
{
    let Name = m_node.querySelector("name").textContent;
    return "monster-" + Name;
}

class MonsterEntry extends ToDoEntry
{
    constructor(props)
    {
        super(props);
        this.StorageKey = storageKeyMonster(this.props.Node);
        const Node = this.props.Node;
        this.Location = Node.querySelector("location").textContent;
        this.Name = Node.querySelector("name").textContent;;
        this.Level = Node.querySelector("level").textContent;
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
        let Name = this.props.Node.querySelector("name");
        return Name.textContent;
    }

    onToggle(new_checked)
    {
        console.log(`Setting ${this.StorageKey} to ${new_checked}...`);
        localStorage.setItem(this.StorageKey, new_checked);
    }

    rightText()
    {
        return this.Level;
    }
}

class MonsterList extends React.Component
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
            var Monsters = [];
            var i = 0;
            this.props.Monsters.forEach(function(node) {
                Monsters.push(
                    e(MonsterEntry,
                      {Node: node, key: i,
                       CheckerSize: 24, CircleThickness: 2,
                       Class: "TodoEntry",
                       Link: node.querySelector("link").textContent,
                      },
                      null));
                i += 1;
            });
            return e("div", {},
                     e("h2", {className: "Location", onClick: this.props.OnClick}, this.props.Loc),
                     e("div", {className: "Monsters"}, Monsters));
        }
    }
}

class LocationList extends React.Component
{
    constructor(props)
    {
        super(props);

        var Monsters = {};
        this.props.XMLDoc.querySelectorAll("monster")
            .forEach(function(node) {
                let Loc = node.querySelector("location").textContent;

                if(Loc in Monsters)
                {
                    Monsters[Loc].push(node);
                }
                else
                {
                    Monsters[Loc] = [node];
                }
            });

        this.Monsters = Monsters;
        var Hide = {};
        Object.keys(this.Monsters).forEach(function(key) {
            Hide[key] = false;
        });
        this.state = { Hide: Hide };
        this.CurrentShow = null;

        // this.onClickLocation = this.onClickLocation.bind(this);
    }

    render()
    {
        var SubNodes = [];
        for(const key in this.Monsters)
        {
            SubNodes.push(
                e(MonsterList,
                  {Loc: key,
                   Monsters: this.Monsters[key],
                   Hide: this.state.Hide[key],
                   key: key},
                  null));
        }

        return e("div", {}, SubNodes);
    }
}


loadXML("monsters.xml", function(doc) {
    ReactDOM.render(
        e(LocationList, {XMLDoc: doc}, null),
        document.getElementById('body'));
});
