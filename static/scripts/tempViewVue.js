

const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        template_data:{},
        template_stats : {}
    },
    computed:{
    },
    async created(){
        this.id = window.id;
        this.stats_show = window.stats_show == "True"
        let response = await fetch('/api/templates/'+this.id);
        let data = await response.json()
        this.template_data = data.data
        this.template_stats = data.stats
    },
    methods: {
    }
})