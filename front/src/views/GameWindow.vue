<template>
    <div id="main-layout">
        <GameExplorer
        :gameFiles="getProfileApplicationLines" />
        <SplitWindow
        @updatesplitwindow="printSomething"
        @updatesketchsplitwindow="updateSketch" />
    </div>
</template>


<script>
import SplitWindow from '@/components/GameSketch/SplitWindow.vue';
import GameExplorer from "@/components/GameSketch/GameExplorer.vue";
import { mapGetters } from "vuex";
export default {
    name: "Window",
    data() {
        return {
            gamesArray: [],
            game_id: '',
            codes: [],
        }
    },
    components: {
        GameExplorer,
        SplitWindow,
    },
    computed: {
        ...mapGetters("sketches", ["projects"]),
        ...mapGetters("profile_application_lines", ["getProfileApplicationLines"]),
        update() {
            console.log('hello world')
        },
    },
    mounted() {
        console.log('hello mazafka');
        // const id = this.$route.params.id;
        // if (id) {
        //     this.projects.map((project) => {
        //         project.file_game_sketches.map((file) => {
        //             if (file.project_game_sketch_id === id) {
        //                 const gameFiles = {};
        //                 gameFiles['name'] = file.name;
        //                 gameFiles['game_sketches'] = file.game_sketches;
        //                 gameFiles['id'] = file.id;
        //                 gameFiles['is_done'] = file.is_done;
        //                 gameFiles['project_game_sketch_id'] = file.project_game_sketch_id;
        //                 gameFiles['timestamp'] = file.timestamp;
        //                 this.gamesArray.push(gameFiles);
        //                 const codes = {};
        //                 codes['code'] = file.code;
        //                 codes['previous_code'] = file.previous_code;
        //                 this.codes.push(codes);
        //             }
        //         })
        //     });
        //     } else {
        //         console.log('nothing');
        //     }

        //     console.log(this.gamesArray);
        //     console.log(this.codes);
    },
    methods: {
        printSomething(n) {
            console.log('printSomething', n);
            this.gamesArray.map((x) => {
                x.game_sketches.map((y) => {
                    if (n.id === y.id) {
                        y.current_char = n.current_char;
                        y.current_line = n.current_line;
                    }
                });
            });
        },
        updateSketch(n) {
            this.gamesArray.map((x) => {
                x.game_sketches.map((y) => {
                    if (n.id === y.id) {
                        y.is_done = n.is_done;
                        y.current_char = n.current_char;
                        y.current_line = n.current_line;
                        y.current = n.current;
                    }
                    if (n.id + 1 === y.id) {
                        y.current = true;
                        console.log(y);
                    }
                });
            });
        }
    }
}

</script>


<style scoped>
#main-layout {
    height: 100%;
    overflow: hidden;
    display: grid;
    grid-template-columns: 300px 1fr;
    background: #F2F4F4;
}
</style>