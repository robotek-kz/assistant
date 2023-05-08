<template>
<div class="directory-listing">
        <component
            v-for="(file, index) in files"
            :key="file.file_id"
            :is="file.type"
            :file="file"
            :isActive="!!getActiveFileList[file.file_id]"
        />
</div>


</template>

<script>
import FileItem from '@/components/Editor/FileItem.vue';
import FolderItem from '@/components/Editor/FolderItem.vue';
import { FadeTransition } from "vue2-transitions";
import  { fileTypes } from '@/models/vFile.model.js';
import { mapGetters } from "vuex";
export default {
    props: {
        files: Array,
        activeFiles: Object,
    },
    components: {
        [fileTypes.FILE]: FileItem,
        [fileTypes.FOLDER]: FolderItem,
        FadeTransition,
    },
    computed: {
        ...mapGetters("editor", ["getActiveFileList"])
    },
    created() {
        this.fileTypes = fileTypes
    }
};
</script>


<style>


</style>