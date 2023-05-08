import initialState, { EDITORS } from "./initialState";

export const types = {
    SET_OPEN_FILES: "SET_OPEN_FILES",
    SET_ACTIVE_FILES: "SET_ACTIVE_FILES",
    SET_ACTIVE_EDITOR: "SET_ACTIVE_EDITOR",
    RESET: "RESET",
};


export default {
    [types.SET_OPEN_FILES]: (state, openFiles) => {
        state.openFiles = openFiles;
    },
    [types.SET_ACTIVE_EDITOR]: (state, activeEditor) => {
        state.activeEditor = activeEditor || EDITORS.primary;
    },
    [types.SET_ACTIVE_FILES]: (state, activeFiles) => {
        state.activeFiles = activeFiles;
    },
    [types.RESET]: (state) => {
        const freshState = initialState();
        Object.keys(freshState).forEach((key) => {
            state[key] = freshState[key];
        });
    },
}