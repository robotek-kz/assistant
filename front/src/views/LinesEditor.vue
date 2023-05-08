<template>
    <div class="editor">
        <simplebar class="block files">
            <simplebar class="topbar">
                <ul class="file-tabs">
                    <li v-for="lines, key in getLinesEditor" @click="getCode(lines.id)">{{ lines.name }}</li>
                </ul>
                <!-- <button @click="admin">admin</button>
                <button @click="testFunc()">testFunc</button> -->
            </simplebar>
            <div>
                <fa @click="showModal" :icon="['fas', 'arrows-alt-h']" />
                    <fa @click="testRef" :icon="['fas', 'clipboard']" />
            </div>
            <div class="textarea">
                <div v-if="code.length === 0">
                    Awesome Editor
                </div>
                <div v-else>
                    <codemirror ref="editor"
                        v-model="code"
                        :options="cmOptions"
                        @ready="onCmReady"
                        @focus="onCmFocus"
                        @input="onCmCodeChange"/>
                    <!-- <textarea name="" id="testik" cols="30" rows="10" v-model="code" ref="editor"></textarea> -->
                </div>
            </div>
        </simplebar>
        <div class="block lines">
            <button @click="sendToServer" class="send-button">Send to server</button>   
            <div class="line-block" 
                     v-for="l, index in arrayLines" 
                     draggable 
                     @dragstart="startDrag($event, index)"
                     @drop="onDrop($event, index)"
                     @dragover.prevent
                     @dragend="dragEnd"
                     @dragenter.prevent
                     :class="l.current ? 'red' : 'black'">
                    id: {{  index }}
                    {{  l.name  }}
                    {{  l.ext }}
                    {{ l.number }}
                    <button @click="remove(index)">remove</button>
                    <button @click="setCurrent(index)">current</button>
                    <button @click="set(index)">set</button>
                </div>
        </div>
        <div class="block lines-properties">
            <div class="lines-editor">
                <codemirror ref="editorLines"
                        v-model="linesCode"
                        :options="cmOptionsLines"
                        @ready="onCmReadyLines"
                        @focus="onCmFocusLines"
                        @input="onCmCodeChangeLines" />
            </div>
            <div class="lines-form">
                    <div id="form">
                        <fieldset id="description">
                            <label for="lines_name">Название файла</label>
                            <input type="text" name="lines_name" v-model="name">
                            <label for="lines_number">Номер урока</label>
                            <input type="text" name="lines_number" v-model="number">
                            <label for="lines_tab_size">Количество пробелов</label>
                            <input type="text" name="lines_tab_size" v-model="tabSize">
                            <label for="lines_score">Очки</label>
                            <input type="range" min="0" max="10" v-model="score">
                            <label for="lines_language">Язык</label>
                            <select name="" id="">
                                <option value="py">py</option>
                            </select>
                        </fieldset>
                        <button @click="addLines" class="lines-form--button" id="add">Добавить</button>
                        <button id="change">Изменить</button>
                    </div>
                </div>
            </div>
            <vue-modal name="my-modal" size="xlg">
                <div class="tabs">
                    <div v-for="lines in getLinesEditor" class="tab">
                        <span @click="setAnotherCode(lines)">{{ lines.name }}</span>
                    </div>
                </div>
                    <textarea name="" id="" cols="30" rows="10"></textarea>
            </vue-modal>
    </div>

</template>


<script>
import { mapGetters } from "vuex";
import difflib from "difflib";
import { codemirror } from 'vue-codemirror'

