import { EDITORS  } from "./initialState";

export default {
    getActiveEditor: (state) => {
        return state.activeEditor;
    },
    getOpenFiles: (state, getters, rootState, rootGetters) => {
        return Object.keys(state.openFiles).reduce((result, editor) => {
            return Object.assign(result, {
                [editor]: state.openFiles[editor].reduce((file_results, file_id) => {
                const file = rootGetters["files/getFile"](file_id);
                if (file) file_results.push(file);
                return file_results;
            }, [])
            })
        }, {})
    },
    getActiveFiles: (state, getters, rootState, rootGetters) => {
        const primary_file_id = state.activeFiles[EDITORS.primary];
        const secondary_file_id = state.activeFiles[EDITORS.secondary];

        return {
            [EDITORS.primary]: primary_file_id
            ? rootGetters["files/getFile"](primary_file_id)
            : null,
            [EDITORS.secondary]: secondary_file_id
            ? rootGetters["files/getFile"](secondary_file_id)
            : null,
        };
    },
    getActiveFileList: (state, getters, rootState, rootGetters) => {
        const activeFiles = getters["getActiveFiles"];
        return Object.keys(activeFiles).reduce((result, editor) => {
            if (activeFiles[editor]) {
                return Object.assign(result, {
                    [activeFiles[editor].id]: true,
                });
            } else {
                return result;
            }
        }, {});

    },
    getChildren: (state, getters, rootState, rootGetters) => (parent_id) => {
        const files = rootGetters["files/getFiles"];
        const children = files.filter((item) => item.parent === parent_id);
        return children;
    }
};