<template>
  <div ref="container" class="container" v-if="getCode">
    <div
      class="code"
      :class="{ready: cmReady, completed: isCompleted}"
      @keydown.capture.prevent="onKeyDown"
    >
      <codemirror
        ref="codemirror"
        v-model="getLine.lines.code"
        class="codemirror"
        :options="cmOptions"
        @ready="onCmReady"
        @focus="onFocus"
        @blur="onUnFocus"
      />
    </div>
    <div class="pop-up" :class="{hidden: !showPopUp, clickable: popUpClickable, 'small-font': popUpText.length > 15}">
      <div>
        <p v-show="popUpText === 'Снова'" class="hardcore-info">
          Не получилось сгенерировать
        </p>
        <h2 @click="popUp(false)">
          {{ popUpText }}
        </h2>
        <p v-show="isCompleted" class="results-info">
          Отправка на сервер...
        </p>
      </div>
    </div>
  </div>
  <div v-else class="template-window">

  </div>
</template>


<script>
import { mapActions, mapGetters } from 'vuex';
import ApiService from '@/services/api.service';

let loadMode = '';
let loadTheme = '';
const codemirror = () => import('@/cmLoader').then((module) => {
  loadMode = module.loadMode;
  loadTheme = module.loadTheme;
  return module.default;
});