// require styles
import 'codemirror/lib/codemirror.css'
export default {
    name: "LinesEditor",
    data() {
        return {
            code: '',
            linesCode: '',
            language: '',
            name: '',
            picked: '',
            dragging: -1,
            score: 0,
            arrayLines: [],
            number: 0,
            currentState: false,
            tabSize: 0,
            data: '',
            cmOptions: {
        // codemirror options
                tabSize: 4,
                mode: 'text/javascript',
                theme: 'base16-dark',
                lineNumbers: true,
                line: true,
            },
            cmOptionsLines: {
                tabSize: 4,
                mode: 'text/javascript',
                theme: 'base16-dark',
                lineNumbers: true,
                line: true,                
            }
        }
    },
    components: {
        codemirror
    },
    computed: {
        ...mapGetters("lines_editor", ["getLinesEditor", "getCurrentEpisode"]),
        isActive() {
            return this.currentState;
        },

        checkedValue: {
            get() {
                return this.defaultState
            },
            set(newValue) {
                this.currentState = newValue;
            }
        },
    },
    methods: {
        onCmReady(cm) {
        console.log('the editor is readied!', cm)
        },
        onCmFocus(cm) {
        console.log('the editor is focus!', cm)
        },
        onCmCodeChange(newCode) {
        console.log('this is new code', newCode)
        this.code = newCode
        },
        onCmReadyLines(cm) {
        console.log('the editor is readied!', cm)
        },
        onCmFocusLines(cm) {
        console.log('the editor is focus!', cm)
        },
        onCmCodeChangeLines(newCode) {
        console.log('this is new code', newCode)
        this.linesCode = newCode;
        },
        setAnotherCode(lines) {
            const another = lines.split;
            const code = this.data.split
            const diff = difflib.contextDiff(another, code);
            const result = diff.filter(d => d[0] === "+" || d[0] === "!")
            const fuck = result.map(res => res.slice(1))
            this.code = fuck.join('\n');
        },
        testFunc() {
            const secondCode =  this.getLinesEditor[this.data.id + 1]
            const code = this.data.split;
            const another = secondCode.split;
            const diff = difflib.contextDiff(another, code);
            const result = diff.filter(d => d[0] === "+" || d[0] === "!")
            const fuck = result.map(res => res.slice(1))
            this.code = fuck.join('\n');
        },
        getCode(id) {
            this.data = this.getLinesEditor[id];
            this.code = this.getLinesEditor[id].code;
        },
        testRef() {
            const selectedText = this.$refs.editor.codemirror.getSelection();
            this.linesCode = selectedText;
        },
        getSelectedText(el) {
            //depr
            var range = document.selection.createRange();
                if (range.parentElement() == el) {
                    return range.text;
                }
            if (typeof el.selectionStart == "number") {
                return el.value.slice(el.selectionStart, el.selectionEnd);
            } else if (typeof document.selection != "undefined") {
                console.log('hello');
                var range = document.selection.createRange();
                if (range.parentElement() == el) {
                    return range.text;
                }
            }
            return "";
        },
        addLines() {
        //    const data = [];
        //    this.linesCode.split('\n').reverse().map((element) => {
        //     if (element !== "") break
        //     element !== "" && data.push(element)
        //    });
        //    console.log(data.reverse())
            this.arrayLines.push(
                {
                    name:this.name,
                    code: this.linesCode, 
                    score: this.score,
                    number: this.number,
                    ext: this.language,
                    file_tab_size: this.tabSize,
                    mode: 'python',
                    file_name: this.name,
                    file_source: 'python.org',
                    file_lines: Number(this.linesCode.split("\n").length)
                }
                );
           this.name = '';
           this.language = '';
           this.linesCode = '';
           this.tabSize = 0;
           this.score = 0;
           this.number = 0;
        },
        setCurrent(ind) {
            this.arrayLines[ind]['current'] = true;
            console.log(this.arrayLines);
        },
        remove(ind) {
            this.arrayLines.splice(ind, 1);
        },
        set(ind) {
           this.name = this.arrayLines[ind]['name'];
           this.linesCode = this.arrayLines[ind]['code'];
           this.language = this.arrayLines[ind]['ext'];
           this.score = this.arrayLines[ind]['score'];
           this.number = this.arrayLines[ind]['number'];
           this.tabSize = this.arrayLines[ind]['tabSize'];
        },
        startDrag(evt, index) {
            evt.dataTransfer.dropEffect = 'move'
            evt.dataTransfer.effectAllowed = 'move'
            evt.dataTransfer.setData('itemID', index)
            this.dragging = index;
        },
        onDrop(evt, i) {
            // const itemID = evt.dataTransfer.getData('itemID')
            this.arrayLines.splice(i, 0, this.arrayLines.splice(this.dragging, 1)[0]);
        },
        dragEnd(evt) {
            this.dragging = -1;
        },
        sendToServer() {
            console.log('currentEpisode', this.getCurrentEpisode);
            // fetch("http://localhost:5000/api/episode/1/lines", {
            // body: '[{"file_tab_size":0,"file_source":"string","code":"string","mode":"string","ext":"string","file_lines":0,"score":0,"name":"string","number":0,"file_name":"string","current":true}]',
            // headers: {
            //     "Content-Type": "application/json"
            // },
            // method: "POST"
            // }).then((response) => console.log('response', response)).catch((error) => {
            //     console.log('error', error)
            // })
            fetch(`http://localhost:5000/api/episode/${this.getCurrentEpisode}/lines`, {
            body: JSON.stringify(this.arrayLines),
            headers: {
                "Content-Type": "application/json"
            },
            method: "POST"
            }).then((response) => console.log('response', response)).catch((error) => {
                console.log('error', error)
            })
        },
        admin() {
            this.$router.push('/admin')
        },
        showModal() {
            this.$modals.show('my-modal');
        },
    }
}

</script>


<style scoped>
.editor {
    display: grid;
    grid-template-columns: 1fr 300px 1fr;
}

.editor .block {
    border: 1px solid red;
    height: 100%;
}

.editor .block.files .topbar {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    
}

.editor .block.files .topbar .file-tabs {
    list-style-type: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: row;
    align-items: center;
}

