/// <reference path="index.js" />

const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        warnings:[],
        allowed: false,
        stage: -1,
        template_data: {}
    },
    computed: {
    },
    async created() {
        this.id = window.id;
        this.allowed = window.allowed == "True"
        let response = await fetch('/api/documents/' + this.id);
        let data = await response.json()

        this.template_data = data.data
        this.stage = data.stage
        if (!this.allowed) {
            this.stage = -1
        }
    },
    methods: {
        async submit(choise) {
            //get list of warnings from validity check
            this.warnings = checkValidityDocument(this.template_data,this.stage)

            //if there exist warnings return and dont continue
            if (this.warnings.length != 0) {
                return false
            }

            let res = await postData('/documents/'+this.id, {
                choice:choise,
                data:this.template_data
            })
            if (res.status == 200) {
                window.location.href = res.url
            }
            else {
                this.warnings = ["An error has occured, trying to submit again"]
                await new Promise(r => setTimeout(r, 1000)); //sleep for 1 second
                submit(choise)
            }

        }
    }
})