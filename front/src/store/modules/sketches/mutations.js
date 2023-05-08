import Vue from "vue";
import initialState from "./initialState";

export const types = {
    SET_PROJECTS: "SET_PROJECTS",
    SET_GAME_SKETCH: "SET_GAME_SKETCH",
    UPDATE_FILE_GAME_SKETCH: "UPDATE_FILE_GAME_SKETCH",
    UPDATE_GAME_SKETCH: "UPDATE_GAME_SKETCH",
    RESET_MODULE_STATE: "RESET_MODULE_STATE",
}


export default {
    [types.SET_PROJECTS]: (state, projects) => {
        state.projects = projects;
    },
    [types.SET_GAME_SKETCH]: (state, sketch) => {
        state.gameSketch = sketch;
    },
    [types.UPDATE_FILE_GAME_SKETCH]: (state, file) => {
        state.fileGameSketch.code = file['ready'];
        state.fileGameSketch.previous_code = file['previous_ready'];
    },
    [types.UPDATE_GAME_SKETCH]: (state, sketch) => {
        state.gameSketch.is_done = sketch['is_done'];
        state.gameSketch.current_char = sketch['current_char'];
        state.gameSketch.current_line = sketch['current_line'];
        state.gameSketch.current = sketch['current'];
    },
    [types.RESET_MODULE_STATE]: (state) => {
        const freshState = initialState();
        Object.keys(freshState).forEach(key => {
            state[key] = freshState[key];
        });
    }
}