/// <reference path="jquery-3.6.0.js" />

let stage = $("#stage").text(); //grab the value of the stage that we are on right now

let currentStation = $(`#StationBody${stage}`); //locate the station for this particular stage

currentStation.children("div.form-floating").children("input").prop( "disabled", false ); //enable all inputs inside the stage

let submit = $("<button></button>").text("Approve").attr("type", "submit").addClass("btn btn-success")
currentStation.append(submit)