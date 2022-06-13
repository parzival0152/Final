/// <reference path="index.js" />

const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        template_data:{
            title:"",
            description:"",
            stations:[
                {
                    Name:"",
                    fields:[]
                }
            ]
        }
    },
    computed:{
    },
    async created(){
        
    },
    methods: {
        create_template(){
            postData('/api/test',this.template_data)
        },
        add_station(){
            this.template_data.stations.push({
                Name:"",
                Email:"",
                fields:[]
            })
        },
        add_input_to_station(station){
            station.fields.push({
                type:"input",
                prompt:"",
                value:""
            })
        },
        add_text_to_station(station){
            station.fields.push({
                type:"text",
                value:""
            })
        }
    }
})