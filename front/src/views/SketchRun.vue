<template>
  <main
    :key="resetKey"
    @keydown.alt="resetSelf"
  >
    <div class="top-bar">
      <div class="info">
        <div class="languageName" />
        <div class="codeInfo">
          <p v-if="gameSketch.file_name">
            {{ gameSketch.file_name }}.{{ gameSketch.ext }}
          </p>
          <p>{{ codeSource }}</p>
        </div>
      </div>
      <div class="buttons">
        <button class="reset" @click="reset">
          По новой
        </button>
        <button class="finish" @click="finish">
          Закончить
        </button>
      </div>
    </div>
    <div v-show="$route.path === '/run-sketch'">
      <span v-show="pause">
        paused
      </span>
    </div>
    <!-- Changing key remounts component -->
    <GameSketch
      v-if="gameSketch.file_name"
      ref="gameSketch"
      :key="componentKey"
      class="code-editor"
      @reset="reset"
      @pause="(action) => {pause = action}"
    />
    <!-- <transition>
      <Results v-if="$route.path === '/results' && stats" :stats="stats" />
    </transition> -->
  </main>
</template>

<script>
import { mapGetters } from 'vuex';
import GameSketch from '@/components/GameSketch.vue';

export default {
  name: 'SketchRun',
  components: {
    GameSketch,
  },
  data() {
    return {
      componentKey: 1,
      resetKey: 1,
      stats: false,
      requestReset: false,
      pause: false,
      completed: false,
    };
  },
  computed: {
    ...mapGetters('sketches', ['gameSketch']),
    codeSource() {
      if (this.gameSketch.file_name) {
        return this.gameSketch.source === 'own' ? 'Создатель' : this.gameSketch.source;
      }
      return 'Молодец';
    },
    // languageName() {
    //   return this.gameSketch.name.replace('_', ' ');
    // },

  },
  created() {
    // if (!this.gameSketch.name) {
    //   this.$router.push('/');
    // }
  },
  methods: {
    reset() {
      this.componentKey += 1;
      if (this.$route.path === '/results') {
        this.$router.push('/run-sketch');
      }
    },
    resetSelf() {
      this.resetKey += 1;
      if (this.$route.path === '/results') {
        this.$router.push('/run-sketch');
      }
    },
    finish() {
      this.$refs.gameSketch.completed();
    },
    // onCompleted(stats) {
    //   this.stats = stats;
    //   this.completed = true;
    //   this.$emit('oneSketchCompleted', 'Скетч пройден, выберите другой');
    // },
    // startTimer() {
    //   console.log('timer start');
    // },
  },
};

</script>

<style lang="sass" scoped>
main
  width: 100%
  display: flex
  flex-direction: column
  justify-content: center
  align-items: center

  .codeEditor
    flex-grow: 1

.top-bar
  display: flex
  justify-content: center
  align-items: center
  position: relative
  animation: opacity-enter .5s ease-out forwards .7s
  animation-fill-mode: both
  margin-bottom: 1rem

  .info
    position: relative
    display: flex
    align-items: center
    min-width: 0

    .languageName
      font-size: 2rem
      margin-right: 1em
    .codeInfo
      display: flex
      justify-content: space-between
      flex-direction: column
      overflow: hidden
      p
        margin-bottom: $grid-gap

  .buttons
    flex-shrink: 0
    button
      text-align: center
      width: 150px
      height: 50px
      background: #DCDCDD
      margin-left: max(10px, calc(20vw - 210px))
      cursor: pointer
      &:hover
        border: 2px solid #E30712

@keyframes opacity-enter
  from
    opacity: 0
  to
    opacity: 1


</style>
