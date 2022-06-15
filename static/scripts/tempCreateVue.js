/// <reference path="index.js" />

const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        template_data: {
            title: "",
            description: "",
            stations: [
                {
                    Name: "",
                    Email: "",
                    state: "border-warning",
                    fields: []
                }
            ]
        }
    },
    computed: {
    },
    async created() {

    },
    methods: {
        async create_template() {

            let isValid = checkValidityTemplate(this.template_data)
            if (!isValid) {
                return false
            }

            //actually create the template
            let res = await postData('/api/create_template', this.template_data)
            if (res.status == 200) {
                window.location.href = res.url
            }
            else {
                //TODO: make sure things dont break if server is unable to respond
            }
        },
        add_station() {
            this.template_data.stations.push({
                Name: "",
                Email: "",
                state: "border-info",
                fields: []
            })
        },
        add_input_to_station(station) {
            station.fields.push({
                type: "input",
                prompt: "",
                value: ""
            })
        },
        add_text_to_station(station) {
            station.fields.push({
                type: "text",
                value: ""
            })
        },
        add_radio_to_station(station) {
            station.fields.push({
                type: "radio",
                options: [],
                choosen: '',
                held: ''
            })
        },
        add_to_field(field) {
            if(field.held == ''){
                return false
            }
            field.options.push(field.held)
            field.held = ''
        },
        remove_from_field(field, index) {
            field.options.splice(index, 1)
        }
    }
})