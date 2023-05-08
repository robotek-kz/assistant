export const types = {
    SET_EPISODE_FILES: "SET_EPISODE_FILES"
}
export default {
    [types.SET_EPISODE_FILES]: (state, files) => {
        state.files = files;
    }
};