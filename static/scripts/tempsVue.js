

const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        temps: [],
        user_id: 0,
        mode: "none"
    },
    computed:{
        title(){
            return this.mode=="all"? "All Created Templates": "My Created Templates"
        }
    },
    async created(){
        this.mode = mode;
        if(mode == "all"){
            this.get_all_temps();
        }
        else{
            let id = await fetch('/api/current_user_id');
            id = await id.json();
            this.user_id = id["id"];
            this.get_user_temps();
        }
    },
    methods: {
        async get_all_temps() {
            console.log("all mode")
            let docs = await fetch(`/api/templates_all`);
            this.temps = await docs.json();
        },
        async get_user_temps() {
            console.log("user mode")
            let docs = await fetch(`/api/templates/${this.user_id}`);
            this.temps = await docs.json();
        },
        sortDocsAlphabeticallyName() {
            console.log("sorting by name");
            this.temps.sort((a, b) => a.name.localeCompare(b.name));
        },
        sortDocsAlphabeticallyCreator() {
            console.log("sorting by creator");
            this.temps.sort((a, b) => a.creator.localeCompare(b.creator));
        },
        sortDocsDateCreated() {
            console.log("sorting by date");
            this.temps.sort((a, b) => a.Did - b.Did);
        }
    }
})