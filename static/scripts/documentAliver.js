/// <reference path="jquery-3.6.0.js" />

let stage = $("#stage").val(); //grab the value of the stage that we are on right now
let allowed = $("#allowed").text()
if (allowed == "True"){
let currentStation = $(`#StationBody${stage}`); //locate the station for this particular stage

currentStation.children("div.form-floating").children("input").prop( "disabled", false ).prop( "required", true ); //enable all inputs inside the stage
currentStation.children("div.form-floating").children("input").attr("autocomplete", "off");

let submit = $("<button></button>").text("Approve").attr("type", "submit").addClass("btn btn-success");
currentStation.append(submit);
}