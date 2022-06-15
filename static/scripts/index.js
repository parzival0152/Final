

async function postData(url, data) {
    let response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });
    return response
}

function checkValidityTemplate(data) {
    //check that title isn't empty
    if (data.title.length == 0) {
        alert("Template title can't be empty")
        return false
    }

    //check that description isn't empty
    if (data.description.length == 0) {
        alert("Template description can't be empty")
        return false
    }

    //check stations validity
    data.stations.forEach((station, index) => {

        //chech that station name isn't empty
        if (station.Name.length == 0) {
            alert("Station name can't be empty")
            return false
        }

        //check that station email isn't empty
        if (station.Email.length == 0 && index != 0) {
            alert("Station email can't be empty")
            return false
        }

        //check that station has some fields
        if(station.fields.length == 0){
            alert("Station must have at-least one (1) field")
            return false
        }

        station.fields.forEach(field => {

            //validate text
            if (field.type == "text") {
                if (field.value.length == 0) {
                    alert("Textual input can't be empty")
                    return false
                }
            }

            //validate input
            if (field.type == "input") {
                if (field.prompt.length == 0) {
                    alert("Input can't be empty");
                    console.log("done with alert")
                    return false
                }
            }

            //validate radio
            if(field.type == 'radio'){
                if (field.options.length == 0) {
                    alert("Radio must have at-least one (1) option");
                    return false
                }
            }

        })

    });
    return true
}


function checkValidityDocument(data, stage) {

    //check stations validity
    station = data.stations[stage]

    station.fields.forEach(field => {
        //TODO: squash this bug
        //validate input
        if (field.type == "input") {
            if (field.value.length == 0) {
                alert("Input can't be empty")
                return false
            }
        }

        //validate radio
        if(field.type == 'radio'){
            if (field.choosen == '') {
                alert("You must choose and option in the radio")
                return false
            }
        }

    })
    return true
}