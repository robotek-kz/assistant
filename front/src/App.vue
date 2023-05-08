<template>
  <div id="app" ref="app">
    <template v-if="!tooSmall">

      <SideBar />
      <keep-alive :exclude="['Run', 'Results', 'SketchRun' ]">
        <transition name="route" mode="out-in">
          <router-view></router-view>
        </transition>
      </keep-alive>
    </template>
    <SmallScreen v-else />
  </div>
</template>

<script>
import NavBar from '@/components//NavBar.vue';
import SideBar from '@/components/SideBar.vue';
import SmallScreen from '@/views/SmallScreen.vue';
import { mapGetters } from 'vuex';

export default {
  components: {
    NavBar,
    SmallScreen,
    SideBar,
  },
  computed: {
    ...mapGetters(['room', 'trackedContainers', 'language']),
    tooSmall() {
      return window.innerWidth < 640 || window.innerHeight < 480;
    },
    isPlaying() {
      return this.$route.path === '/run';
    },
  },
  methods: {
    trackMouse(ev) {
      if (!this.rafActive) {
        this.rafActive = true;
        requestAnimationFrame(() => {
          this.rafActive = false;
          this.trackedContainers.forEach((element) => {
            // console.log(element.tagName, element.className);
            const pos = element.getBoundingClientRect();
            const x = ev.pageX - pos.left;
            const y = ev.pageY - pos.top;
            element.style.setProperty('--mouse-x', `${x}px`);
            element.style.setProperty('--mouse-y', `${y}px`);
          });
        });
      }
    },
  },
};
</script>

<style lang="sass">
*
  margin: 0
  padding: 0

body
  font-family: sans-serif
  overflow: hidden

#app
  padding: 0 !important
  width: 100%
  min-height: 100vh
  display: grid
  grid-template-columns: 60px 1fr
  background: #F2F4F4
  position: relative


.route-enter-from
  opacity: 0
  transform: translateY(100px)

.route-enter-active
  transition: all 0.3s ease-out

.route-leave-to
  opacity: 0
  transform: translateY(-100px)

.route-leave-active
  transition: all 0.3s ease-in

</style>
