<template>
    <div class="notebook-controls">
        <div class="left-controls">
            <a href="javascript: void(0);"
            @click="executeNotebookCommand">
            <span>Run all paragraphs</span>
        </a>
        </div>
    </div>


</template>


<script>
export default {
    name: 'NotebookControls',
    props: {
        noteId: {required: true}
    }
}


</script>


<style scoped>
.notebook-controls {
    height: 30px;
    background: #f7f7f7;
}

.notebook-controls a {
    display: inline-block;
    height: 100%;
    padding: 2px 6px
}

.notebook-controls a span {
    vertical-align: middle;
}

.notebook-controls .left-controls {
    float: left;
    padding-left: 7px;
    height: 100%;
    display: flex;
}
</style>