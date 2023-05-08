<template>
  <div class="profile">
    <header class="header-user">
      <div class="info">
        <span>{{ currentUser.nickname }}</span>
        <img :src="currentUser.avatar_url" alt="" class="avatar">
      </div>
      <div class="actions">
        <button><fa :icon="['fas', 'toolbox']" size="2x" /></button>
        <button><fa :icon="['fas', 'sign-out-alt']" size="2x" /></button>
      </div>
    </header>
    <main>
    <div class="layout">
      
      <article>
        <h2>Эпизоды</h2>
        <p>Пройдите все эпизоды</p>
        <div class="episodes">
          <div v-for="episode in getEpisode" class="episode">
            <div class="description">
              <h3>{{ episode.episode.name }}</h3>
              <p>{{ episode.is_finished}}</p>
              <span>
              </span>
            </div>
            <div class="actions">
              <span v-if="episode.is_finished"><fa :icon="['far', 'check-square']" size="2x" style="color: green" /></span>
              <span v-else><fa :icon="['far', 'square']" size="2x" style="color: red" /></span>
              <button @click="test_episode(episode.episode.id)"><fa :icon="['fas', 'play-circle']" size="2x" /></button>
            </div>
          </div>
        </div>
      </article>

      <aside>
        <div class="header">
          <h3>Приложения</h3>
          <p>Выберите одно из приложений и начните создавать!</p>
        </div>

        <vue-horizontal class="horizontal">
          <div class="item" v-for="app in currentUser.application">
            <div class="card">
              <div class="image">
                <div class="playback">
                  <svg viewBox="0 0 24 24" width="24" height="24">
                    <path
                      d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 13.5v-7c0-.41.47-.65.8-.4l4.67 3.5c.27.2.27.6 0 .8l-4.67 3.5c-.33.25-.8.01-.8-.4z"/>
                  </svg>
                </div>
              </div>
              <div class="content">
                <div>
                  <div class="title">{{ app.application.description }}</div>
                  <span v-if="app.is_finished"><fa :icon="['far', 'check-square']" size="2x" style="color: green" /></span>
                  <span v-else><fa :icon="['far', 'square']" size="2x" style="color: red" /></span>
                </div>

                <div class="actions">
                  <b>{{ app.application.name }}</b>
                  <button @click="test_app(app.application)"><fa :icon="['fas', 'external-link-alt']" /></button>
                  <button @click="download(app.application)">Download</button>
                </div>
              </div>
            </div>
          </div>
        </vue-horizontal>
      </aside>
    </div>
  </main>
  </div>
</template>


<script>
import { mapActions, mapGetters, mapState } from 'vuex';
import ApiService from '@/services/api.service';
import { codemirror } from 'vue-codemirror';
import { copyToClipboard } from '@/utils/helper';
import VueHorizontal from "vue-horizontal";

export default {
  components: {
    codemirror,
    VueHorizontal
  },
  data() {
    return {
      test: 'Hello World\nHello World',
      sketches: [],
      isCopied: false,
      application_id: '',
      cmOption: {
        tabSize: 4,
        lineNumbers: true,
        line: true,
        foldGutter: true,
        styleSelectedText: true,
        mode: 'text/python',
        readOnly: true,
      },
    };
  },
  computed: {
    ...mapGetters('user', ['currentUser']),
    ...mapState('user', ['user']),
    ...mapGetters('profile_application_episode',['getProfileApplicationEpisodes']),
    getEpisode() {
      return this.getProfileApplicationEpisodes;
    }
    // getSketch() {
    //   const api = new ApiService('Something get wrong!');
    //   const data = api.get(`/users/${this.currentUser.id}/sketches`).then((res) => res)
    //     .catch((res) => {
    //       console.warn(res);
    //     });
    //   console.log('sketches:', data);
    //   return data;
    // },
  },
  async mounted() {
    const api = new ApiService('Something get wrong!');
    const body = await api.get(`/users/${this.currentUser.id}/sketches`);
    const sketches = await body.body;
    this.sketches = sketches.data;
  },
  methods: {
    ...mapActions('profile_application_episode', ['all','clear']),
    ...mapActions('profile_application_lines', ['allProfileLines']),
    test_episode(id) {
      console.log('bluat');
      this.allProfileLines(id);
      this.$router.push({ name: 'GameWindow', params: { id: id}});
      setTimeout(() => {
        this.clear();
      },2000); 
    },
    test_app(app) {
      this.application_id = app.id;
      this.all(app.id);
      // this.$router.push('/profile/episode');
    }, 
    copyCode(code) {
      copyToClipboard(code);
      this.isCopied = true;
      const interval = setInterval(() => {
        this.isCopied = false;
        clearInterval(interval);
      }, 600);
      // var toCopy  = document.getElementById( 'to-copy' ),
      // btnCopy = document.getElementById( 'copy' );
      // btnCopy.classList.add( 'copied' );
      
      //   var temp = setInterval( function(){
      //     btnCopy.classList.remove( 'copied' );
      //     clearInterval(temp);
      //   }, 600 );
    },
    download(app) {
      fetch(`http://localhost:5000/api/application/${app.id}/files/download`, {method: 'GET'
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(new Blob([blob]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'unknown.zip')
        document.body.appendChild(link)
        link.click()
    })
    }
  }
};
</script>


<style scoped>

.profile {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: 52px 1fr;
}

.profile .header-user {
  color: #212121;
  border-bottom: 2px solid #E30712;
  padding: 0.5em;
  font-size: 150%;
  display: flex;
  justify-content: space-between;
}
.profile .header-user .info {
  display: flex;
  align-items: center;
  gap: 0.4em;
}
.profile .header-user .actions {
  display: flex;
  align-items: center;
  gap: 0.4em;
}
.profile .header-user .info img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
}

