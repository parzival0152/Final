

const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        text:"hello there",
        template_data:{},
        template_stats : {}
    },
    computed:{
    },
    async created(){
        this.id = window.id;
        let response = await fetch('/api/templates/'+this.id);
        let data = await response.json()
        this.template_data = data.data
        this.template_stats = data.stats
        console.log(this.template_data)
    },
    methods: {
    }
})