.editor .block.files  .topbar .file-tabs li {
    padding: 7px 5px 7px 15px;
    opacity: 0.7;
    background: white;
    color: black;
    display: flex;
    flex-direction: row;
    align-items: center;
    border-bottom:  2px solid #E30712;
    max-width: 150px;
}

.editor .block.files  .topbar .file-tabs li span {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  pointer-events: none;
}
.editor .block.files  .topbar .file-tabs li:hover {
  opacity: 1;
  cursor: pointer;
  background-color: rgba(227, 7, 18, 0.7);
}
.editor .files {
    display: grid;
    grid-template-rows: 40px 1fr;
}


.editor .block.files .textarea .vue-codemirror {
  border: 1px solid #ccc;
  border-radius: 4px;
  height: 100vh !important;
  width: 100% !important;
}
.editor .block.files .textarea  .vue-codemirror ::v-deep .CodeMirror, .CodeMirror-gutters {
    font-size: 12px !important;
    color: black;
}


.editor .lines {
    overflow-y: scroll;
    height: 100vh;
}

.editor .block .line-block {
    width: 250px;
    height: 50px;
    border: 1px solid red;
    margin: 1.5em;
}
.editor .lines-properties {
    display: grid;
    grid-template-rows: 1fr 1fr;
}
.editor .lines-properties .lines-editor {
    margin: 0.5em;
    width: 500px;
}
.editor .lines-properties .lines-editor .vue-codemirror ::v-deep .CodeMirror, .CodeMirror-gutters  {
    font-size: 12px !important;
    color: black;
}

fieldset {
    border: 0;
}
#form {
    display: grid;
    grid-template-areas: 
      "description description"
      "change add";
  	grid-template-columns: 1fr;  
  	grid-template-rows: auto 50px;
    grid-gap: .8em .5em;
    background: #eee;
    padding: 1.2em;
    height: 90%;
}
#form label {
    display: block;
}
#description {
    grid-area: description
}
#add {
    grid-area: add;
}
#change {
    grid-area: change;
}
.editor .lines-properties .lines-form {
    margin: 0.5em;
}
.editor .lines-properties .lines-form input {
    margin: 0.5em;
    border: 1px solid red;
}
.editor .lines-properties .lines-form {
    box-sizing: border-box;
    border: 2px solid #ccc;
    border-radius: 4px;
    background-color: #f8f8f8;
    font-size: 12px;
    resize: none;
}
.editor .lines-properties .lines-form .lines-form--button {
   border: 1px solid black
}
.textarea {
    display:inline-block;
    position:relative;
}

.textarea .arrow {
    position: absolute;
    top: 10px;
    right: 60px;  
}

.textarea .arrow:hover {
    color: #ccc;
    position: absolute;
}
.textarea .button {
    position: absolute;
    top: 10px;
    right: 30px;
}
.textarea .button:hover {
    color: #ccc;
    position: absolute;
}

.form-control {
  font-family: system-ui, sans-serif;
  font-size: 0.8rem;
  font-weight: bold;
  line-height: 1.2;
  display: grid;
  grid-template-columns: 2em auto;
  gap: 0.5em;
}

.form-control + .form-control {
  margin-top: 1em;
}

.form-control:focus-within {
  color: var(--form-control-color);
}
.red {
    background-color: #FFCDD2;
}
.black {
    background-color: #7D383F;
}

.send-button {
    width: 100%;
    background-color: #7D383F;
    height: 2em;
    margin: 0.3em;
    padding: 0.3em;
}
.send-button:hover {
    background-color: white;
}
input[type="radio"] {
  /* Add if not using autoprefixer */
  -webkit-appearance: none;
  /* Remove most all native input styles */
  appearance: none;
  /* For iOS < 15 */
  background-color: var(--form-background);
  /* Not removed via appearance */
  margin: 0;

  font: inherit;
  color: currentColor;
  width: 1.15em;
  height: 1.15em;
  border: 0.15em solid currentColor;
  border-radius: 50%;
  transform: translateY(-0.075em);

  display: grid;
  place-content: center;
}

input[type="radio"]::before {
  content: "";
  width: 0.65em;
  height: 0.65em;
  border-radius: 50%;
  transform: scale(0);
  transition: 120ms transform ease-in-out;
  box-shadow: inset 1em 1em var(--form-control-color);
  /* Windows High Contrast Mode */
  background-color: CanvasText;
}

input[type="radio"]:checked::before {
  transform: scale(1);
}

input[type="radio"]:focus {
  outline: max(2px, 0.15em) solid currentColor;
  outline-offset: max(2px, 0.15em);
}
.tabs {
    display: flex;
    flex-direction: row;
    gap: 2em;
}
.tabs .tab {
    background-color: #ccc;
    padding: 0.4em;
    border-radius: 0.4em;
}
.tabs .tab:hover {
    background-color: #FFCDD2;
}
</style>