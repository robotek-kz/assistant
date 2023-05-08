import Vue from 'vue';
import VueRouter from 'vue-router';
import Start from '../views/Start.vue';
import Projects from '../views/Projects.vue';
import Lesson from '../views/Lesson.vue';
import Settings from '../views/Settings.vue';
import PageNotFound from '../views/PageNotFound.vue';
import Rating from '../views/Rating.vue';
import Register from '../views/Register.vue';
import Login from '../views/Login.vue';
import Profile from '../views/Profile.vue';
import Sketches from '../views/Sketches.vue';
import SketchRun from '../views/SketchRun.vue';
import OneFile from '../views/OneFile.vue';
import CodeEditor from '../views/CodeEditor.vue';
import Days from '../views/Days.vue';
import Packages from '../views/Packages.vue';
import GameWindow from '../views/GameWindow.vue';
import Files from '../views/Files.vue';
import Admin from '../views/Admin.vue';
import Episode from '../views/Episode.vue';
import LinesEditor from '../views/LinesEditor.vue';
import Application from '../views/Application.vue';
import ProfileApplicationEpisode from '../views/ProfileApplicationEpisode.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Start',
    component: Start,
  },
  {
    path: '/lesson',
    name: 'Lesson',
    component: Lesson,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings,
  },
  {
    path: '/projects',
    name: 'Projects',
    component: Projects,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/sketches',
    name: 'Sketches',
    component: Sketches,
  },
  {
    path: '/@:nickname',
    name: 'nickname',
    component: Profile,
  },
  {
    path: '/profile/episode',
    name: 'ProfileApplicationEpisode',
    component: ProfileApplicationEpisode
  },
  {
    path: '/run-sketch',
    name: 'SketchRun',
    component: SketchRun,
  },
  {
    path: '/one-file',
    name: 'OneFile',
    component: OneFile,
  },
  {
    path: '/code-editor',
    name: 'CodeEditor',
    component: CodeEditor,
  },
  {
    path: '/rating',
    name: 'Rating',
    component: Rating,
  },
  {
    path: '/days',
    name: 'Days',
    component: Days,
  },
  {
    path: '/packages',
    name: 'Packages',
    component: Packages
  },
  {
    path: '/game-window/:id',
    name: 'GameWindow',
    component: GameWindow,
  },
  {
    path: '/file',
    name: 'Files',
    component: Files,
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin,
  },
  {
    path: '/application',
    name: 'Application',
    component: Application,
  },
  {
    path: '/episode/:id',
    name: 'Episode',
    component: Episode,
  },
  {
    path: "/lines-editor",
    name: "LinesEditor",
    component: LinesEditor
  },
  {
    path: '*',
    component: PageNotFound,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
