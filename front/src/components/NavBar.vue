<template>
  <nav>
    <button class="title" @click="mainPage">
      Тренажер
    </button>

    <div class="links" :class="{'room-connected': room.connected}">
      <router-link to="/" class="link">
        <fa :icon="['fas', 'home']" :class="{flip: $route.path === '/run'}" />
        <span class="btn-text">
          Главная
        </span>
      </router-link>
      <router-link to="/projects" class="link">
        <fa :icon="['fas', 'tasks']" :class="{flip: $route.path === '/run'}" />
        <span id="v-step-2" class="btn-text">
          Упражнения
        </span>
      </router-link>
      <router-link to="/settings" class="link">
        <fa :icon="['fas', 'wrench']" :class="{flip: $route.path === '/run'}" />
        <span class="btn-text">
          Настройки
        </span>
      </router-link>
      <router-link to="/code-editor" class="link">
        <fa :icon="['fas', 'pen-fancy']" :class="{flip: $route.path === '/run'}" />
        <span class="btn-text">
          Редактор кода
        </span>
      </router-link>
      <router-link to="/rating" class="link">
        <fa :icon="['fas', 'star']" :class="{flip: $route.path === '/run'}" />
        <span class="btn-text">
          Рейтинг
        </span>
      </router-link>
      <router-link to="/sketches" class="link">
        <fa :icon="['fas', 'gamepad']" :class="{flip: $route.path === '/run'}" />
        <span class="btn-text">
          Скетчи
        </span>
      </router-link>
    </div>
    <div v-if="currentUser.nickname" class="profile">
      <div class="profile-name">
        <router-link
          class="btn-text"
          active-class="active"
          exact
          :to="{
            name: 'nickname',
            params: { nickname: currentUser.nickname }
          }"
        >
          <img
            :src="currentUser.avatar_url"
            alt=""
            width="24px"
            height="24px"
          >
          {{ currentUser.nickname }}
        </router-link>
        <button @click="logout">
          <fa :icon="['fas', 'sign-out-alt']" />
        </button>
      </div>
    </div>
    <div v-else class="profile">
      <span class="profile-name">
        Вы не авторизованы
      </span>
    </div>
    <!-- <v-tour name="myTour" :steps="steps" /> -->
  </nav>
</template>

<script>
import { mapGetters } from 'vuex';




export default {
  name: 'NavBar',
  data() {
    return {
      roomName: '',
      playerName: '',
      roomInfoMsg: '',
      showRoomCreator: false,
      showRoomLink: true,
      askForPlayerName: false,
      origin: window.location.origin,
      // steps: [
      //   {
      //     target: '#v-step-0', // We're using document.querySelector() under the hood
      //     header: {
      //       title: 'В путь',
      //     },
      //     content: 'Перед началом, необходимо ввести ваше имя!',
      //   },
      //   {
      //     target: '#v-step-1', // We're using document.querySelector() under the hood
      //     header: {
      //       title: 'Сохранитесь',
      //     },
      //     content: 'Теперь нужно сохранить имя!',
      //   },
      //   {
      //     target: '#v-step-2', // We're using document.querySelector() under the hood
      //     header: {
      //       title: 'Приступайте к обучению',
      //     },
      //     content: 'Выберите упражение и начинайте работать!',
      //   },
      // ],
    };
  },
  computed: {
    ...mapGetters(['room', 'options', 'language', 'userLanguage', 'currentUser', 'isAutheticated']),
  },
  sockets: {
    connect() {
      this.resetInfoMsg();
      console.warn('connected');
    },
    room_created() {
      this.$store.commit('SET_ROOM_PROPERTY', ['connected', true]);
      this.$store.commit('SET_ROOM_PROPERTY', ['name', this.roomName]);
      this.$store.commit('SET_ROOM_PROPERTY', ['myName', this.playerName]);
      this.$store.commit('SET_ROOM_PROPERTY', ['ownerName', this.playerName]);
      this.$store.commit('SET_ROOM_PROPERTY', ['owner', true]);
      this.$store.commit('SET_ROOM_PROPERTY', ['players', {
        [this.playerName]: {
          connected: true,
          ready: false,
          owner: true,
        },
      }]);
    },
    room_exist() {
      if (this.action === 'create') {
        console.error('ROOM ALREADY EXIST');
        this.roomInfoMsg = `Room "${this.roomName}" already exists.`;
        this.disconnect();
      } else {
        this.askForPlayerName = true;
      }
    },
    room_dont_exist() {
      if (this.action === 'create') {
        this.askForPlayerName = true;
      } else {
        console.error('ROOM DONT EXIST');
        this.roomInfoMsg = `Room "${this.roomName}" doesn't exist.`;
        this.disconnect();
      }
    },
    player_name_avaible() {
      this.$store.commit('SET_ROOM_PROPERTY', ['myName', this.playerName]);
      this.joinRoom();
    },
    player_name_taken() {
      console.error('PLAYER NAME TAKEN');
      this.roomInfoMsg = `Nick "${this.playerName}" is already taken.`;
    },
  },
  mounted() {
    // this.$tours.myTour.start();
    if (this.$route.params.roomName) {
      this.roomName = this.$route.params.roomName;
      this.checkRoom('join');
      this.$router.push('/');
    }
  },
  methods: {
    logout() {
      this.$store.commit('purgeAuth');
      localStorage.removeItem('id_token');
      this.$router.push('/');
    },
    mainPage() {
      if (this.room.owner) {
        this.$socket.client.emit('reset');
      }
      this.$router.push('/');
    },
    checkRoom(action) {
      this.action = action;
      this.$socket.client.io.opts.query = { roomName: this.roomName };
      this.$socket.client.open();
    },
    createRoom() {
      this.$socket.client.emit('createRoom', {
        ownerName: this.playerName,
        roomName: this.roomName,
        options: {
          codeLength: this.options.codeLength,
          autoIndent: this.options.autoIndent,
        },
        languageIndex: this.language.index,
      });
    },
    checkPlayerName() {
      this.$socket.client.emit('checkPlayerName', this.playerName);
    },
    joinRoom() {
      this.$socket.client.emit('joinRoom');
      this.askForPlayerName = false;
    },
    disconnect(action = false) {
      this.$socket.client.close();
      this.$store.commit('SET_ROOM_PROPERTY', ['connected', false]);
      this.$store.commit('SET_ROOM_PROPERTY', ['name', '']);
      this.$store.commit('SET_ROOM_PROPERTY', ['owner', false]);
      if (action) {
        this.askForPlayerName = false;
        this.roomName = '';
      } else {
        this.askForPlayerName = false;
      }
    },
    copy() {
      console.log(this.$refs.shareLink);
      this.$refs.shareLink.select();
      document.execCommand('copy');
      console.log('copied');
    },
    resetInfoMsg() {
      this.roomInfoMsg = '';
    },
  },
};
</script>

