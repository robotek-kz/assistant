<template>
    <div class="game-wrapper">
        <!-- <div class="game-item"> 
            <div class="clickable-area" @click="toggleShowSketches">
                    <fa v-if="isShowSketches" :icon="['fas', 'book-open']" />
                    <fa v-else :icon="['fas', 'book']" />
                <span id="filename">{{ gameFilename }}</span>
            </div>
            <div class="context-menu">
            </div>
        </div> -->
        <div class="sketches">
            <SketchItem
                :sketchItem="sketches"
            />
        </div>
    </div>
</template>


<script>
import SketchItem from '@/components/GameSketch/SketchItem.vue';
import { 
    FileTextIcon,
    MoreVerticalIcon, } from "vue-feather-icons";
import { mapActions } from "vuex";
export default {
    name: "GameItem",
    components: {
        FileTextIcon,
        MoreVerticalIcon,
        SketchItem,
    },
    computed: {
        sketches() {
            const gs = this.gameItem;
            return gs;
        }
    },
    data() {
        return {
            readonly: true,
            gameFilename: "",
            isShowSketches: false,
        };
    },
    props: {
        gameItem: Object,
    },
    methods: {
        // toggleShowSketches() {
        //     this.isShowSketches = !this.isShowSketches;
        // },
    },
    watch: {
    },
    mounted() {
        console.log('from GameItem', this.gameItem);
        this.gameFilename = this.gameItem.name;
    },
};
</script>



<style>
.game-wrapper {
    display: flex;
    flex-direction: column;
}
.game-wrapper .sketches {
    margin-left: 10px;
    display: flex;
    flex-direction: column;
}

.game-item {
    display: flex;
    color: #E30712;
    flex-direction: row;
    align-items: center;
    padding: 2px 5px 2px 0;
    margin: 2px 5px;
    border-radius: 5px;
}

.game-item .clickable-area {
    display: flex;
    align-items: center;
    flex: 1;
    padding: 0.3em
}
#filename {
    padding-left: 0.5em;
}
</style>