.card {
  border-radius: 6px;
  overflow: hidden;
  color: #212121;
  border:  2px solid #E30712;
  background-color: #f8f8f8;
  height: 95%;
  display: flex;
  flex-direction: column;
  cursor: pointer;
}

.image {
  background-position: center !important;
  background-size: cover !important;
  background-repeat: no-repeat !important;
  padding-top: 50%;
  position: relative;
}

.image .playback {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.item .card {
  width: 200px;
}
.image svg {
  height: 48px;
  width: 48px;
  fill: currentColor;
  color: #ccc;
}

.card:hover .image .playback svg {
  color: #133D52;
}

.content {
  padding: 12px 16px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.title {
  font-size: 14px;
  font-weight: 700;
  line-height: 1.6;
  margin-bottom: 8px;
}

main .layout .episodes .episode .actions {
  display: flex;
  align-items: center;
  gap: 0.4em;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.5;
}
.actions button {
  color: #ccc;
}
.actions button:hover {
  color: #133D52;
}

aside .horizontal .item .card .content .actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
</style>

<style scoped>
.header {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

main {
  padding: 24px;
}


.episode {
  padding: 16px;
  width: 100%;
  border: 2px solid #E30712;
  border-radius: 6px;
  margin-top: 16px;
  display: flex;
  justify-content: space-between;
}

@media (min-width: 768px) {
  main {
    padding: 48px;
  }
}
</style>

<!-- Responsive Breakpoints -->
<style scoped>
.layout {
  display: flex;
  flex-wrap: wrap;
  margin: -32px;
}

article, aside {
  flex-grow: 1;
  width: 100%;
  padding: 32px;
}

.horizontal {
  --fixed: 200px;
  --count: 1;
  --gap: 12px;
  --margin: 24px;
}

@media (min-width: 768px) {
  .layout {
    flex-wrap: nowrap;
  }

  .horizontal {
    --count: 2;
    --margin: 0;
    --gap: 16px;
  }

  aside {
    width: 40%;
  }
}

@media (min-width: 1024px) {
  .horizontal {
    --count: 2;
  }

  aside {
    width: 40%;
  }
}

@media (min-width: 1280px) {
  .horizontal {
    --count: 3;
  }

  aside {
    width: 50%;
  }
}
</style>

<!--
## Responsive Logic
The margin removes the padding from the parent container and add it into vue-horizontal.
If the gap is less than margin, this causes overflow to show and peeks into the next content for better UX.
You can replace this section entirely for basic responsive CSS logic if you don't want this "peeking" experience
for the mobile web.
Note that this responsive logic is hyper sensitive to your design choices, it's not a one size fit all solution.
var() has only 95% cross browser compatibility, you should convert it to fixed values.

There are 2 set of logic:
0-768 for peeking optimized for touch scrolling.
>768 for navigation via buttons for desktop/laptop users.
-->
<style scoped>
@media (max-width: 767.98px) {
  .item {
    width: var(--fixed);
    padding: 0 calc(var(--gap) / 2);
  }

  .item:first-child {
    width: calc(var(--fixed) + var(--margin) - (var(--gap) / 2));
    padding-left: var(--margin);
  }

  .item:last-child {
    width: calc(var(--fixed) + var(--margin) - (var(--gap) / 2));
    padding-right: var(--margin);
  }

  .item:only-child {
    width: calc(var(--fixed) + var(--margin) * 2 - var(--gap));
  }

  .horizontal {
    margin: 0 calc(var(--margin) * -1);
  }

  .horizontal >>> .v-hl-container {
    scroll-padding: 0 calc(var(--margin) - (var(--gap) / 2));
  }

  .horizontal >>> .v-hl-btn {
    display: none;
  }
}

@media (min-width: 768px) {
  .item {
    width: var(--fixed);
    margin-right: var(--gap);
  }
}

@media (min-width: 1024px) {
  .item {
    width: calc((100% - ((var(--count) - 1) * var(--gap))) / var(--count));
  }
}
</style>