

const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        docs: [],
        user_id: 0,
        state: 0
    },
    async created() {
        let id = await fetch('/api/current_user_id');
        id = await id.json();
        this.user_id = id["id"];
        this.get_pending_docs()
    },
    methods: {
        async get_pending_docs() {
            console.log("pending mode")
            this.state = 0;
            let docs = await fetch(`/api/docs_pending/${this.user_id}`);
            this.docs = await docs.json();
        },
        async get_past_docs() {
            console.log("past mode")
            this.state = -1;
            let docs = await fetch(`/api/docs_past/${this.user_id}`);
            this.docs = await docs.json();
        },
        async get_created_docs() {
            console.log("created mode")
            this.state = 1;
            let docs = await fetch(`/api/docs_created/${this.user_id}`);
            this.docs = await docs.json();
        },
        sortDocsAlphabeticallyName() {
            console.log("sorting by name");
            this.docs.sort((a, b) => a.name.localeCompare(b.name));
        },
        sortDocsAlphabeticallyCreator() {
            console.log("sorting by creator");
            this.docs.sort((a, b) => a.creator.localeCompare(b.creator));
        },
        sortDocsDateCreated() {
            console.log("sorting by date");
            this.docs.sort((a, b) => a.Did - b.Did);
        }
    }
})