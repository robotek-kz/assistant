<template>
        <div class="sketch-item"
        :class="{ 'active' : sketchItem.current, 'blocked' : !sketchItem.current, 'finished' : sketchItem.state === 'finished' }" 
        :disabled="sketchItem.state === 'finished'">
            <div class="clickable-area">
                <div>
                    <FileTextIcon class="icon" size="18" />
                    <span id="filename"
                          @click="generate(sketchItem)">{{ sketchItem.lines.name }}</span>
                </div>
                <div class="status">
                    <span v-show="sketchItem.state=='init'"><fa :icon="['far', 'square']" size="2x" /></span>
                    <span v-show="sketchItem.state=='finished'"><fa :icon="['far', 'check-square']" size="2x" style="color: green" /></span>
                </div>
            </div>
        </div>
</template>

<script>
import { 
    FileTextIcon,
    MoreVerticalIcon, } from "vue-feather-icons";
import { mapActions, mapGetters } from "vuex";
export default {
    name: "SketchItem",
    components: {
        FileTextIcon,
        MoreVerticalIcon,
    },
    computed: {
        ...mapGetters("profile_application_lines", ["getLine"]),
    },
    data() {
        return {
            sketchFilename: "",
        };
    },
    props: {
        sketchItem: Object,
    },
    methods: {
        ...mapActions("profile_application_lines", ["generateProfileLine"]),
        generate(item) {
            console.log('че за херня', item);
            if (item.state === 'finished' || item.current === false) {
                console.log('hello')
                return false;
            } else {
                console.log('heelllooo', item.lines.id);
                // this.$store.dispatch('sketches/generateSketch', item);
                this.generateProfileLine(item);
                console.log('this.getLine()', this.getLine);
            }
        }
    },
    watch: {
    },
    mounted() {
    },
};
</script>



<style scoped>
.sketch-item {
    display: flex;
    color: #212121;
    flex-direction: row;
    align-items: center;
    padding: 2px 5px 2px 0;
    margin: 2px 5px;
    border-radius: 5px;
}

.sketch-item .clickable-area {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex: 1;
    padding: 3px 10px;
}
.sketch-item .clickable-area .status {
    display: flex;
    align-items: center;
    gap: 0.4em;
}
.sketch-item.active {
    background: #FFCDD2;
}
.active:hover {
    background-color: #DCDCDD;
}
.blocked {
    background-color: #7D383F;
    border-radius: 10px;
}
.finished {
    background: #DCFFCD;
}
</style>