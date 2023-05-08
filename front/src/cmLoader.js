// modified lazy loader for webpack

import CodeMirror from 'codemirror';

import codemirror from 'vue-codemirror/src/codemirror.vue';
import 'codemirror/addon/mode/simple';
import 'codemirror/addon/mode/overlay';
import 'codemirror/lib/codemirror.css';
// import '../public/cm/theme/material-darker.ecss';
import 'codemirror/addon/selection/active-line';
import 'cm-show-invisibles/lib/show-invisibles';

// make cm global so modes can properly register
window.CodeMirror = CodeMirror;

let loading = {};

function splitCallback(cont, n) {
  let countDown = n;
  return () => {
    countDown -= 1;
    if (countDown === 0) {
      cont();
    }
  };
}

const ensureDeps = (mode, cont) => {
  const deps = CodeMirror.modes[mode].dependencies;
  if (!deps) return cont();
  const missing = [];
  for (let i = 0; i < deps.length; i += 1) {
    if (!Object.prototype.hasOwnProperty.call(CodeMirror.modes, deps[i])) {
      missing.push(deps[i]);
    } else {
      // console.log(`[ensureDeps ${mode}] Skipping ${deps[i]}`);
    }
  }
  if (!missing.length) {
    return cont();
  }
  const split = splitCallback(cont, missing.length);

  for (let i = 0; i < missing.length; i += 1) {
    CodeMirror.requireMode(missing[i], split);
  }
};

CodeMirror.requireMode = (mode, cont, reject) => {
  if (mode) {
    if (Object.prototype.hasOwnProperty.call(CodeMirror.modes, mode)) {
      return ensureDeps(mode, cont);
    }
    if (Object.prototype.hasOwnProperty.call(loading, mode)) {
      return loading[mode].push(cont);
    }


    const script = document.createElement('script');
    script.onerror = () => reject(Error('No internet'));
    script.async = true;
    script.src = `/cm/mode/${mode}/${mode}.js`;
    // console.log(`loading: ${script.src}`);
    const others = document.getElementsByTagName('script')[0];
    loading[mode] = [cont];

    // omg 12h of debugging
    const list = loading[mode];

    CodeMirror.on(script, 'load', () => {
    // console.log('load');
      ensureDeps(mode, () => {
        for (let i = 0; i < list.length; i += 1) {
          list[i]();
        }
      });
    });

    others.parentNode.insertBefore(script, others);
  } else {
    cont();
  }
};

CodeMirror.autoLoadMode = (instance, mode, mime) => new Promise((resolve, reject) => {
  if (Object.defineProperty.hasOwnProperty.call(CodeMirror, mode)) {
    // console.log(`[autoLoadMode] Skipping ${mode}`);
    resolve('SKIP');
  }

  CodeMirror.requireMode(mode, () => {
    // console.warn('requireMode CB');
    instance.setOption('mode', mime || mode);
    resolve('CB');
  }, reject);
});

const loadMode = async (cm, mode, mime) => {
  if (mode) {
    // console.log(`LOADING ${mode}`);
    loading = {};
    const resp = await CodeMirror.autoLoadMode(cm, mode, mime);
    return resp;
  }
  // console.log('no mode to load');
  return 'no mode to load';
};

const loadTheme = (name = 'material-darker') => {
  const existing = document.getElementById(name);

  if (!existing) {
    const link = document.createElement('link');
    link.href = `/cm/theme/${name}.css`;
    link.rel = 'stylesheet';
    link.id = name;
    document.head.appendChild(link);
  } else {
    return 'skip';
  }
};

export { loadMode, loadTheme };
export default codemirror;
