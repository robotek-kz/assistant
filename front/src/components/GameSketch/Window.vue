<template>
<div id="main-layout">
    <GameExplorer />
</div>
</template>


<script>
import GameExplorer from "@/components/GameSketch/GameExplorer.vue";
export default {
    name: "Window",
    components: {
        GameExplorer
    }
}

</script>


<style scoped>
  #main-layout {
    height: 100%;
    display: grid;
    overflow: hidden;
    grid-template-columns: 300px 1fr;
    background: #F2F4F4;
  }
</style>