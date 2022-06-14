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
                    state:"",
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
        async create_template(){
            //TODO: data validation





            //actually create the template
            let res = await postData('/api/create_template',this.template_data)
            if (res.status==200){
                window.location.href = res.url
            }
            else{
                //TODO: make sure things dont break if server is unable to respond
            }
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