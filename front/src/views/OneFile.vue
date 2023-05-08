<template>
    <div>
        <div class="start-block">
            <div class="start-block__info">
              <h1><Однофайловые скетчи></h1>
            </div>
        </div>
        <div class="project_window">
            <div class="project_window--block" v-for="p, index in projects" :key="p.id">
                <h1 class="text"># {{ p.name }}</h1>
                <p>{{ p.is_done }}</p>
                <div class="project_window--buttons">
                    <button @click="showModal(p.id)"><fa :icon="['fas', 'play']" size="2x"/></button>
                    <button @click="nextWindow(p.id)">Start lesson</button>
                </div>
            </div>
        </div>
        <vue-modal name="my-modal" size="xlg">
            <h2 slot="header">Добро пожаловать</h2>
            <div class="window__steps">
                <div class="blocks">
                    <div class="step-block" v-for="level in levels">
                        <span @click="prepareSketchInfo(level.id)" 
                              class="step-block__span" 
                              :class="{ 'active' : level.current, 'blocked' : !level.current }" 
                              :disabled="level.is_done === 'finished'">{{ level.number }}</span>
                    </div>
                </div>
            </div>
            <div class="window">
                <div class="window__editor">
                    <div><button @click="showLevel(file.id)">{{ file.name }}</button></div>
                    <CodeDiffViewer :new-content="file.code" :old-content="file.previous_code" />
                    {{ file.ready }}
                    <hr>
                    {{ file.previous_ready }}
                </div>
            </div>
        </vue-modal>
    </div>
</template>



<script>

import { codemirror } from 'vue-codemirror';
import { mapGetters } from 'vuex';
import CodeDiffViewer from '@/components/Diff/CodeDiffViewer.vue';
export default {
    name: 'OneFile',
    components: {
        codemirror,
        CodeDiffViewer,
    },
    data() {
        return {
            cmOptions: {},
            file: {},
            levels: {},
        }
    },
    computed: {
        ...mapGetters('user', ['currentUser']),
        ...mapGetters('sketches',  ['gameSketch', 'projects']),
    },
    mounted() {
    },
    methods: {
        // fetchSketces() {
        //     this.$store.dispatch('sketches/resetState');
        //     console.log('hello there', this.currentUser.id);
        //     this.$store.dispatch('sketches/allLoad', this.currentUser.id);
        //     // this.$store.dispatch('loadFileGameSketch', this.currentUser.id);
        // },
        showLevel(id) {
            this.levels = this.file.game_sketches;
            console.log(this.levels);
        },
        nextWindow(id) {
            this.$router.push({ name: 'GameWindow', params: { id: id}});
        },
        showModal(id) {
            if (id) {
            this.levels = {};
            this.projects.map((project) => {
                project.file_game_sketches.map((file) => {
                    if (file.project_game_sketch_id === id) {
                        this.file = file;
                    }
                })
            });
            this.$modals.show('my-modal');
            } else {
                console.log('nothing');
            }

            // console.log('tydym:', this.fileGameSketch);
            // const data = Object.values(this.fileGameSketch)
            //         .filter((file) => file.project_game_sketch_id === id);
            // console.log('daaata', data[0].game_sketches_url.slice(4));
            // if (data) {
            //     this.$modals.show('my-modal');
            //     this.$store.dispatch('loadSketches', `${data[0].game_sketches_url.slice(4)}`);
            // } else {
            //     console.log('не найден');
            // }
        },
        onGameSketchCmReady(cm) {
            this.cmOptions = cm;
            this.cmOptions.setOption('readOnly', false);
            this.cmOptions.setOption('tabSize', 4);
            this.cmOptions.setOption('lineNumbers', true);
            this.cmOptions.setOption('lineWrapping', true);
            this.cmOptions.setOption('foldGutter', true);
            this.cmOptions.setOption('styleSelectedText', true);
            this.cmOptions.setOption('matchBrackets', true);
            this.cmOptions.setOption('theme', 'material-darker');
            this.cmOptions.setOption('mode', 'python');
            this.cmOptions.setOption('gutter', true)
        },
        prepareSketchInfo(id) {
            this.$store.dispatch('sketches/generateSketch', id);
            if (this.gameSketch.is_done === 'finished' || this.gameSketch.current === false) {
                return false;
            }
            this.$router.push('/run-sketch');
            this.$modals.hide('my-modal');
        }
    },
}

</script>


<style lang="sass" scoped>

.project_window
   display: grid
   grid-template-columns: 1fr 1fr
   gap: 0.5em
   padding: 3em
   background: ghostwhite

.project_window--block

  width: 100%
  height: 250px
  color: #212121
  font-size: 150%
  display: grid
  grid-template-rows: 1fr 1fr

.project_window--buttons
  display: flex
  justify-content: space-around
  background: #DCDCDD
  border-radius: 10px
  height: 70px

.start-block
  display: grid
  grid-template-columns: 1fr

  .start-block__info
    color: #212121
    border-bottom: 2px solid #E30712
    padding: 1.2em
    font-size: 150%

.text
  color: #212121
  text-align: center

.window
  display: grid
  grid-template-columns: 1fr

.codemirror ::v-deep
  .CodeMirror, .CodeMirror-gutters
    font-size: 1rem
    height: auto !important
    color: white
    background: transparent !important
  .CodeMirror
    color: white !important

  .CodeMirror pre.CodeMirror-line
    color: white !important


  .CodeMirror-linenumber
    width: 1rem !important
  .CodeMirror-line > span
    color: black
    & > span
      color: black

.window__steps
  display: grid
  padding: 0.4em

  .blocks
    display: grid
    grid-template-columns: repeat(auto-fill, minmax(50px, 1fr))
    grid-auto-rows: minmax(50px, auto)
    grid-gap: 3em
    .step-block
        width: 2em
        height: 2em
        color: black
        font-size: 150%
        border-radius: 10px


        .active
          border: 2px solid #055d67
          background-color: #055d67
          padding-left: 0.7em
          padding-right: 0.7em
          padding-bottom: 0.7em
          border-radius: 10px
          &:hover
            background-color: #044B53

        .blocked
          border: 2px solid #7d383f
          background-color: #7d383f
          padding-left: 0.7em
          padding-right: 0.7em
          padding-bottom: 0.7em
          border-radius: 10px

</style>