export default {
  name: 'GameTyper',
  components: {
    codemirror,
  },
  data() {
    return {
      timeout: 0,
      countdown: 3,
      showPopUp: true,
      popUpClickable: false,
      popUpText: 3,
      cm: {},
      userText: '',
      codeText: '',
      started: false,
      pauseTime: 0,
      isCompleted: false,
      cmReady: false,
      toFix: 0,
      rightMostMistakeMarked: false,
      markers: [],
      currentLine: 0,
      currentChar: 0,
      correctCharsInLine: 0,
      freshCorrect: 0,
      liveWpmInterval: null,
      currentChange: {},
      stats: {
        history: [],
        wpmOverTime: [],
        firstCharTime: 0,
      },
    };
  },

  computed: {
    ...mapGetters('profile_application_lines', ['getLine']),
    ...mapGetters('user', ['currentUser']),
    getCode() {
      console.log(this.getLine.lines);
      if (typeof this.getLine.lines === 'undefined') {
        return false;
      } else {
        return true;
      }
    },
    cmOptions() {
      return {
        showInvisibles: this.getLine.lines.file_name,
        maxInvisibles: 2,
        undoDepth: 0,
        tabSize: this.getLine.lines.file_tab_size,
        styleActiveLine: false,
        lineNumbers: true,
        styleSelectedText: true,
        lineWrapping: true,
        matchBrackets: false,
        dragDrop: false,
        autoCloseBrackets: false,
        cursorBlinkRate: 320,
        smartIndent: false,
        lint: false,
        spellcheck: false,
        autocorrect: false,
        showCursorWhenSelectring: true,
        theme: 'eclipse',
        cursroScrollMargin: 100,
        readOnly: true,
      };
    },
  },
  watch: { 
    },
  methods: {
    ...mapActions("profile_application_lines", ["allProfileLines", "clearProfileLine", "updateProfileLine", "finishProfileLine"]),
    ...mapActions('profile_application_episode', ['all']),
    popUp(action, text = this.popUpText) {
      this.popUpText = text;

      if (action) {
        if (text === 'Продолжить' || text === 'Снова') {
          this.popUpClickable = true;
        }
      } else {
        this.popUpClickable = false;
        if (this.popUpText === 'Снова') {
          this.$emit('reset');
        }
        this.cm.focus();
        // дописать cm.focus()
      }
      this.showPopUp = action;
    },

    onKeyDown(ev) {
      const handleEnter = () => {
        const expectedText = this.cm.getLine(this.currentLine);
        if (this.correctCharsInLine === expectedText.length
        || this.correctCharsInLine === expectedText.length - this.getLine.current_char
        || this.correctCharsInLine === expectedText.length - 4) {
          this.cm.execCommand('goCharRight');
          this.currentLine += 1;
          this.currentChange = {
            ...this.currentChange,
            type: 'correct',
            text: 'Enter',
          };
          this.userText += '\n';
          if (this.currentLine + 1 === this.getLine.lines.file_lines && this.cm.getLine(this.currentLine).trim().length === 0) {
            // console.red('Last line is empty');
            this.stats.history.push(this.currentChange);
            this.completed();
          }

          if (true) {
            this.cm.execCommand('goLineStartSmart');
            this.currentChar = this.cm.getCursor().ch;
            this.userText += new Array(this.currentChar).join(' ');
            this.correctCharsInLine = this.currentChar;
          } else {
            this.currentChar = 0;
            this.correctCharsInLine = 0;
          }
          if (true) {
            let underScoreWidth = 1;
            if (!true && this.cm.getLine(this.currentLine).slice(0, this.getLine.lines.file_tab_size) === Array(this.getLine.lines.file_tab_size).fill(' ').join('')) {
              underScoreWidth = this.getLine.lines.file_tab_size;
            }
            this.cm.markText(
              { line: this.currentLine, ch: this.currentChar },
              { line: this.currentLine, ch: this.currentChar + underScoreWidth },
              {
                className: 'next-char', clearOnEnter: true, inclusiveRight: true,
              },
            );
          }
        } else {
          console.log('enter blocked before end of the line');
          this.currentChange = {
            ...this.currentChange,
            type: 'blockedEnter',
          };
        }
      };

      const handleWrite = (key) => {
        console.log(key);
        const lineText = this.cm.getLine(this.currentLine);
        if (this.currentChar !== lineText.length) {
          let expectedText = lineText[this.currentChar];
          let text = key;
          if (key === 'Tab') {
            text = Array(this.getLine.lines.file_tab_size).fill(' ').join('');
            if (expectedText === ' ') {
              if (lineText.slice(this.currentChar, this.currentChar + this.getLine.lines.file_tab_size) === text) {
                expectedText = text;
              }
            } else if (expectedText === '    ') {
              text = ' ';
            }
          }
          if (text === expectedText) {
            if (this.toFix) {
              this.currentChange = {
                ...this.currentChange,
                type: 'unfixed',
                text,
              };
            } else {
              this.cm.markText(
                { line: this.currentLine, ch: this.currentChar },
                { line: this.currentLine, ch: this.currentChar + text.length },
                { className: 'correct' },
              );

              this.currentChar += text.length;
              this.correctCharsInLine += text.length;
              this.currentChange = {
                ...this.currentChange,
                type: 'correct',
                text,
              };
              this.userText += text;
              if (text.length > 1) {
                this.cm.startOperation();
                for (let i = 0; i < text.length; i += 1) {
                  this.cm.execCommand('goCharRight');
                }
                this.cm.endOperation();
              } else {
                this.cm.execCommand('goCharRight');
              }

              if (this.currentLine + 1 === this.getLine.lines.file_lines && this.correctCharsInLine === this.cm.getLine(this.currentLine).length) {
                this.stats.history.push(this.currentChange);
                this.completed();
                // поменяй снизу true на что то другое
              } else if (true) {
                if (this.currentChar !== lineText.length) {
                  let underScoreWidth = 1;
                  if (true && this.cm.getLine(this.currentLine).slice(this.currentChar, this.getLine.lines.file_tab_size + this.currentChar) === Array(this.getLine.lines.file_tab_size).fill(' ').join('')) {
                    underScoreWidth = this.getLine.lines.file_tab_size;
                  }
                  this.cm.markText(
                    { line: this.currentLine, ch: this.currentChar },
                    { line: this.currentLine, ch: this.currentChar + underScoreWidth },
                    { className: 'next-char', clearOnEnter: true, inclusiveRight: true },
                  );
                }
              }
            }
          } else {
            this.toFix += 1;
            const marker = this.cm.markText(
              {
                line: this.currentLine, ch: this.currentChar,
              },
              {
                line: this.currentLine, ch: this.currentChar + text.length,
              },
              {
                className: 'mistake',
              },
            );
            this.markers.push(marker);
            this.currentChar += text.length;
            this.currentChange = {
              ...this.currentChange,
              type: 'mistake',
              fixQueuePos: this.toFix,
              expectedText,
              text,
            };
            if (text.length > 1) {
              this.cm.startOperation();
              for (let i = 0; i < text.length; i += 1) {
                this.cm.execCommand('goCharRight');
              }
              this.cm.endOperation();
            } else {
              this.cm.execCommand('goCharRight');
            }
          }
        } else {
          this.currentChange = {
            ...this.currentChange,
            type: 'lineEnd',
          };
        }
      };

      if (ev.ctrlKey && !ev.key) {
        return;
      }
      if (true) {
        if (ev.ctrlKey && ev.key === 'Insert') {
          this.cm.execCommand('goLineEnd');
          this.cm.execCommand('goCharRight');
          this.cm.markText(
            { line: this.currentLine, ch: this.currentChar },
            { line: this.currentLine, ch: this.cm.getLine(this.currentLine).length + 1 },
            { className: 'correct' },
          );
          this.currentLine += 1;
          this.currentChar = 0;
          this.correctCharsInLine = 0;
          this.stats.cheats = true;
          return;
        } if (ev.ctrlKey && ev.key === 'End') {
          this.stats.cheats = true;
          this.completed();
          return;
        } if (ev.ctrlKey && ev.key === 'Home') {
          // must import stats first
          this.cm.execCommand('goDocEnd');
          this.cm.markText(
            { line: 0, ch: 0 },
            { line: this.codeInfo.lines + 1, ch: 1 },
            { className: 'correct' },
          );
          this.currentLine = this.codeInfo.lines - 1;
          this.currentChar = this.cm.getLine(this.currentLine);
          this.correctCharsInLine = this.currentChar;
          this.stats.cheats = true;
          this.completed(true);
          return;
        }
      }
      if (ev.key.length > 9 || ev.key === 'GroupNext' || ev.key === 'Shift' || ev.key === 'CapsLock' || ev.key === 'Alt' || ev.key === 'AltGraph' || ev.key === 'PageUp' || ev.key === 'Delete' || ev.key === 'PageDown' || ev.key === 'Insert' || ev.key === 'Home' || ev.key === 'End' || ev.ctrlKey || ev.metaKey || ev.key.slice(0, 5) === 'Arrow' || (ev.key.length > 1 && ev.key[0] === 'F')) {
        // prevent double event and block keys
        return;
      }
      if (this.started && !this.stats.firstCharTime) {
        this.stats.firstCharTime = Date.now();
        this.$emit('start');
      }
      this.currentChange = {
        time: this.timeElapsed(),
        type: 'initialType',
        shift: ev.shiftKey,
        alt: ev.altKey,
        keyCode: ev.keyCode,
      };

      if (ev.key === 'Escape' || ev.key === 'Pause') {
        this.popUp(true, 'Продолжить');
        if (this.stats.firstCharTime) {
          this.pauseStart = Date.now();
        }
        this.$emit('pause', true);
      } else if (ev.key === 'Enter') {
        handleEnter();
      } else if (ev.key === 'Backspace') {
        if (this.toFix) {
          this.toFix -= 1;
          const marker = this.markers.pop();
          const position = marker.find();
          marker.clear();
          const markerLength = position.to.ch - position.from.ch;
          if (markerLength > 1) {
            this.cm.startOperation();
            for (let i = 0; i < markerLength; i += 1) {
              this.cm.execCommand('goCharLeft');
            }
            this.cm.endOperation();
          } else {
            this.cm.execCommand('goCharLeft');
          }
          // console.log(`cleared marker with a length of: ${markerLength}`);
          this.currentChar -= markerLength;
          this.currentChange = {
            ...this.currentChange,
            type: 'backspace',
            fixQueuePos: this.toFix,
          };
          if (this.toFix > 0) {
            if (this.rightMostMistakeMarked) {
              // console.log('corrected middle mistake');
              this.cm.markText(position.from, position.to, { className: 'corrected middle' });
            } else {
              // console.log('corrected right-most mistake');
              this.cm.markText(position.from, position.to, { className: 'corrected right-most' });
              this.rightMostMistakeMarked = true;
            }
          } else {
            if (this.rightMostMistakeMarked) {
              // console.log('corrected left-most mistake');
              this.rightMostMistakeMarked = false;
              this.cm.markText(position.from, position.to, { className: 'corrected left-most' });
            } else {
              // console.log('corrected alone mistake');
              this.cm.markText(position.from, position.to, { className: 'corrected alone' });
            }
            if (true) {
              let underScoreWidth = 1;
              if (!true && this.cm.getLine(this.currentLine).slice(this.currentChar, this.getLine.lines.file_tab_size + this.currentChar) === Array(this.getLine.lines.file_tab_size).fill(' ').join('')) {
                underScoreWidth = this.getLine.lines.file_tab_size;
              }
              this.cm.markText(
                { line: this.currentLine, ch: this.currentChar },
                { line: this.currentLine, ch: this.currentChar + underScoreWidth },
                { className: 'next-char', clearOnEnter: true, inclusiveRight: true },
              );
            }
          }
        } else {
          // console.log('Blocked backspace overshoot');
          this.currentChange = {
            ...this.currentChange,
            type: 'blockedBackspace',
          };
        }
      } else {
        handleWrite(ev.key, ev);
      }
      console.log('ev.key', ev.key);
      if (this.currentChange.type !== 'initialType') {
        this.stats.history.push(this.currentChange);
      } else {
        console.log('currentChange:', this.currentChange);
      }
      this.currentChange = {};
    },
    timeElapsed() {
      return Date.now() - this.stats.firstCharTime - this.pauseTime;
    },
    onCmReady(cm) {
      this.cm = cm;
      this.init();
      this.fixHeight();
    },
    onFocus() {
      // console.log('cmFocus');
      this.$emit('pause', false);
      if (this.pauseStart) {
        this.pauseTime += Date.now() - this.pauseStart;
        this.pauseStart = null;
      }
    },
    onUnFocus(_, ev) {
      console.log('ev', ev);
      if (ev) {
        if (this.stats.firstCharTime) {
          this.pauseStart = Date.now();
        }
        if (!this.isCompleted && this.popUpText !== 'Try again' && ev) {
          if (ev.relatedTarget !== null) {
            if (ev.relatedTarget.tagName !== 'BUTTON' && ev.relatedTarget.tagName !== 'A') {
              this.popUp(true, 'Продолжить');
            }
          } else {
            this.popUp(true, 'Продолжить');
            this.$emit('pause', true);
          }
        }
      }
    },
    fixHeight() {
      const height = `${this.$refs.container.offsetHeight+250}px`;
      const scroll = this.$refs.codemirror.$el.getElementsByClassName('CodeMirror-scroll')[0];
      scroll.style.maxHeight = height;
    },
    start(interval) {
      clearInterval(interval);
      this.currentLine = this.getLine.current_line;
      this.currentChar = this.getLine.current_char;
      this.cm.markText(
        { line: this.getLine.lines.file_lines + 1, ch: 1 },
        { line: 0, ch: 0 },
        { className: 'bugfix' },
      );
      if (true) {
        this.cm.markText(
          { line: this.currentLine, ch: this.currentChar },
          { line: this.currentLine, ch: this.currentChar + 1 },
          { className: 'next-char', clearOnEnter: true, inclusiveRight: true },
        );
      }
      this.popUp(false, 'Вперед');
      this.started = true;
      this.cm.focus();
      this.cm.setCursor(this.getLine.current_line,this.getLine.current_char);
      this.stats.startTime = Date.now();
    },
    init() {
      console.log('gameSketch:', this.gameSketch);
      this.countdown = 3;
      this.showPopUp = true;
      this.popUpClickable = false;
      this.popUpText = 3;
      this.isCompleted = false;
      this.correctCharsInLine = 0;
      if (this.getLine.lines.code) {
      const initTime = Date.now();
      const interval = setInterval(() => {
        this.countdown -= 0.5
        this.popUpText = Math.ceil(this.countdown);
        if (this.countdown === 2) {
          if (!this.cmReady || !this.codeText) {
            this.countdown += 0.5;
            if ((Date.now() - initTime) / 1000 < 5) {
              this.popUpText = 'Самостоятельная работа...';
            } else {
              this.popUpText = 'WTF';
              this.popUp(false);
            }
          }
        } else if (this.countdown === 0) {
          this.start(interval);
        }
      }, 500);
      Promise.all([loadTheme('eclipse'), loadMode(this.cm, this.getLine.lines.mode, 'python')])
        .then(() => {
          this.codeText = this.getLine.lines.code;
          this.cmReady = true;
        })
        .catch((err) => {
          console.log('error', err);
        });
        }
    },
    completed() {
      this.cm.setOption('readOnly', 'nocursor');
      const complete = this.currentLine + 1 >= this.getLine.lines.file_lines;
      this.popUp(true, complete ? 'Скетч завершен' : 'Скетч завершен не полностью');

      // this.stats = {
      //   ...this.stats,
      //   time: this.timeElapsed(),
      //   correctLines: this.currentLine + 1,
      //   codeInfo: {
      //     ...this.gameSketch,
      //   },
      //   complete,
      // };

      // this.$emit('completed', this.stats);
      if (complete) {
        this.isCompleted = true;
        this.finishProfileLine({
          id: this.getLine.lines.id,
          state: 'finished',
          current_char: this.currentChar,
          current_line: this.currentLine,
          current: false
        });
        // this.$store.dispatch('sketches/updateFileSketch', {
        //   id: this.gameSketch.file_game_sketch_id,
        //   ready: this.gameSketch.ready,
        //   previous_ready: this.gameSketch.previous_ready
        // });
        this.$store.dispatch('files/createFile',{
          name: this.getLine.lines.name,
          content: this.getLine.lines.code
        });
        setTimeout(() => {
          this.clearProfileLine();
          this.allProfileLines(this.$route.params.id);
          this.popUp(false);
        }, 2000);
      } else {
        console.log('not completed');
        console.log(this.currentChar, this.currentLine);
        this.updateProfileLine({
          id: this.getLine.lines.id,
          state: "continue",
          current_char: this.currentChar, 
          current_line: this.currentLine,
          current: true,
        })
        // this.$store.dispatch('sketches/updateGameSketch', {
        //   id: this.getLine.lines.id,
        //   state: "continue",
        //   current_char: this.currentChar, 
        //   current_line: this.currentLine,
        //   current: true,
        // });
        // this.$emit('update',{
        //   id: this.gameSketch.id,
        //   is_done: 'continue',
        //   current_char: this.currentChar, 
        //   current_line: this.currentLine
        // })
        setTimeout(() => {
          this.clearProfileLine();
          this.allProfileLines(this.$route.params.id);
        }, 2000);
      }
    },
  },
};

