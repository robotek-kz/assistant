<template>
  <div class="sketch_wrapper">
    <div class="projects">
      <h1>Проекты</h1>
    </div>
    <div class="single-file">
      <div class="block">
        <h1>Одиночные файлы</h1>
        <span>Количество: {{ countOneFile }}</span>
      </div>
      <div class="start-button">
        <router-link to="/one-file"><fa :icon="['fas', 'play']" size="6x"  /></router-link>
      </div>
    </div>
    <div class="multiple-files">
      <div class="block">
        <h1>Многофайловые</h1>
      </div>
    </div>
    <div class="low-code">
      <h1>Немножечко кода</h1>
    </div>
  </div>
  <!-- <div>
    <div class="sketch_wrapper">
      <div class="box one_file">
        <h1 class="text">One File</h1>
        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dolorum necessitatibus incidunt magni aperiam nam id est itaque veniam voluptates dolorem?</p>
        <router-link to="/one-file"><div class="icon"><fa :icon="['fas', 'play']" /></div></router-link>
      </div>

      
      <div class="box many_files">
        <h1 class="text">Many Files</h1>
        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dolorum necessitatibus incidunt magni aperiam nam id est itaque veniam voluptates dolorem?</p>
        <div class="icon"><fa :icon="['fas', 'play']" /></div>
      </div>

      <div class="box low_code_sketches">
        <h1 class="text">Low-code sketches</h1>
        <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Dolorum necessitatibus incidunt magni aperiam nam id est itaque veniam voluptates dolorem?</p>
        <div class="icon"><fa :icon="['fas', 'play']" /></div>
      </div>
    </div> -->
    <!-- <div v-for="temp, index in gameSketchList.data" :key="temp.id" class="card">
      <div class="card__created">
        <h2>{{ temp.name }}</h2>
        <p>монетки: {{ temp.score }}</p>
        <p>сложно: {{ temp.difficulty }}</p>
        <p>закончил: {{ temp.is_done }}</p>
        <p class="card--text__right">
          {{ temp.file_name }}.{{ temp.ext }}
        </p>
      </div>
      <codemirror
        :value="temp.code"
        :options="cmOptions"
        class="card__temp"
        @ready="onGameSketchCmReady"
      />
      <div class="card__buttons" v-if="temp.is_done !== 'finished'">
        <button @click="prepareSketchInfo(temp.id)">
          выбрать
        </button>
        <button v-if="temp.id === gameSketch.id" @click="run">
          <span v-if="temp.is_done === 'init'">начать</span>
          <span v-else-if="temp.is_done === 'continue'">продолжить</span>
        </button>
      </div>
      <div class="card__buttons" v-else>Ты закончил скетч.</div>
    </div>
    <button @click="getNext()">
      Next sketch
    </button> -->
  <!-- </div> -->
</template>


<script>
import { codemirror } from 'vue-codemirror';
import ApiService from '@/services/api.service';
import { mapGetters } from 'vuex';



export default {
  name: 'Sketches',
  components: {
    codemirror,
  },
  data() {
    return {
      template: [],
      cmOptions: {},
    };
  },
  computed: {
    ...mapGetters('user', ['currentUser']),
    ...mapGetters('sketches', ['projects']),
    countOneFile() {
      let count = 0;
      this.projects.map((project) => {
            count += 1;
      });
      return count;
    }
    // ...mapGetters('skethces', ['gameSketch']),
    // checkCurrent(id) {
    //   return id === this.gameSketch.id;
    // },
  },
  created() {
    // console.log('game sketh:', this.gameSketchList.data[0]);
    const script = document.createElement('script');
    script.async = true;
    script.src = '/cm/mode/python/python.js';
    // console.log(`loading: ${script.src}`);
    const others = document.getElementsByTagName('script')[0];
    others.parentNode.insertBefore(script, others);
  },
  mounted() {
    this.fetchSketces();
  },
  methods: {
    fetchSketces() {
            this.$store.dispatch('sketches/resetState');
            console.log('hello there', this.currentUser.id);
            this.$store.dispatch('sketches/allLoad', this.currentUser.id);
            // this.$store.dispatch('loadFileGameSketch', this.currentUser.id);
    },
    onGameSketchCmReady(cm) {
      this.cmOptions = cm;
      this.cmOptions.setOption('readOnly', true);
      this.cmOptions.setOption('tabSize', 4);
      this.cmOptions.setOption('lineNumbers', true);
      this.cmOptions.setOption('lineWrapping', true);
      this.cmOptions.setOption('foldGutter', true);
      this.cmOptions.setOption('styleSelectedText', true);
      this.cmOptions.setOption('matchBrackets', true);
      this.cmOptions.setOption('theme', 'material-darker');
      this.cmOptions.setOption('mode', 'python');
      // tabSize: 4,
      //   lineNumbers: true,
      //   lineWrapping: true,
      //   foldGutter: true,
      //   styleSelectedText: true,
      //   theme: 'material-darker',
      //   matchBrackets: true,
      //   readOnly: true,
    },
    async getNext() {
      console.log('Длина:', this.template.length);
      const api = new ApiService('Haha');
      const after = this.template[this.template.length - 1].timestamp;
      console.log('after:', after);
      const data = await api.get(`/users/${this.currentUser.id}/game_sketches`, {
        after,
      });
      console.log('Длина нужного:', data);
      const body = await data.body;
      this.template.push(...body.data);
    },
    run() {
      console.log('run');
      this.$router.push('/run-sketch');
    },
    prepareSketchInfo(id) {
      this.$store.dispatch('generateGameSketch', id);
      console.log('gameSketch', this.gameSketch);
    },
  },
};
</script>


<style lang="sass" scoped>
.sketch_wrapper
  display: grid
  grid-template-columns: repeat(2, [col] 1fr )
  grid-template-rows: repeat(3, [row] auto  )

.projects
  grid-column: col / span 2
  grid-row: row
  display: grid
  justify-content: center
  border-right: 2px solid #E30712
  border-top: 2px solid #E30712
  border-bottom: 2px solid #E30712

.single-file
  grid-column: col
  grid-row: row 2
  display: grid
  grid-template-columns: 1fr 1fr
  border-right: 2px solid #E30712
  border-bottom: 2px solid #E30712

  .block
    padding: 20px

  .start-button
    display: flex
    justify-content: center
    align-items: center
    opacity: 0.5
    background-color: #133D52
  
    &:hover
      opacity: 1
      background-color: #133D52
    .fa-play
      opacity: 0.5
      color:  ghostwhite
      &:hover
        opacity: 1



.multiple-files
  grid-column: col 2
  grid-row: row 2
  border-right: 2px solid #E30712
  border-bottom: 2px solid #E30712
  display: grid
  grid-template-columns: 1fr 1fr

  .block
    padding: 20px

.low-code
  grid-column: col / span 2
  grid-row: row 3
  border-right: 2px solid #E30712
  border-bottom: 2px solid #E30712
  display: grid
  justify-content: center
</style>

