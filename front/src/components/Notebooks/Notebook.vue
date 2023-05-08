<template>
    <div>
        <div v-if="paragraphs === null" class="code-overlay-body">
            <div class="code-loader">
                <span>{</span>
                <span>}</span>
            </div>
        </div>
        <div
            v-else
            class="notebook">
            <div
                class="nb-controls-container">
                <h1>Notebook Controls</h1>
            </div>
            <div
                class="paragraph-container scrollbar"
                >
                <h1>Paragraph</h1>
            </div>
        </div>
    </div>

</template>

<script>
export default {
    name: 'Notebook',
    props: {
        note: { required: true }
    },
    components: {

    },
    data() {
        return {

        }
    },
    computed: {
        activeParagraphId() {
            return ''
        },
        notebook() {
            return ''
        },
        paragraphs() {
            return ''
        }
    },
    mounted() {
        console.log('this.fetchNode()');
    },
    methods: {
        setActive: (paragraph) => {

        },
        fetchNote: () => {

        }
    }
}
</script>

<style scoped>
.notebook {
    position: relative;
    height: 100%;
}

.nb-controls-container {
    position: absolute;
    width: 100%;
}


</style>