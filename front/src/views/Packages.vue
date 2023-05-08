<template>
    <div>
        <h1>Python модули</h1>
        <div>
            <input type="file" @change="uploadFile" ref="file">
            <button @click="submitFile">Upload!</button>
          </div>
    </div>
</template>


<script>
export default {
    name: 'Packages',
    data() {    
        return {
           images: null,
        }
    },
    methods: {
        uploadFile() {
        console.log(this.$refs.file.files);
        this.images = this.$refs.file.files[0];
      },
      submitFile() {
        const body = new FormData()
        body.append('wheel', this.images)
        body.append('name', this.images.name)
        body.append('path', this.images.name)
        console.log(this.images)
        fetch("http://localhost:5000/api/upload", {
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