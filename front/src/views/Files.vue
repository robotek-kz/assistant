<template>
    <div>
        <h1>Файлы для загрузки</h1>
        <div>
            <input type="file" @change="uploadFile" ref="file">
            <button @click="submitFile">Загрузить!</button>
          </div>
    </div>
</template>


<script>
export default {
    name: 'Files',
    data() {    
        return {
           file: null,
        }
    },
    mounted() {
        fetch("http://localhost:5000/api/users/files", {
            method: "GET"
        }).then(response => {
            return response.json();
        }).then(file => {
            console.log(file);
        });
    },
    methods: {
        uploadFile() {
        console.log(this.$refs.file.files);
        this.file = this.$refs.file.files[0];
      },
      submitFile() {
        const body = new FormData()
        body.append('file', this.file)
        fetch("http://localhost:5000/api/fileupload", {
        body,
        config: { headers: {
                'Content-Type': 'multipart/form-data'
            }},
        method: "POST"
        })
        }
    }
}

</script>


<style>


</style>