</script>



<style lang="sass" scoped>
.container
  position: relative
  height: 100%

.template-window
  position: relative
  height: 100%
  width: 100%
  background: #DCDCDD

.code
  position: absolute
  opacity: 0
  outline: none
  height: 100%
  width: 100%

  transition: opacity .5s ease-in
  transition-delay: .7s
  pointer-events: none
  &.ready
    opacity: 1


.vue-codemirror  ::v-deep
  .CodeMirror
    height: 330px
.codemirror ::v-deep
  .CodeMirror-gutters
    border: none
  .CodeMirror-cursor
    border-left: 1px solid red
    border-right: none
    opacity: 1

  .CodeMirror-selected
    background: transparent

  .CodeMirror-line > span
    &::after
      display: none

    & > span
      font-size: 20px
      font-weight: normal
      filter: grayscale(30%) brightness(80%)
      line-height: 22px
      transition: filter 1s ease-out

    .correct
      filter: none

    .next-char
      border-bottom: 2px solid white

    .mistake
      background-color: rgba(255, 255, 255, .3)


  .CodeMirror-scroll
    padding-right: .7em

  .CodeMirror-vscrollbar
    &::-webkit-scrollbar
      width: $gap / 2 !important
    &::-webkit-scrollbar-thumb
      background: linear-gradient(to top, #DCDCDD) !important
    &::-webkit-scrollbar-track
      background-color: #DCDCDD !important
    &::-webkit-scrollbar-corner
      background-color: #DCDCDD !important

.pop-up
  display: flex
  align-items: center
  justify-content: space-around
  animation: opacity-enter .7s ease-out forwards
  position: absolute
  width: 100%
  height: 100%
  font-size: 4rem
  background-color: rgba(#1e202e, .5)
  cursor: default
  opacity: 1
  text-align: center
  z-index: 10
  user-select: none
  pointer-events: none


  h2
    margin-bottom: 2rem

  &.hidden
    animation: opacity-leave .4s ease-out forwards .1s
    pointer-events: none

  &.clickable
    pointer-events: all
    h2
      cursor: pointer


</style>
