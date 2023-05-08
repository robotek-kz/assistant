export const types = {
    SET_LINES_EDITOR: "SET_LINES_EDITOR",
    SET_CURRENT_EPISODE: "SET_CURRENT_EPISODE",
}
export default {
    [types.SET_LINES_EDITOR]: (state, linesEditor) => {
        state.linesEditor = linesEditor;
    },
    [types.SET_CURRENT_EPISODE]: (state, currentEpisode) => {
        state.currentEpisode = currentEpisode;
    }
};