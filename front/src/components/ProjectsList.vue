<template>
  <div>
    <div class="buttons">
      <button class="button start-btn" :class="{ highlight: language.name }" @click="runCode">
        Начать игру
      </button>
      <button class="button start-btn" :class="{ highlight: language.name }" @click="runLesson">
        Посмотреть урок
      </button>
    </div>
    <div
      v-for="project in projectsList"
      :key="project.index"
      class="container"
    >
      <div class="card p-8 bg-white w-full max-w-xl my-10 mx-auto">
        <h1 class="text-center mb-8 font-bold py-3 text-2xl">
          {{ project.project_name }}
        </h1>
        <dl class="menu-list">
          <div
            v-for="(lesson,index) in project.lessons"
            :key="lesson.index"
            class="menu-list-item"
          >
            <label
              class="language"
              :class="{'selected':lesson.index === language.index}"
            >
              <dt>{{ lesson.name }} </dt>
              <input
                v-model="language"
                type="radio"
                :index="lesson.index"
                :value="project.lessons[index]"
              >
            </label>
          </div>
        </dl>
      </div>
    </div>
    <br>
    <br>
    <!-- <ul
      v-for="project in projectsList"
      :key="project.id"
    >
      <li>
        {{ project.project_name }} содержит {{ project.lessons.length }} урок
        <br>
        <label
          v-for="(lesson,index) in project.lessons"
          :key="lesson.id"
          class="language"
        >
          {{ lesson.name }}
          {{ language }}
          <input
            v-model="language"
            type="radio"
            :index="lesson.id"
            :value="project.lessons[index]"
          >
        </label>
      </li>
    </ul> -->
    <!-- <p>{{ projectsList }}</p> -->
  </div>
</template>


<script>
import { mapGetters } from 'vuex';
import { createHelpers } from 'vuex-map-fields';


const { mapFields } = createHelpers({
  getterType: 'getLanguage',
  mutationType: 'UPDATE_LANGUAGE',
});

export default {
  data() {
    return {
      searchText: '',
    };
  },
  computed: {
    ...mapGetters(['projectsList', 'customCode', 'lessonText']),
    ...mapFields(['language']),
    // filteredProject() {
    //   if (this.languagesList.length) {
    //     const search = this.searchText.toLowerCase();
    //     const filtered = this.languagesList
    //       .filter((language) => language.name.toLowerCase().includes(search))
    //       .sort((a, b) => (b.name.toLowerCase().startsWith(search) ? 1 : -1));
    //     return filtered.length > 0 ? filtered : this.languagesList;
    //   }
    //   return [...Array(29)].map(() => ({ name: 'Загрузка...' }));
    // },
  },
  methods: {
    runCode() {
      console.log('hello world');
      console.log('this.language', this.language);
      if (!this.language.name) {
        return false;
      }
      let fileIndex = -1;
      if (!this.customCode.text) {
        fileIndex = Math.floor(Math.random() * this.language.files.length);
      }
      this.$store.dispatch('generateCodeInfo', fileIndex);
      this.$router.push('run');


      // console.log(this.language.files.length);
      // let fileIndex = -1;
      // if (!this.customCode.text) {
      //   fileIndex = Math.floor(Math.random() * this.language.files.length);
      // }
      // console.log('FILE INDEX:', fileIndex);
      console.log(this.language);
      // this.$store.dispatch('generateCodeInfo', fileIndex);
      // if (this.room.owner) {
      //   this.$socket.client.emit('fileIndex', fileIndex);
      // }
    },
    runLesson() {
      this.$store.dispatch('generateLessonText');
      this.$router.push('lesson');
    },
  },
};

</script>



<style lang="sass" scoped>
.language
  min-height: 40px
  position: relative
  cursor: pointer
  background: $navy-grey
  opacity: 0.95
  box-shadow: 0px 0px 2px 2px rgba(black, .1)
  display: flex
  justify-content: space-around
  align-items: center
  background: linear-gradient(to right, #0ae7a5 5.8%, $grid-color 5.8%)
  background-size: 200%
  background-position: 99.8% 0 // 1px glitch
  transition: background .1s ease-in

.selected
  background-position: left
  transition: background 0.3s ease-in-out

  &:hover
    opacity: 0.85

.container
  display: flex
  justify-content: center
  align-items: center
  padding-top: 1em
  padding-bottom: 1em

.card
  width: 75%
  background-color: #242633
  box-shadow: 1rem 1rem 0 #0ae7a5


h1
  border-top: 2px solid #363749
  border-bottom: 2px solid #363749


.menu-list
  font-family: monospace
  font-size: 20px

dl.menu-list .menu-list-item
  display: flex
  margin: 5px 10px 10px 10px

dl.menu-list dt
  flex: 0 1 auto
  margin: 0px 0px 0px 0px
  order: 1

dl.menu-list .menu-list-item:after
  background-image:  radial-gradient(circle, #363749 0%, #363749 24%, #363749 25%, #363749 100%)
  background-size: .5em .5rem
  background-repeat: repeat-x
  background-position: left bottom
  content: ""
  display: block
  flex: 1 1 auto
  margin: 0px 12px 5px 12px
  order: 2

dl.menu-list dd
  flex: 0 1 auto
  margin: 0px 0px 0px 0px
  order: 3

.buttons
  display: flex
  justify-content: flex-end
  align-items: flex-start
  gap: 10px
  margin-top: $gap
  margin-bottom: $grid-gap
  margin-right: 1em

.button
  display: flex
  text-align: center
  justify-content: space-around
  align-items: center
  width: 150px
  height: 47px
  background: $grid-color
  margin-right: $gap
  cursor: pointer
  flex-grow: 1
  max-width: 250px

.start-btn, .ready-btn
  background: linear-gradient(to right, #0ae7a5 , #0ae7a5 50%, #242633 50% 100%)
  background-size: 200%
  background-position: right

  transition: background .2s ease-in

.start-btn
  margin-right: 0

.highlight
  background-position: left
  transition: background 1.2s ease-out
</style>
