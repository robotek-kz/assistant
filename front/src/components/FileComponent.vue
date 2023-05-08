<template>
    <div>
        <div v-for="file in files" style="float:left">
            <span>{{  file.name  }}</span>
        </div>
    </div>
</template>


<script>
export default {
    name: "FileComponent",
    data() {
        return {
            files: []
        }
    },
    props: {
        url: String
    },
    mounted() {
        fetch(`http://localhost:5000${this.url}`).then((response) => response.json()).then((data) => this.files = data);
    }
}

</script>


<style>

</style>