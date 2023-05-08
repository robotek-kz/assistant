<template>
    <div class="diff-viewer">
        <div class="title">
            <h3>{{ title }}</h3>
            <button @click="copyCode">COPY</button>
        </div>
        <div class="container" v-if="newContent && oldContent">
            <div class="left">
                <code-chunk v-for="(chunk, index) in splitedLeft"
                    :key="index"
                    :chunk="chunk" @expand="expandChunk"/>
            </div>
            <div class="right">
                <code-chunk v-for="(chunk, index) in splitedRight"
                    :key="index"
                    :chunk="chunk" @expand="expandChunk"/>
            </div>
        </div>
        <div v-else v-for="(chunk, index) in unifiedResult"
            :key="index">
            <code-chunk :chunk="chunk" :index="index"/>
        </div>
    </div>

</template>

<script>
import { diffLines } from 'diff/lib/diff/line';
import CodeChunk from './CodeDiffChunk.vue';
import { copyToClipboard } from '@/utils/helper';
export default {
    name: 'code-diff-viewer',
    components: {
        CodeChunk
    },
    props: {
        oldContent: String,
        newContent: String,
        title: String,
        collapse: {
            type: Number,
            default : 10
        }
    },
    data() {
        return {
            unifiedResult: [],
            splitedLeft: [],
            splitedRight: []
        }
    },
    created() {
        this.calculateDiff();
    },
    watch: {
        'title'(v) {
            this.calculateDiff();
        },
        'newContent'(v) {
            this.calculateDiff();
        },
        'oldContent'(v) {
            this.calculateDiff();
        }
    },
    methods: {
        copyCode() {
           let code = '';
           this.splitedRight.map((chunk) => {
            if (typeof chunk.lines !== 'undefined') {
                chunk.lines.map((lines) => {
                    code+=lines;
                    code+='\n';
                });
            }
        });
           copyToClipboard(code);
        },
        calculateDiff() {
            this.unifiedResult = this.diff();
            this.splitedRight = [];
            this.splitedLeft = [];
            if (this.unifiedResult.length) {
                const { left, right } = this.splitDiffResult(this.unifiedResult);
                console.log('elft', left, right);
                this.adaptSplitResult(left, right);
            }
        },
        diff() {
            if (this.newContent && this.oldContent) {
                const diffs = diffLines(this.oldContent, this.newContent, {
                    ignoreWhitespace: false
                });

                const length = diffs.length;
                return diffs.map((chunk, index) => {
                    const type = chunk.added ? 'add' : (chunk.removed ? 'remove' : '');

                    let lines = chunk.value.split('\n');
                    lines = index === length - 1 ? lines.slice(0) : lines.slice(0, -1);
                    return {
                        type,
                        lines,
                        lineCount: lines.length,
                        collapse: !type && lines.length > this.collapse
                    };
                });
            } else if (this.newContent || this.oldContent) {

                const diffs = this.newContent || this.oldContent;
                console.log(diffs);
                const lines = diffs.split('\n');
                console.log(lines);
                const type = !this.newContent ? 'remove' : (!this.oldContent ? 'add' : '');
                console.log(type);
                return [{
                    type,
                    lines,
                    lineCount: lines.length,
                    startCount: 1
                }];
            }
            return [];
        },
        splitDiffResult(diffResult) {
            const left = {
                chunks: [],
                lineCount: 1,
            };
            const right = {
                chunks: [],
                lineCount: 1
            };

            const setChunkLineNumber = (chunk, lineNumber) => {
                chunk.startLineNumber = lineNumber;
                return lineNumber + chunk.lineCount;
            };

            diffResult.forEach((chunk, index) => {
                if (chunk.type === 'add') {
                    right.lineCount = setChunkLineNumber(chunk, right.lineCount);
                    right.chunks.push(chunk);

                    if (this.shouldSetBlank(chunk.type, index)) {
                        left.chunks.push(this.createBlankChunk(chunk.lineCount));
                    }
                }
                else if (chunk.type === 'remove') {
                    left.lineCount = setChunkLineNumber(chunk, left.lineCount);
                    left.chunks.push(chunk);

                    if (this.shouldSetBlank(chunk.type, index)) {
                        right.chunks.push(this.createBlankChunk(chunk.lineCount));
                    }
                } else {
                    left.lineCount = setChunkLineNumber(chunk, left.lineCount);
                    left.chunks.push(chunk);

                    const clonedChunk = {...chunk};
                    right.lineCount = setChunkLineNumber(clonedChunk, right.lineCount);
                    right.chunks.push(clonedChunk);
                }
            });
            return {left, right};
        },
        adaptSplitResult(left, right) {
            left.chunks.forEach((leftChunk, index) => {
                const rightChunk = right.chunks[index];
                console.log('leftChunk', leftChunk.collapse);
                console.log('rightChunk', rightChunk.collapse);
                if (leftChunk.collapse && rightChunk.collapse) {
                    // 记录下左右栏chunk index; 点击展开时，通过此index定位chunk进行展开。
                    leftChunk.leftIndex = rightChunk.leftIndex = this.splitedLeft.length;
                    leftChunk.rightIndex = rightChunk.rightIndex = this.splitedRight.length;
                }
                this.splitedLeft.push(leftChunk);
                this.splitedRight.push(rightChunk);
                // 修改的行数不一致时，补充空白块。例如：左栏删除 3行，右栏添加5行代码。则左栏需补充 2行空白，进行对齐。
                if (leftChunk.type === 'remove' && rightChunk.type === 'add') {
                    const count = leftChunk.lineCount - rightChunk.lineCount;
                    if (count < 0) {
                        this.splitedLeft.push(this.createBlankChunk(Math.abs(count)));
                    }
                    else if (count > 0) {
                        this.splitedRight.push(this.createBlankChunk(count));
                    }
                }
            });
        },
        /**
         * 是否应该设置空白块：
         *    1. 最后一块返回 true
         *    2. 当前块是‘remove'类型，看下一块类型是否为空（没有变化）
         *    3. 当前块是‘add'类型，看上一块类型是否为空(没有变化)
         *
         * @param {type} type 当前块类型
         * @param {inddex} index 当前块索引
         * @return {boolean}
         */
        shouldSetBlank(type, index) {
            if (index === this.unifiedResult.length - 1) {
                return true;
            }
            index = type === 'remove' ? index + 1 : index - 1;
            const chunk = this.unifiedResult[index];
            return !chunk || !chunk.type;
        },
        /**
         * 创建空白块
         *
         * @param {number} lineCount 行数
         * @return {Object} 空白块对象
         */
        createBlankChunk(lineCount) {
            return {
                type: 'blank',
                lineCount,
                lines: new Array(lineCount).fill(' ')
            };
        },
        expandChunk(leftIndex, rightIndex) {
            this.splitedLeft[leftIndex].collapse = false;
            this.splitedRight[rightIndex].collapse = false;
        }   

    }
}
</script>

<style lang="sass" scoped>
.diff-viewer
  font-family: Consolas, "Liberation Mono", Menlo, Courier, monospace, sans-serif
  font-size: 1.2em
  margin-bottom: 15px
  border-radius: 5px
  border: 1px solid #ddd
  background-color: ghostwhite

  .title
    box-sizing: border-box
    text-align: right
    margin: 0
    padding: 5px 10px
    height: 40px
    line-height: 30px
    border-radius: 5px 5px 0 0
    border-bottom: 1px solid #212121
    background-color: #DCDCDD
    color: #212121
    font-weight: 600

  .container
    display: flex
    > div
      width: 100%



</style>