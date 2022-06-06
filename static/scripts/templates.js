/// <reference path="jquery-3.6.0.js" />
/// <reference path="inputCreator.js" />

const form = $("#form");
let stationCount = 0;
let count = 0;


$("#station_maker").on("click", () => {
    // Code to create a station goes here
    let StationWrapper = $("<div></div>").addClass("StationWrapper");
    let contentDiv = $("<div></div>").attr("id", `station${stationCount}`).addClass("StationContent");

    let nameLabel = $("<label></label>")
        .addClass("StationLabel")
        .attr("for", `Station${stationCount}_Name`)
        .text("Enter a name for the station");

    let nameInput = $("<input></input>").attr({
        class: "form-control",
        name: `Station${stationCount}_Name`,
        type: "text",
        placeholder: "skdjfg",
        "autocomplete": "off"
    }).prop("required",true);

    let emailLabel = $("<label></label>").addClass("StationLabel")
        .attr("for", `Station${stationCount}_Email`)
        .text("Enter an email for the station");

    let emailInput = $("<input></input>").attr({
        class: "form-control",
        name: `Station${stationCount}_Email`,
        type: "email",
        placeholder: "skdjfg",
        "autocomplete": "off"
    }).prop("required",true);

    let nameDiv = $("<div></div>").addClass("form-floating w-75").append(nameInput, nameLabel);
    let emailDiv = $("<div></div>").addClass("form-floating w-75").append(emailInput, emailLabel);

    if (stationCount == 0){
        emailInput.prop("required",false);
        emailDiv.hide();
    }

    let inC = new inputCreator(contentDiv, stationCount);

    let buttonDiv = $("<div></div>").addClass("btn-group");
    
    let Textbutton = $("<button></button>").text("Create a text field").on("click", () => { inC.CreateTextField() }).attr("type", "button").addClass("btn btn-primary");
    let Inputbutton =$("<button></button>").text("Create a user-input field").on("click", () => { inC.CreateInputField() }).attr("type", "button").addClass("btn btn-primary");

    buttonDiv.append(Textbutton,Inputbutton)

    StationWrapper.append($("<div></div>").text(`This is Station #${stationCount}`),
        nameDiv, emailDiv, contentDiv,buttonDiv
    );

    form.append(StationWrapper);
    stationCount++;
});

