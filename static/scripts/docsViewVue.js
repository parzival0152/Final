

const app = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
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
        async submit_approved() {
            let isValid = this.data_validate()

            if (isValid) {
                let res = await postData('/documents/'+this.id, {
                    choice:"approve",
                    data:this.template_data
                })
                if (res.status == 200) {
                    window.location.href = res.url
                }
                else {
                    //TODO: make sure things dont break if server is unable to respond
                }
            }

        },
        async submit_rejected() {
            let isValid = this.data_validate()

            if (isValid) {
                let res = await postData('/documents/'+this.id, {
                    choice:"reject",
                    data:this.template_data
                })
                if (res.status == 200) {
                    window.location.href = res.url
                }
                else {
                    //TODO: make sure things dont break if server is unable to respond
                }
            }
        },
        data_validate() {
            //TODO: add data validation here too

            return true
        }
    }
})