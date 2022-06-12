/// <reference path="jquery-3.6.0.js" />

class inputCreator {
    constructor(targetdiv, stationId) {
        this.stationId = stationId;
        this.targetdiv = targetdiv;
        this.count = 0;
    }

    CreateInputField = () => {
        let div = $("<div></div>").addClass("form-floating w-75");
        let name = `Station${this.stationId}_input${this.count}`;
        let input = $("<input></input>").addClass("form-control").attr({
            name: name,
            type: "text",
            placeholder: "skdjfg",
            border:"15px",
            "autocomplete": "off",
            "required": "true"
        }).prop("required",true);
        let label = $("<label></label>")
            .addClass("InputLabel")
            .attr("for", name)
            .text("Enter the prompt for the input");
        div.append(input,label)
        this.targetdiv.append(div);
        this.count++;
    };

    CreateImageField = () => {
        let div = $("<div></div>").addClass("form-floating w-75");
        let name = `Station${this.stationId}_image${this.count}`;
        let input = $("<input></input>").addClass("form-control").attr({
            name: name,
            type: "text",
            placeholder: "skdjfg",
            border:"15px",
            "autocomplete": "off",
            "required": "true"
        }).prop("required",true);
        let label = $("<label></label>")
            .addClass("InputLabel")
            .attr("for", name)
            .text("Enter the prompt for the input");
        div.append(input,label)
        this.targetdiv.append(div);
        this.count++;
    };

    CreateTextField = () => {
        let div = $("<div></div>").addClass(" w-75");
        let name = `Station${this.stationId}_text${this.count}`;
        let input = $("<textarea></textarea>").addClass("form-control").attr({
            name: name,
            border:"30%",
            placeholder: "skdjfg",
            "autocomplete": "off",
        }).prop("required",true);
        let label = $("<label></label>")
            .addClass("InputLabel")
            .attr("for", name)
            .text("Enter the text you wish to be displayed");
        div.append(input,label)
        this.targetdiv.append(div);
        this.count++;
    };
}