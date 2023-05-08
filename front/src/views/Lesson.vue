<template>
  <div class="app-container">
    <div v-html="singleMark" />
  </div>
</template>


<script>
import { mapGetters } from 'vuex';

import 'highlight.js/styles/googlecode.css';

const marked = require('marked');
const hljs = require('highlight.js');

marked.setOptions({
  renderer: new marked.Renderer(),
  sanitize: false,
  gfm: true,
  breaks: true,
  tables: true,
  highlight(code) {
    return hljs.highlightAuto(code).value;
  },
});

export default {
  data() {
    return {
      text: '',
    };
  },
  computed: {
    ...mapGetters(['lessonText', 'language']),
    singleMark() {
      return marked(this.init() || '');
    },
  },
  methods: {
    async getLesson() {
      const url = `http://localhost:3000/code/${this.language.name}/${this.lessonText.name}`;
      try {
        const resp = await axios.get(url);
        return resp.data;
      } catch (err) {
        if (err.request) {
          throw new Error('Без доступа к сети');
        } else {
          throw err;
        }
      }
    },
    init() {
      Promise.all([this.getLesson()])
        .then((resp) => {
          console.log('resp:', resp);
          [this.text] = resp;
        })
        .catch((err) => {
          if (err.message === 'No internet') {
            console.log('Отсутсвтует соединения с сервером.');
          } else {
            console.log('Пожалуйста попробуйте позже');
          }
        });

      return this.text;
    },
  },
};
</script>


<style lang="sass" scoped>

.app-container
  width: 100%
  margin: 2rem auto
  max-width: 800px
  padding: 1.5rem

h1, h2, h3, h4, h5, h6
  font-family: 'Source Sans Pro'
  line-height: 1


h1
  font-size: 3rem


h2
  font-size: 2.2rem
  margin-top: 3.4em


h3
  font-size: 1.6rem
  margin-top: 1.8em


p
  position: relative


pre
  background: gray
  color: #fff
  overflow-x: auto
  overflow-y: visible

pre b
  color: #bac9d8


pre, pre code
  font-family: 'Fira Mono'
  font-size: 1.1em

code
  padding: .1em .2em


pre, .demo, .note
  line-height: 1.8
  padding: 4em 2em 2em
  border-radius: 0px
  position: relative
  margin: 2em 0

pre:before, .demo:before, .note:before
  color: #bbb
  font-family: 'Source Sans Pro'
  content: '💻 Python (py template):'
  position: absolute
  top: 0
  left: 0
  background: rgba(0, 0, 0, 0.2)
  display: block
  width: 100%
  border-radius: inherit
  padding: .4em .4em .4em .8em
  box-sizing: border-box


ul
  margin: 2rem 0


* + li
  margin-top: 1em


.demo li
  margin-top: 0rem


.demo, p.note
  background: inherit
  border: 1px solid #42b883
  font-family: sans-serif

.demo:before, p.note:before
  content: '👀 OUTPUT:'
  color: #fff
  background: #42b883


p.note
  font-family: 'Source Serif Pro'
  border-color: #42b883
  background: #d6f0e4
  border: none
  padding: 1em .5em 1em 2rem
  border-left: 8px solid #42b883

p.note:before
  content: '💡'
  background: transparent
  top: .4em
  font-size: 1.5em
  left: .15em
  margin: 0
  padding: 0
  position: absolute


input
  padding: .5em
  width: 100%
  display: inline-block
  font-size: .9em

input[type=range]
  padding: 0
  width: auto
  display: inline-block


.comment
  color: #aaa


.highlight
  position: relative
  display: inline-block
  width: 100%
  left: -.6em
  padding: .2em 0 .2em .6em
  background: -webkit-gradient(linear, left top, right top, from(#47627f), to(transparent))
  background: linear-gradient(to right, #47627f, transparent)


.alert
  background: red
  color: white


[disabled]
  opacity: .5

</style>
