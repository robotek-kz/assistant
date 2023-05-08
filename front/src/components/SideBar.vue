<template>
    <div class="side-navigation-bar">
        <div class="branding">
            <img src="../styles/brand.png" alt="" width="42" height="26">
        </div>
        <div class="menu expand">
            <router-link to="/">
               <div class="menu-icon">
                    <fa :icon="['fas', 'home']" />
                    <span class="menu-tooltip">Главная</span>
               </div>
            </router-link>
            <router-link to="/projects">
                <div class="menu-icon">
                  <fa :icon="['fas', 'tasks']" />
                  <span class="menu-tooltip">Упражнения</span>
                </div>
            </router-link>
            <router-link to="/code-editor">
              <div class="menu-icon">
                  <fa :icon="['fas', 'pen-fancy']" />
                  <span class="menu-tooltip">Редактор кода</span>
              </div>
            </router-link>
            <router-link to="/rating">
              <div class="menu-icon">
                  <fa :icon="['fas', 'star']" />
                  <span class="menu-tooltip">Рейтинг</span>
              </div>
            </router-link>
            <router-link to="/sketches">
              <div class="menu-icon">
                  <fa :icon="['fas', 'gamepad']" />
                  <span class="menu-tooltip">Скетчи</span>
              </div>
            </router-link>
        </div>
        <div class="menu">
          <router-link to="/packages">
            <div class="menu-icon">
              <fa :icon="['fas', 'file-archive']" />
              <span class="menu-tooltip">Модули</span>
            </div>
          </router-link>
          <router-link to="/settings">
            <div class="menu-icon">
              <fa :icon="['fas', 'wrench']" />
              <span class="menu-tooltip">Настройки</span>
            </div>
          </router-link>
          <router-link v-if="currentUser.nickname" exact :to="{
            name: 'nickname',
            params: { nickname: currentUser.nickname }
          }">
            <div class="menu-icon" >
               <fa :icon="['fas', 'user']" />
               <span class="menu-tooltip">{{ currentUser.nickname }}</span>
            </div>
          </router-link>
          <div v-else class="menu-icon">
            <fa :icon="['fas', 'ghost']" />
            <span class="menu-tooltip"> Вы не авторизованы</span>
          </div>
        </div>
    </div>
</template>


<script>
import { mapGetters } from "vuex";
export default {
    name: "SideBar",
    computed: {
      ...mapGetters('user', ["currentUser"]),
    }
}

</script>


<style lang="sass" scoped>
.side-navigation-bar
  background: #DCDCDD
  display: flex
  flex-direction: column
  align-items: center
  border-right: 2px solid #E30712

  .branding
    padding: 10px
    border-bottom: 2px solid #E30712


  .menu
    display: flex
    flex-direction: column
    align-items: center
    padding: 5px
    

    &.expand
      flex: 1

    .menu-icon
      width: 40px
      height: 40px
      display: flex
      align-items: center
      justify-content: center
      border-radius: 50%
      background: #133D52
      opacity: 0.5
      margin-bottom: 5px
      position: relative
      transition: 0.3s all ease-in-out
      color: ghostwhite

      .menu-tooltip
        position: absolute
        left: 60px
        top: 0
        z-index: 99
        white-space: nowrap
        background: #DCDCDD
        padding: 10px 15px
        border-radius: 5px
        color: black
        opacity: 0
        transform: translateX(-30px)
        transition: 0.3s all ease-in-out
        pointer-events: none

      &:hover
        z-index: 99
        background: #133D52
        opacity: 1
        cursor: pointer
        border-radius: 5px

        .menu-tooltip
          display: flex
          transform: translateX(0px)
          opacity: 1

      /* &.active
        background: #DCDCDD
        color: black
        opacity: 1
        border-radius: 5px */

</style>