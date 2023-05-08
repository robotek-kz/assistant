import initialState from './initialState';

export const types = {
    RESET: "RESET",
    SET_FILES: "SET_FILES"
}

export default {
    [types.RESET]: (state) => {
        const freshState = initialState();
        Object.keys(freshState).forEach(key => {
            state[key] = freshState[key];
        });
    },
    [types.SET_FILES]: (state, files) => {
        state.files = files;
        state.filesById = Object.keys(files);
    },
};