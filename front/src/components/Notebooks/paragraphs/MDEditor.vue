<template>
    <div class="md-editor-inner">
        <editor-menu-bar :editor="editor">
        <div class="menubar" slot-scope="{ commands, isActive}">
            <button
                class="menubar__button"
                :class="{ 'is-active': isActive.bold() }"
                @click="commands.bold">
                bold
            </button>

            <button
                class="menubar__button"
                :class="{ 'is-active': isActive.italic() }"
                @click="commands.italic">

            </button>
        </div>
        </editor-menu-bar>
    </div>
</template>


<script>



</script>


<style>


</style>