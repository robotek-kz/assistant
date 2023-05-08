<template>
    <div class="split_window">
        <div class="game_window">
            <GameTyper
                ref="typer"
                @pause="(action) => {pause = action}"
                @update="printSomething"
                @updatesketch="updateSketch" />
            <div class="side-panel">
                <div class="button" @click="finish">
                    <fa :icon="['fas', 'thumbs-up']" />
                    <span class="button-tooltip">Завершить сейчас</span>
                </div>
            </div>
        </div>
        <!-- <simplebar class="diff-window diff-area">
            <CodeDiffViewer :new-content="code[0].code" :old-content="code[0].previous_code" />
        </simplebar> -->
    </div>
</template>



<script>
import GameTyper from '@/components/GameSketch/GameTyper.vue';
import { mapGetters } from "vuex";
import CodeDiffViewer from '@/components/Diff/CodeDiffViewer.vue';
export default {
    name: "SplitWindow",
    data() {
        return {
            new_content: 'dsadasd',
            old_content: 'dasfdsfasdsd',
        }
    },
    props: {
        // code: {},
    },
    computed: {
        ...mapGetters('sketches', ['projects']),
    },
    components: {
        GameTyper,
        CodeDiffViewer,
    },
    methods: {
        finish() {
           this.$refs.typer.completed();
        },
        printSomething(n) {
            this.$emit('updatesplitwindow',n)
        },
        updateSketch(n) {
            this.$emit('updatesketchsplitwindow',n)
        },
        // updateDiffTyper(n) {
        //     this.code[0].code = n.ready;
        //     this.code[0].previous_code= n.previous_ready;
        // }
    }
}
</script>



<style scoped>
.split_window {
    display: grid;
    grid-template-rows: 400px 1fr;
}

.game_window {
    display: grid;
    grid-template-columns: 1fr 100px;
}

.diff-window {
    height: 300px;
    padding: 2em;
}

.game_window .side-panel {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 2em;
    border-left: 2px solid #E30712;
    border-bottom: 2px solid #E30712;
}

.game_window .side-panel .button {
      margin-top: 1em;
      width: 40px;
      height: 40px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      background: #133D52;
      opacity: 0.5;
      margin-bottom: 5px;
      position: relative;
      transition: 0.3s all ease-in-out;
      color: ghostwhite;
}
.game_window .side-panel .button .button-tooltip {
    position: absolute;
    top: 0;
    z-index: 99;
    white-space: nowrap;
    background: #DCDCDD;
    padding: 10px 15px;
    border-radius: 5px;
    color: black;
    opacity: 0;
    transform: translateX(-10px);
    transition: 0.3s all ease-in-out;
    pointer-events: none;
}
.game_window .side-panel .button:hover {
    background: #133D52;
    opacity: 1;
    cursor: pointer;
    border-radius: 5px;
}

.game_window .side-panel .button:hover .button-tooltip {
    display: flex;
    transform: translateX(-120px);
    opacity: 1;
}

.diff-area {
    flex: 1;
    height: 100vh;
    display: flex;
    flex-direction: column;
    overflow: visible;
}
</style>