function loadXML(filename, on_finish)
{
    var xhr = new XMLHttpRequest();
    xhr.onload = function() {
        on_finish(xhr.responseXML);
    }
    xhr.onerror = function() {
        dump("Error while getting XML.");
    }
    xhr.open("GET", filename);
    xhr.responseType = "document";
    xhr.send();
}

const e = React.createElement;

class ToDoEntry extends React.Component
{
    constructor(props) {
        super(props);
        this.state = { Checked: false };
        this.onToggleRaw = this.onToggleRaw.bind(this);
        this.onClickText = this.onClickText.bind(this);
    }

    onToggleRaw(e)
    {
        this.setState({ Checked: !this.state.Checked },
                      function() {this.onToggle(this.state.Checked)});
    }

    onToggle(new_checked)
    {
    }

    onClickText(e)
    {
    }

    checked()
    {
        return this.state.Checked;
    }

    check()
    {
        if(!this.state.Checked)
        {
            this.setState({ Checked: true },
                          function() {this.onToggle(true)});
        }
    }

    uncheck()
    {
        if(this.state.Checked)
        {
            this.setState({ Checked: false },
                          function() {this.onToggle(false)});
        }
    }

    text()
    {
        return this.props.Text;
    }

    rightText()
    {
        return this.props.Righttext;
    }

    render()
    {
        let CheckerSize = this.props.CheckerSize;
        let CircleThickness = this.props.CircleThickness;
        let CheckCircle =
            e("circle",
              {cx: CheckerSize / 2, cy: CheckerSize / 2, r: CheckerSize / 2 - CircleThickness,
               fill: "none",
               className: "Border"},
              null);
        let CheckInner =
            e("circle",
              {cx: CheckerSize / 2, cy: CheckerSize / 2, r: CheckerSize / 2 - 3 * CircleThickness,
               stroke: "none",
               className: "CheckMark"},
              null);
        var CheckMark = null;
        if(this.state.Checked)
        {
            CheckMark =
                e("svg",
                  {className: "Checker", width: CheckerSize, height: CheckerSize,
                   onClick: this.onToggleRaw},
                  CheckCircle,
                  CheckInner);
        }
        else
        {
            CheckMark =
                e("svg",
                  {className: "Checker", width: CheckerSize, height: CheckerSize,
                   onClick: this.onToggleRaw},
                  CheckCircle);
        }

        var Text = null;
        if(this.props.Link)
        {
            Text = e("a", {href: this.props.Link}, this.text());
        }
        else
        {
            Text = this.text();
        }

        return e("div", {className: this.props.Class},
                 CheckMark,
                 e("span", {className: "TodoText", onClick: this.onClickText}, Text),
                 e("span", {className: "TodoRightText"}, this.rightText())
                );
    }
}
