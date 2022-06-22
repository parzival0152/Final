

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
    let warnings = []

    //check that title isn't empty
    if (data.title.length == 0) {
        warnings.push("Template title can't be empty")
    }

    //check that description isn't empty
    // if (data.description.length == 0) {
    //     warnings.push("Template description can't be empty")
    
    // } //removed by suggestion

    //check stations validity
    data.stations.forEach((station, index) => {

        //chech that station name isn't empty
        if (station.Name.length == 0) {
            warnings.push(`Section #${index} name can't be empty`)

        }

        //check that station email isn't empty
        if (station.Email.length == 0 && index != 0) {
            warnings.push(`Section #${index} email can't be empty`)

        }

        //check that station has some fields
        if (station.fields.length == 0) {
            warnings.push(`Section #${index} must have at-least one (1) field`)

        }

        station.fields.forEach(field => {

            //validate text
            if (field.type == "text") {
                if (field.value.length == 0) {
                    warnings.push(`Section #${index}: Textual input can't be empty`)

                }
            }

            //validate input
            if (field.type == "input") {
                if (field.prompt.length == 0) {
                    warnings.push(`Section #${index}: Input can't be empty`)

                }
            }

            //validate radio
            if (field.type == 'radio') {
                if (field.prompt.length == 0) {
                    warnings.push(`Section #${index}: Radio prompt can't be empty`)

                }
                if (field.options.length <= 1) {
                    warnings.push(`Section #${index}: Radio must have at-least two (2) options`);

                }
            }

            //validate checkbox
            if (field.type == 'checkbox') {
                if (field.prompt.length == 0) {
                    warnings.push(`Section #${index}: Checkbox prompt can't be empty`)

                }
                if (field.options.length == 0) {
                    warnings.push(`Section #${index}: Checkbox must have at-least one (1) option`);

                }
            }
        })

    });
    return warnings
}


function checkValidityDocument(data, stage) {

    let warnings = []

    //check stations validity
    let station = data.stations[stage]

    station.fields.forEach(field => {
        //validate input
        if (field.type == "input") {
            if (field.value.length == 0) {
                warnings.push("Input can't be empty")

            }
        }

        //validate radio
        if (field.type == 'radio') {
            if (field.chosen == '') {
                warnings.push("You must choose an option in the radio")

            }
        }

        if (field.type == 'checkbox') {
            if (field.chosen.length == 0) {
                warnings.push("You must choose at-least one option in the checkbox")

            }
        }
    })
    return warnings
}

