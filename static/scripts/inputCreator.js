/// <reference path="jquery-3.6.0.js" />

class inputCreator {
    constructor(targetdiv, stationId) {
        this.stationId = stationId;
        this.targetdiv = targetdiv;
        this.count = 0;
    }

    CreateInputField = () => {
        let div = $("<div></div>").addClass("form-floating");
        let name = `Station${this.stationId}_input${this.count}`;
        let input = $("<input></input>").addClass("form-control").attr({
            name: name,
            type: "text",
            placeholder: "skdjfg",
            "autocomplete": "off"
        });
        let label = $("<label></label>")
            .addClass("InputLabel")
            .attr("for", name)
            .text("Enter the prompt for the input");
        div.append(input,label)
        this.targetdiv.append(div);
        this.count++;
    };

    CreateTextField = () => {
        let div = $("<div></div>").addClass("form-floating");
        let name = `Station${this.stationId}_text${this.count}`;
        let input = $("<textarea></textarea>").addClass("form-control").attr({
            name: name,
            placeholder: "skdjfg",
            "autocomplete": "off"
        });
        let label = $("<label></label>")
            .addClass("InputLabel")
            .attr("for", name)
            .text("Enter the text you wish to be displayed");
        div.append(input,label)
        this.targetdiv.append(div);
        this.count++;
    };
}