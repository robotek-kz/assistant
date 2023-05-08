import { types } from "./mutations";
import VFile from "@/models/vFile.model";

export default {
    openFile: async({state, commit}, { file_id }) => {
        if (!state.openFiles[state.activeEditor].includes(file_id)) {
            commit(types.SET_OPEN_FILES, {
                ...state.openFiles,
                [state.activeEditor]: [...state.openFiles[state.activeEditor], file_id],
            });
        }
        commit(types.SET_ACTIVE_FILES, {
            ...state.activeFiles,
            [state.activeEditor]: file_id,
        });
    },

    closeFile: async({state, commit, dispatch}, { editor, file_id}) => {
        if (state.activeFiles[editor] === file_id) {
            await dispatch("setActiveFile", {
                editor,
                file_id:
                  state.openFiles[editor].filter((_id) => _id !== file_id)[0] || null,
            });
            // commit(types.SET_ACTIVE_FILES, {
            //     ...state.activeEditor,
            //     [editor]:
            //       state.openFiles[editor] && state.openFiles[editor].length > 0
            //       ? state.openFiles[editor][0]
            //       : null,
            // });
        }
        commit(types.SET_OPEN_FILES, {
            ...state.openFiles,
            [editor]: state.openFiles[editor].filter((_id) => _id !== file_id)
        });
    },
    closeFileFromAllEditor: async ({ state, dispatch }, { file_id }) => {
        const editors = Object.keys(state.openFiles);
        for (let i = 0; i < editors.length; i++) {
            if (state.openFiles[editors[i]].includes(file_id)) {
                await dispatch("closeFile", { editor: editors[i], file_id })
            }
        }
        // commit(
        //     types.SET_OPEN_FILES,
        //     Object.keys(state.openFiles)
        // );
    },
    setActiveFile: async ({ state, commit }, { editor, file_id }) => {
        commit(types.SET_ACTIVE_FILES, {
          ...state.activeFiles,
          [editor]: file_id,
        });
      },
}