<style lang="sass" scoped>
@mixin padding-left
  padding-left: 1.2rem
  padding-right: 1.2rem

@mixin mouse-effect
  transition: background-color .15s ease-in-out

  &:hover
    background-color: rgba($white, .1)

  &:active
    background-color: rgba($white, .2)

@mixin small-btn
  text-align: center
  width: 40%
  padding: $grid-gap
  border-left: 1px solid $grey
  @include mouse-effect

.title
  // margin-top: 4% // 10-6
  font-size: 2rem
  font-weight: 600
  padding: 1.1rem 0
  width: 100%
  transition: opacity $nav-trans-dur $nav-trans-timing $nav-trans-dur, background-color .15s ease-in-out
  @include padding-left
  @include mouse-effect

nav
  height: 100%
  /* padding: 6% 0 */
  display: flex
  flex-direction: column
  justify-content: flex-start
  background: linear-gradient(340deg, #1e202e, #1e202e 20%, #242633)
  font-size: 1.2rem
  position: fixed

nav:after
  content: ''
  position: absolute
  pointer-events: none
  @include pos0
  transition: backdrop-filter $nav-trans-dur $nav-trans-timing 0s

.thin:after
  // backdrop-filter: hue-rotate(20deg)
  transition-delay: 1s
  backdrop-filter: hue-rotate(10deg) brightness(80%)

.thin
  $translate: translateX(calc(#{$nav-size} - 2.5em - #{$nav-move} / 2))
  .btn-text, .title, .room, .profile
    transition-delay: 0s
    opacity: 0
  svg:not(.heart)
    transition-delay: $nav-trans-dur
    transform: $translate
  .flip
    transform: $translate rotate(180deg) !important
  .author
    opacity: 0
    transition-delay: $nav-trans-dur

.btn-text, .room, .author, .profile
  transition: opacity $nav-trans-dur $nav-trans-timing $nav-trans-dur

.links
  display: flex
  flex-direction: column
  justify-content: space-evenly
  transition: min-height .5s ease-in-out


  .link
    display: block
    width: 100%
    padding: 1.1rem
    @include padding-left
    @include mouse-effect


  .line
    width: 100%
    // border-bottom: 1px solid $grey

  .btn-text
    margin-left: 1em

.links.room-connected
  min-height: 25%

svg
  display: inline-block
  width: 1em !important
  transition: transform $nav-trans-dur $nav-trans-timing 0s

.profile
  flex-grow: 1
  @include padding-left

  svg
    margin-top: $grid-gap

  input
    margin-left: 1em
    border-bottom: 1px solid $grey
    padding: $grid-gap


  .buttons
    display: flex
    margin-top: 1em
    justify-content: space-between

  button
    @include small-btn



.room
  flex-grow: 1
  @include padding-left

  svg
    margin-top: $grid-gap

  input
    margin-left: 1em
    border-bottom: 1px solid $grey
    padding: $grid-gap

.roomNotConnected
  display: flex
  flex-direction: column
  justify-content: space-between

  button
    @include small-btn

  .roomName, .playerName
    display: flex
    justify-content: space-between
    margin: 1em 0

  .buttons
    display: flex
    justify-content: space-between


  .info
    margin-top: 1em

.roomConnected
  .popUp
    margin-bottom: 2em
    .shareLink
      display: flex
      justify-content: space-between
      margin: 1em 0

    input
      flex-grow: 1

    .close-btn
      @include small-btn

  .roomNameContainer
    display: flex
    justify-content: space-between
    align-items: center
    margin-bottom: 1em

    svg
      margin-bottom: $grid-gap

input::placeholder
    color: $grey

button:disabled
  cursor: not-allowed

.author
  @include padding-left

  .author-text
    font-size: .9em

    .author-name
      white-space: nowrap

</style>
